#/tmp/maixpy_run/ 工作目录
from maix import camera, display, nn, app
import sys, math

sys.path.append(r'/root/neeko')
from NNDetector import NNDetector
from SERIAL_IO import SerialIO
from IdentifyColorCards import IdentifyColorCards

dis = display.Display()
serial = SerialIO()
identify_color_cards = IdentifyColorCards(_is_it_card_colour_by_hand=True)

#需要修改的参数
"""=================================================================================================================="""
identify_color_cards.set_card_colour_list([0, 1]) # 测试时修改 0:red 1:blue 2:green
detection_distance = 5
model_path = "/root/models/maixhub/147350/model_147350.mud"
"""=================================================================================================================="""
all_object_list = []
detector = nn.YOLOv5(model=model_path, dual_buff = True)
nnDetector = NNDetector(_detector=detector)
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())


class Execute:
    def __init__(self, _detection_distance=5):# 修改这个值
        self.detection_distance = _detection_distance
        self.state = None
        self.mode = None
        self.img = None
        self.duplicate_counting_list = []
        self.sign_position_list = None # 标志位置列表
        self.position_list = None
            # [identify_color_cards.get_first_card_colour(),
            #                        identify_color_cards.get_second_card_colour(), 1]

    def set_state(self, _state):
        self.state = _state
        print("The current state is:", self.state)

    def set_mode(self, _mode):
        self.mode = _mode
        print("The current mode is:", self.mode)

    def set_img(self, _img):
        self.img = _img

    def __is_it_duplicate_counting__(self, _position):
        if self.duplicate_counting_list:  # 重复计数列表
            for duplicate_position in self.duplicate_counting_list:
                if math.dist(_position, duplicate_position) < self.detection_distance:
                    print("Yes, it is duplicated")
                    return True
        print("No, it is not duplicated")
        return False

    def parse_coordinates_into_data(self, _position):
        pass

    def __identify_the_pills__(self, _colour_number):
        # self.position_list, self.img = nnDetector.detect(colour_number=_colour_number, _img=self.img)
        self.position_list = nnDetector.get_position(obj_list=all_object_list, colour_number=_colour_number)
        # 判断是否重复
        for position in self.position_list:
            if not self.__is_it_duplicate_counting__(position):
                print("self.sign_position_list", self.sign_position_list)
                serial.set_sign_position_list(self.sign_position_list)
                serial.send(position)
                break
            else:
                continue

    def __is_it_the_finals__(self):
        flag = True
        if len(self.position_list) != 0:
            for position in self.position_list:
                if not self.__is_it_duplicate_counting__(position):
                    flag = False
                    break

        if flag:
            self.sign_position_list = [identify_color_cards.get_first_card_colour(),
                                       identify_color_cards.get_second_card_colour(), 3]
            serial.set_sign_position_list(self.sign_position_list)

    def perform_analysis(self):
        """
        收
        数据包格式: 0xA1,0xA2,状态位,模式位,0xFE
        状态位: 0 默认位,1 到位准备抓取,2 完成抓取
        模式位: 0 默认位,1 药板,2 药瓶,3 瓶盖
        === === === === === === === === === ===
        发
        0xAA, 0xBB, 颜色标志位(药板), 颜色标志位(药瓶), 状态标志位 || 象限标志位, x坐标整数, x坐标小数, y坐标整数, y坐标小数, 0xFF
        颜色标志位: 1 red, 2 green, 3 blue
        状态标志位: 1 药板, 2 药瓶, 3 拧瓶盖
        象限标志位: 1 第一象限, 2 第二象限, 3 第三象限, 4 第四象限
        """
        if self.state == 3 and self.mode == 0:
            """
            这里的state = 3是特殊的
            刚开始按按钮4, 进行色卡识别
            这个判断仅运行一次
            """
            identify_color_cards.to_do_identify()
            self.sign_position_list = [identify_color_cards.get_first_card_colour(),
                                  identify_color_cards.get_second_card_colour(), 1]
            coordinate_list = [0, 0, 0, 0, 0]
            serial.set_sign_position_list(self.sign_position_list)
            serial.set_coordinate_list(coordinate_list)
            serial.send() # 发送信号开始执行

        elif self.state == 0 and self.mode == 1:
            """
            准备药板, 无事可做
            """
            self.sign_position_list = [identify_color_cards.get_first_card_colour(),
                                       identify_color_cards.get_second_card_colour(), 1]
            pass

        elif self.state == 1 and self.mode == 1:
            """
            此时定位到托盘上方位置, 可以开始识别药丸(停留时间5s左右)
            """
            self.__identify_the_pills__(identify_color_cards.get_first_card_colour())

        elif self.state == 2 and self.mode == 1:
            """
            完成抓取, 无事可做
            """
            pass
        elif self.state == 0 and self.mode == 2:
            """
            准备药瓶, 无事可做
            """
            self.sign_position_list = [identify_color_cards.get_first_card_colour(),
                                       identify_color_cards.get_second_card_colour(), 3]
            pass
        elif self.state == 1 and self.mode == 2:
            """
            主控控制电机定位到托盘上方位置, 开始识别药丸(停留时间5s左右)
            """
            self.__is_it_the_finals__()
            self.__identify_the_pills__(identify_color_cards.get_second_card_colour())

        elif self.state == 2 and self.mode == 2:
            """
            完成抓取, 无事可做
            """
            pass






execute = Execute(_detection_distance=detection_distance)
print("\n===begin===")
while not app.need_exit():
    img = cam.read()
    all_object_list, img = nnDetector.detect(_img=img)
    # execute.set_img(img)
    dis.show(img)
    if serial.receive():
        execute.set_state(serial.get_state())
        execute.set_mode(serial.get_mode())
        execute.perform_analysis()
