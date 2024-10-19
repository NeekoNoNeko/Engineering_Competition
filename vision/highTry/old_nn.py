import ml
from ml.utils import NMS
import sensor, image, time, pyb, math
from machine import UART

red_threshold = [(0, 51, 36, 62, 19, 50)]
blue_threshold = [(19, 55, -8, 30, -65, -32)]
green_threshold = [(23, 57, -35, 0, -24, 14)]


# 下面的阈值一般跟踪红色/绿色的东西。你可以调整它们…
# red:001, green:010, blue:100

manyThresholds = [(0, 100, 24, 127, -10, 127), # generic_red_thresholds -> index is 0 so code == (1 << 0)
                 (1, 98, -128, -15, 16, 67), # generic_green_thresholds -> index is 1 so code == (1 << 1)
                 (0, 100, -86, 23, -82, -30)] # generic_blue_thresholds -> index is 2 so code == (1 << 2)
# 当“find_blobs”的“merge = True”时，code代码被组合在一起。

middle = (160, 120)
K = 0.5767220
uartAddr = UART(3, 9600)
send_flag = True

min_confidence = 0.4
threshold_list = [(math.ceil(min_confidence * 255), 255)]

# Load built-in model
model = ml.Model("trained")
print(model)

pyb.delay(5000)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False)                         #关闭白平衡
#sensor.set_contrast(3)      # 设置相机图像对比度。-3至+3。
#sensor.set_brightness(3)   # 设置相机图像亮度。-3至+3。
#sensor.set_saturation(3)   # 设置相机图像饱和度。-3至+3。
sensor.skip_frames(time = 2000)

