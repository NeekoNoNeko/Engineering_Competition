# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光

import sensor, image, time, pyb
from machine import UART
red_threshold = [(0, 50, 4, 60, 0, 60)]
#(9, 35, -9, 36, -31, 28)
blue_threshold = [(0, 60, -10, 127, -128, -10)]
green_threshold = [(24, 70, -128, -5, -128, 15)]


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

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False)                         #关闭白平衡
sensor.skip_frames(time = 2000)


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


    #    print("has been sent")

#data = uart.read().decode()
class Movement:
#    _mode = {0 : "mode1", 1 : "mode2", 2 : "mode3"}
    _colour = {"red":red_threshold, "green":green_threshold, "blue":blue_threshold}
    def __init__(self, colour):
        self.x = None
        self.y = None
        self.colour = self._colour[colour]

    def catch(self):
        print("catch")
        sensor.skip_frames(time=3000)
        img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变
        blobs = img.find_blobs(self.colour, area_threshold=300, margin=10)# type(blob) is list
        print(blobs)
        print("blobs数量:", len(blobs))
        # 寻找对应阈值的色块，阈值小于300像素的色块过滤掉，合并相邻像素在10个像素内的色块

        for b in blobs:
            print(b.pixels())
            img.draw_rectangle(b.rect())
            img.draw_cross(b.cx(), b.cy())
            img.draw_line((159, 120, b[5], b[6]), color=(0, 0, 0), thickness=2)# color is black
        print("\n\n")
        img.draw_cross(160, 120, color=(0, 255, 0), size=20, thickness=3)# green

        # 500-1000 色块大小
        if blobs:
            print("进入比较色块大小")
            if 500 < blobs[0].pixels() < 1000:
                img.draw_cross(blobs[0].cx(), blobs[0].cy(), color=(0, 255, 0))
                print("X:", blobs[0].cx(), " Y:", blobs[0].cy())
                self.x = blobs[0].cx()
                self.y = blobs[0].cy()
                return self.x, self.y

            elif blobs[0].pixels() > 1000:
                img.mean(2)             #均值滤波,均值滤波是最快的滤波,size=1则是3x3的核，size=2则是5x5的核,不应该使用大于2的值。
                img.binary(self.colour)
                img.flood_fill(10, 10, clear_background=False)
                img.erode(2)

                bright_spot = img.find_blobs([(0, 76, -128, 127, -128, 127)], area_threshold=10, margin=100)

                img.draw_cross(bright_spot[0].cx(), bright_spot[0].cy(), color=(0, 255, 0))
                print("X:", bright_spot[0].cx(), " Y:", bright_spot[0].cy())
                self.x = bright_spot[0].cx()
                self.y = bright_spot[0].cy()
                return self.x, self.y
                # blob.cx() 返回色块的外框的中心x坐标（int），也可以通过blob[5]来获取。
                # blob.cy() 返回色块的外框的中心y坐标（int），也可以通过blob[6]来获取。
        else: return None

#         if blob:                                            #如果找到了目标颜色
#             for b in blob:
#             #迭代找到的目标颜色区域
# #                img.draw_cross(b[5], b[6],color=(255,0,0))                  #画十字 cx,cy
#
#                 img.draw_line((160, 120, b[5], b[6]), color=(0,0,255), thickness=2)
# # #                user_send(b[5], b[6])
# #                 return b[5], b[6]

class IdentifyColorCards:
    code_to_colour = {1: "red", 2: "green", 4: "blue"}
    colour_to_code = {"red": 1, "green": 2, "blue": 4}
    def __init__(self):
        self.colors = None
        self.ColourCardList = []

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
            pyb.delay(5000)
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
            print("into do analyze")
            tem_colour = identify_color_cards.code_to_colour[identify_color_cards.ColourCardList[colour_index]]
            print("tem_colour: ", tem_colour)
            movement = Movement(tem_colour)
            # movement = Movement("red")
            val = movement.catch()

            print("val:", val)
            if val:
                send = SendData(val[0], val[1])
                send.uart_send()
                print("done\n\n\n")
        elif self.mode == 3:
            # 将识别到的色卡顺序，发送出去
            send_colour_list = identify_color_cards.ColourCardList
            while len(send_colour_list) < 2:
                identify_color_cards.find()
                # identify_color_cards.find()
            print("===========end_identify_colour_card===========\n\n\n")
            # 将识别到的色卡顺序，发送出去
            # send_colour_list = identify_color_cards.ColourCardList
            print(send_colour_list)
            send_colour_list[0] = identify_color_cards.colour_to_code[send_colour_list[0]]
            send_colour_list[1] = identify_color_cards.colour_to_code[send_colour_list[1]]
            sent_uart_data = bytearray([0xAA, 0xBB, send_colour_list[0], send_colour_list[1], analyzeData.position,
                                        0,0,0,0,0, 0xFF])
                        # 帧头，帧头，颜色标志位1，颜色标志位2，状态标志位(position)，符号象限位，X坐标前，后，Y坐标前，后，帧尾
            print(uartAddr.write(sent_uart_data))# 开始启动!!!

        elif self.mode == 0 or self.mode == 2 or self.mode == 4:
            pass



analyzeData = AnalyzeData()
identify_color_cards = IdentifyColorCards()
print("go")
while True:
    if analyzeData.read_uart():
        analyzeData.do_analyze()# 只需这个


    # movement = Movement("red")
    # movement.catch()
    # identify_color_cards = IdentifyColorCards()
    # identify_color_cards.find()
    # print("looping")

print("break")
