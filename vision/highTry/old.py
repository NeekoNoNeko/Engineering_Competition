# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光

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

pyb.delay(5000)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False)                         #关闭白平衡
sensor.set_contrast(3)      # 设置相机图像对比度。-3至+3。
sensor.set_brightness(3)   # 设置相机图像亮度。-3至+3。
sensor.set_saturation(3)   # 设置相机图像饱和度。-3至+3。
sensor.skip_frames(time = 2000)

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


    #    print("has been sent")


class ClosestPair:
    point_list = []
    closest_pair_points = []

    def get_point_list(self, x):
        self.point_list = x

    def calculation(self):
        self.closest_pair_points = []
        distances, pair = self.closest_pair(self.point_list, 0, len(self.point_list) - 1)
        for i in range(2):
            self.closest_pair_points.append(pair[i])
        # self.closest_pair_points[0] = pair[0]
        # self.closest_pair_points[1] = pair[1]
        print("min distance:", distances)
        print("The closest pair is:", pair)

        # return pair



    # 定义一个函数来计算两点之间的欧几里得距离
    def dist(self,a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    # 定义一个函数来找到一组点中的最近点对
    def closest_pair(self, points, left, right):
        # 当点的数量少于等于3时，直接使用暴力方法计算最小距离
        # if right - left <= 3:
            return self.brute_force(points)

    # 合并两个子集的函数
    def merge(self, p1, p2):
        # 合并两个列表，并按照y坐标排序
        return sorted(p1 + p2, key=lambda x: x[1])

    # 找到横跨中点的最近点对的函数
    # def closest_in_strip(self, points, d_min):
    #     # 按照x坐标排序
    #     points = sorted(points, key=lambda x: x[0])
    #     d = d_min
    #     best_pair = None
    #
    #     # 遍历每个点，找到横跨中点的最近点对
    #     for i in range(len(points)):
    #         for j in range(i + 1, len(points)):
    #             if points[j][0] - points[i][0] >= d:
    #                 break
    #             if self.dist(points[i], points[j]) < d:
    #                 d = self.dist(points[i], points[j])
    #                 best_pair = (points[i], points[j])
    #
    #     return d, best_pair

    def brute_force(self, points):
        # 初始化最小距离为无穷大
        min_dist = 100000
        best_pair = None
        # 计算所有点对的距离，找出最小值
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if self.dist(points[i], points[j]) < min_dist:
                    min_dist = self.dist(points[i], points[j])
                    best_pair = (points[i], points[j])
        # 返回最小距离和最近点对
        return min_dist, best_pair

#data = uart.read().decode()
class Movement:

    _colour = {"red":red_threshold, "green":green_threshold, "blue":blue_threshold}
    def __init__(self, colour):
        self.x = None
        self.y = None
        self.colour = self._colour[colour]

    def catch(self):
        print("catch")
        closest_pair_calculation = ClosestPair()
        sensor.skip_frames(time=2000)
        img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变
        blobs = img.find_blobs(self.colour, area_threshold=300, margin=0)# type(blob) is list
        print(blobs)
        print("blobs数量:", len(blobs))
        # 寻找对应阈值的色块，阈值小于300像素的色块过滤掉，合并相邻像素在10个像素内的色块

        for b in blobs:
            print(b.pixels())
            img.draw_rectangle(b.rect())
            img.draw_cross(b.cx(), b.cy())
#            img.draw_line((159, 120, b[5], b[6]), color=(0, 0, 0), thickness=2)# color is black
        print("\n\n")
        img.draw_cross(160, 120, color=(0, 255, 0), size=20, thickness=3)# green 中心十字

        # 500-1000 色块大小
        if blobs:
#            img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变
            print("进入比较色块大小")
            if 100 < blobs[0].pixels() < 800:
                print("进入500-800")
                img.draw_cross(blobs[0].cx(), blobs[0].cy(), color=(255, 0, 255), thickness=3)
                print("X:", blobs[0].cx(), " Y:", blobs[0].cy())
                self.x = blobs[0].cx()
                self.y = blobs[0].cy()
                return self.x, self.y

            elif blobs[0].pixels() > 800:
                print("进入>800")
                roi = blobs[0].rect()

#                img.mean(1)             #均值滤波,均值滤波是最快的滤波,size=1则是3x3的核，size=2则是5x5的核,不应该使用大于2的值。
                img.gaussian(2)
                img.binary(self.colour)
#                img.gaussian(2)
                img.erode(1)
                img.flood_fill(10, 10, clear_background=False)
#                img.dilate(1)
                bright_spot = img.find_blobs([(0, 80, -128, 127, -128, 127)], area_threshold=10, margin=0, roi=roi)
                img.draw_rectangle(roi, color=(0, 50, 255))  # 青色矩形
#                img = sensor.snapshot().lens_corr(strength=1.5, zoom=1.0)  # 消除镜头鱼眼畸变
                print("1len bright_spot:", len(bright_spot))


                if len(bright_spot) > 2:
                    print("if len >2")
                    temp_point_list = []
                    for b in bright_spot:
                        temp_point = (b.cx(), b.cy())
                        temp_point_list.append(temp_point)
                        print("temp_point:", temp_point)
                        print("1(b.cx(), b.cy())", (b.cx(), b.cy()))
                        print("bpixels: ", b.pixels())
                    closest_pair_calculation.get_point_list(temp_point_list)
                    print("temp_point_list:", temp_point_list)
                    print("point_list:", closest_pair_calculation.point_list)
                    closest_pair_calculation.calculation()
                    pair_point = closest_pair_calculation.closest_pair_points
#                    closest_pair_calculation.closest_pair_points = []

                    print("2pair_point:", pair_point)
                    for b in bright_spot:
                        print("ready to move")
                        print("(b.cx(), b.cy()): ", (b.cx(), b.cy()))
                        if (b.cx(), b.cy()) in pair_point:
                            img.draw_cross(b.cx(), b.cy(), color=(255, 0, 0), thickness=2) # 红色叉
                            print("remove1")
                            bright_spot.remove(b)
                            print("remove:", (b.cx(), b.cy()))


                if bright_spot:
                    print("3bright_spot:", bright_spot)
                    print("2len bright_spot:", len(bright_spot))
                    for b in bright_spot:
                        print("b_pixels: ", b.pixels())
#                        if b.pixels() > max_pixels:
#                            print("large pixel:", b.pixels())
#                            continue
#                        img.draw_cross(b.cx(), b.cy(), color=(255, 0, 255), thickness=3)
                        img.draw_rectangle(b.rect(), color=(0,255,255)) # 青色矩形
                        print("X:", b.cx(), " Y:", b.cy())
                        self.x = b.cx()
                        self.y = b.cy()
                        return self.x, self.y
                        # blob.cx() 返回色块的外框的中心x坐标（int），也可以通过blob[5]来获取。
                        # blob.cy() 返回色块的外框的中心y坐标（int），也可以通过blob[6]来获取。
#                img.draw_cross(bright_spot[0].cx(), bright_spot[0].cy(), color=(0, 255, 0))
#                print("X:", bright_spot[0].cx(), " Y:", bright_spot[0].cy())
#                self.x = bright_spot[0].cx()
#                self.y = bright_spot[0].cy()
#                return self.x, self.y
        elif analyzeData == 2:
            is_empty.count()
            is_empty.do_analysis()
            return None

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

while True:
    led = pyb.LED(1)
    led.on()
    if analyzeData.read_uart():
        analyzeData.do_analyze()# 只需这个


    # movement = Movement("red")
    # movement.catch()
    # identify_color_cards = IdentifyColorCards()
    # identify_color_cards.find()
    # print("looping")

print("break")