colors = [  # Add more colors if you are detecting more than 7 types of classes at once.
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

class NN:

    def fomo_post_process(self, model, inputs, outputs):
        n, oh, ow, oc = model.output_shape[0]
        nms = NMS(ow, oh, inputs[0].roi)
        for i in range(oc):
            img = image.Image(outputs[0][0, :, :, i] * 255)
            blobs = img.find_blobs(
                threshold_list, x_stride=1, area_threshold=1, pixels_threshold=1
            )
            for b in blobs:
                rect = b.rect()
                x, y, w, h = rect
                score = (
                    img.get_statistics(thresholds=threshold_list, roi=rect).l_mean() / 255.0
                )
                nms.add_bounding_box(x, y, x + w, y + h, score, i)
        return nms.get_bounding_boxes()

    def get_position(self, color):
        dis = {"red": 1, "green": 2, "blue": 3}
        sensor.skip_frames(time=2000)
        img = sensor.snapshot()

        for i, detection_list in enumerate(model.predict([img], callback=self.fomo_post_process)):
            if i != dis[color]:
                continue
            if i == 0:
                continue  # background class
            if len(detection_list) == 0:
                continue  # no detections for this class?

            print("********** %s **********" % model.labels[i])

            for (x, y, w, h), score in detection_list:
                center_x = math.floor(x + (w / 2))
                center_y = math.floor(y + (h / 2))
                print(f"x {center_x}\ty {center_y}\tscore {score}")
                return center_x, center_y


class IsEmpty :
    empty_times = 0

    def count(self):
        self.empty_times += 1

    def do_analysis(self):
        if self.empty_times >= 2:
            send_colour_list = identify_color_cards.ColourCardList
            sent_uart_data = bytearray([0xAA, 0xBB, send_colour_list[0], send_colour_list[1], 3,
                                        0, 0, 0, 0, 0, 0xFF])
            # 帧头，帧头，颜色标志位1，颜色标志位2，状态标志位(position)，符号象限位，X坐标前，后，Y坐标前，后，帧尾
            print(uartAddr.write(sent_uart_data))  # 开始启动!!!
            print("sent_uart_data:", sent_uart_data)

class SendData:
    def __init__(self, x_position, y_position):

#        self.uartAddr = UART(3, 9600)
        self.relative_data = []
        self.x = x_position
        self.y = y_position

    ##得到摄像头中心与小球的真实距离
    def _make_relative_data(self):

        data_x = (self.x - middle[0]) * K
        data_y = (middle[1] - self.y) * K

        data_x *= 100
        data_y *= 100

        data_x = int(data_x)
        data_y = int(data_y)

        self.relative_data =  [data_y, data_x]#操作板与摄像头的坐标互换

    ##拆分小数点
    def __split_decimal_point(self, num):
        num = abs(num)
        left_num = int(num // 100)
        right_num = int(num % 100)

        return left_num, right_num

    def uart_send(self):

        # 将识别到的色卡顺序，发送出去
        send_colour_list = identify_color_cards.ColourCardList
        print("send_colour_list:", send_colour_list)
        # send_colour_list[0] = identify_color_cards.colour_to_code[send_colour_list[0]]
        # send_colour_list[1] = identify_color_cards.colour_to_code[send_colour_list[1]]

        self._make_relative_data()
        #quadrant符号象限位判断
        if self.relative_data[0] > 0:
            if self.relative_data[1] > 0:
                quadrant = 1
            else:
                quadrant = 4
        else:
            if self.relative_data[1] > 0:
                quadrant = 2
            else:
                quadrant = 3
    #进行拆分小数点
        x_data0, x_data1 = self.__split_decimal_point(self.relative_data[0])
        y_data0, y_data1 = self.__split_decimal_point(self.relative_data[1])
    #    print(x_data0,"  ",x_data1,"  ", y_data0,"  ", y_data1)

        #发送字节数据
        data = bytearray([0xAA, 0xBB, send_colour_list[0], send_colour_list[1], analyzeData.position,
                          quadrant,x_data0,x_data1,y_data0,y_data1, 0xFF])
    #    data = bytearray([0xAA, 0xBB, 1, 1, relative_data[0], relative_data[1], 0xFF])

        # 帧头，帧头，颜色标志位，颜色标志位2，状态标志位(position)，符号象限位，X坐标前，后，Y坐标前，后，帧尾
        print("sent data\n",data)
        print("写入的字节数： ", uartAddr.write(data))
        print(data.hex('-'))#print打印会将16进制转成对应字符
        print("sent")

class IdentifyColorCards:
    code_to_colour = {1: "red", 2: "green", 4: "blue"}
    colour_to_code = {"red": 1, "green": 2, "blue": 4}
    def __init__(self):
        self.colors = None
        self.ColourCardList = []
        # self.ColourCardList = [1, 2]

    def Get_MaxIndex(self, blobs):
        maxb_index = 0  # 最大色块索引初始化
        max_pixels = 0  # 最大像素值初始化
        for i in range(len(blobs)):  # 对N个色块进行N次遍历
            if blobs[i].pixels() > max_pixels:  # 当某个色块像素大于最大值
                max_pixels = blobs[i].pixels()  # 更新最大像素
                maxb_index = i  # 更新最大索引
                return maxb_index

    def find(self):
        if len(self.ColourCardList) == 1:
            led = pyb.LED(2)
            led.on()
            pyb.delay(5000)
            led.off()
        sensor.skip_frames(time=3000)
        img = sensor.snapshot().lens_corr(strength=1.5, zoom=1.0)  # 消除镜头鱼眼畸变
        blobs = img.find_blobs(manyThresholds, area_threshold=3000, margin=10, merge=False)
        print(blobs)
        max_blobs_index = self.Get_MaxIndex(blobs)
        print("maxBlobs_index", max_blobs_index)

        if blobs:
            b = blobs[max_blobs_index]
            print("识别到的色卡颜色: ", self.code_to_colour[b.code()])
            print("b", b)
            print("\n b.code(): ", b.code())
            if len(self.ColourCardList) == 0:
                self.ColourCardList.append(self.code_to_colour[b.code()])
            elif len(self.ColourCardList) == 1:
                self.ColourCardList.append(self.code_to_colour[b.code()])
        print(self.ColourCardList)



class AnalyzeData:
#    _uartData = None

    def __init__(self):
        self._uartData = None
        self.mode = None
        self.position = 1

    def read_uart(self):
        self._uartData = uartAddr.read()
        # a1 a2 0 0 fe
        # 写入模式
        # 去哪里位置位: 0默认，1药板，2药瓶
        if self._uartData:
            print("\n\n\n========beging_read_uart========")
            print(self._uartData)
            print(self._uartData.hex("-"))

            if self._uartData.startswith(b"\xa1", 0):
                if self._uartData.startswith(b"\xa2", 1):
                    if self._uartData.endswith(b"\xfe"):
                        self.mode = self._uartData[2]
                        temp_position = self._uartData[3]

                        if temp_position== 2 and self.position == 1: #positon转变时发送
                            self.position = self._uartData[3]
                            send_colour_list = identify_color_cards.ColourCardList
                            sent_uart_data = bytearray([0xAA, 0xBB, send_colour_list[0], send_colour_list[1], self.position,
                                                        0, 0, 0, 0, 0, 0xFF])
                            # 帧头，帧头，颜色标志位1，颜色标志位2，状态标志位(position)，符号象限位，X坐标前，后，Y坐标前，后，帧尾
                            print(uartAddr.write(sent_uart_data))  # 开始启动!!!
                            print("sent")
                            print("sent_uart_data:", sent_uart_data.hex("-"))
                        self.position = self._uartData[3]
                        print("mode: ", self.mode)
                        print("position: ", self.position)
                    else:
                        self._uartData = None
                        print("no!!!")
                else:
                    self._uartData = None
                    print("no!!!")
            else:
                self._uartData = None
                print("no!!!")
            return True
        self._uartData = None
        return False
        # print("========finish_read_uart========")
        # print("_uartData: ", self._uartData)


    def do_analyze(self):
        # 解析数据包
        if self.position == 1:
            colour_index = 0
        elif self.position == 2:
            colour_index = 1

        if self.mode == 1:
            # 做一个是否有色卡列表的判断
            # while len(identify_color_cards.ColourCardList ) < 2:
            #     print("做色卡判断")
            #     identify_color_cards.find()

            print("into do analyze")
            led.off()
            tem_colour = identify_color_cards.code_to_colour[identify_color_cards.ColourCardList[colour_index]]
            print("tem_colour: ", tem_colour)
            nn = NN()
            val = nn.get_position(tem_colour)

            print("val:", val)
            if val:
                send = SendData(val[0], val[1])
                send.uart_send()
                print("done\n\n\n")
        elif self.mode == 3:
            # 将识别到的色卡顺序，发送出去
            send_colour_list = identify_color_cards.ColourCardList
            print("send_colour_list:", send_colour_list)
            led.off()
            while len(send_colour_list) < 2:
                identify_color_cards.find()
                # identify_color_cards.find()
            print("===========end_identify_colour_card===========\n\n\n")
            # 将识别到的色卡顺序，发送出去
            # send_colour_list = identify_color_cards.ColourCardList
            print(send_colour_list)
            send_colour_list[0] = identify_color_cards.colour_to_code[send_colour_list[0]]
            send_colour_list[1] = identify_color_cards.colour_to_code[send_colour_list[1]]
            sent_uart_data = bytearray([0xAA, 0xBB, send_colour_list[0], send_colour_list[1], 1,
                                        0,0,0,0,0, 0xFF])
#            sent_uart_data = bytearray([0xAA, 0xBB, 1, 1, 1, 0,0,0,0,0, 0xFF])
                        # 帧头，帧头，颜色标志位1，颜色标志位2，状态标志位(position)，符号象限位，X坐标前，后，Y坐标前，后，帧尾
            print(uartAddr.write(sent_uart_data))# 开始启动!!!
            print("sent_uart_data:", sent_uart_data)

        # elif self.mode == 4:
        #     send_colour_list = identify_color_cards.ColourCardList
        #     sent_uart_data = bytearray([0xAA, 0xBB, send_colour_list[0], send_colour_list[1], self.position,
        #                                 0, 0, 0, 0, 0, 0xFF])
        #     # 帧头，帧头，颜色标志位1，颜色标志位2，状态标志位(position)，符号象限位，X坐标前，后，Y坐标前，后，帧尾
        #     print(uartAddr.write(sent_uart_data))  # 开始启动!!!
        #     print("sent_uart_data:", sent_uart_data.hex("-"))
        elif self.mode == 0 or self.mode == 2:
            pass


analyzeData = AnalyzeData()
identify_color_cards = IdentifyColorCards()
is_empty = IsEmpty()
print("go")
sensor.skip_frames(time=3000)
while True:
    led = pyb.LED(1)
    led.on()

    if analyzeData.read_uart():
        analyzeData.do_analyze()# 只需这个
