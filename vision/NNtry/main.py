#/tmp/maixpy_run/ 工作目录
from xml.sax import parse

from maix import camera, display, image, nn, app
import sys, math

sys.path.append(r'/root/neeko')
from NNDetector import NNDetector
from SERIAL_IO import SerialIO
from IdentifyColorCards import IdentifyColorCards

detector = nn.YOLOv5(model="/root/models/maixhub/147350/model_147350.mud", dual_buff = True)
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
dis = display.Display()
nnDetector = NNDetector(_detector=detector, _cam=cam)
serial = SerialIO()
identify_color_cards = IdentifyColorCards(_is_it_card_colour_by_hand=True)

#需要修改的参数
"""=================================================================================================================="""
identify_color_cards.set_card_colour_list([0, 1]) # 测试时修改 0:red 1:blue 2:green
"""=================================================================================================================="""

class Execute:
    def __init__(self):
        self.state = None
        self.mode = None
        self.img = None
        self.duplicate_counting_list = []

    def set_state(self, _state):
        self.state = _state
        print("The current state is:", self.state)

    def set_mode(self, _mode):
        self.mode = _mode
        print("The current mode is:", self.mode)

    def set_img(self, _img):
        self.img = _img

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
            sign_position_list = [identify_color_cards.get_first_card_colour(),
                                  identify_color_cards.get_second_card_colour(), 1]
            coordinate_list = [0, 0, 0, 0, 0]
            serial.set_sign_position_list(sign_position_list)
            serial.set_coordinate_list(coordinate_list)
            serial.send() # 发送信号开始执行
        elif self.state == 1 and self.mode == 1:
            """
            此时定位到托盘上方位置, 可以开始识别药丸(停留时间5s左右)
            """
            position_list, self.img = nnDetector.detect(colour_number=identify_color_cards.get_first_card_colour(), _img=self.img)
            for position in position_list:
                if self.duplicate_counting_list:
########################################################################################################################
                    if math.dist(position, self.duplicate_counting_list) < 5: # 修改这个值
########################################################################################################################






execute = Execute()
while not app.need_exit():
    img = cam.read()
    if serial.receive():
        execute.state(serial.get_state())
        execute.set_mode(serial.get_mode())
        execute.perform_analysis()
