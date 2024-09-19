# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光

import sensor, image, time, pyb, math
from machine import UART

from vision.highTry.test_file.ClosestPair import closest_pair

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

pyb.delay(5000)

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


class ClosestPair:
    point_list = []

    def get_point_list(self, x):
        self.point_list.append(x)

    def calculation(self):
        distances, pair = self.closest_pair(self.point_list, 0, len(self.point_list) - 1)
        print("min distance:", distances)
        print("The closest pair is:", pair)
        return pair

    # 定义一个函数来计算两点之间的欧几里得距离
    def dist(self,a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    # 定义一个函数来找到一组点中的最近点对
    def closest_pair(self, points, left, right):
        # 当点的数量少于等于3时，直接使用暴力方法计算最小距离
        if right - left <= 3:
            return self.brute_force(points[left:right + 1])

        # 找到中点，将点集分成两部分
        mid = (left + right) // 2
        p1 = points[left:mid + 1]
        p2 = points[mid + 1:right + 1]

        # 递归地在两个子集中找到最近点对
        d1, pair1 = self.closest_pair(points, left, mid)
        d2, pair2 = self.closest_pair(points, mid + 1, right)
        d_min = min(d1, d2)
        best_pair = pair1 if d1 <= d2 else pair2

        # 合并两个子集，并找到横跨中点的最近点对
        merge_points = self.merge(p1, p2)
        d_strip, strip_pair = self.closest_in_strip(merge_points, d_min)
        if d_strip < d_min:
            d_min = d_strip
            best_pair = strip_pair

        return d_min, best_pair

    # 合并两个子集的函数
    def merge(self, p1, p2):
        # 合并两个列表，并按照y坐标排序
        return sorted(p1 + p2, key=lambda x: x[1])

    # 找到横跨中点的最近点对的函数
    def closest_in_strip(self, points, d_min):
        # 按照x坐标排序
        points = sorted(points, key=lambda x: x[0])
        d = d_min
        best_pair = None

        # 遍历每个点，找到横跨中点的最近点对
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if points[j][0] - points[i][0] >= d:
                    break
                if self.dist(points[i], points[j]) < d:
                    d = self.dist(points[i], points[j])
                    best_pair = (points[i], points[j])

        return d, best_pair

    def brute_force(self, points):
        # 初始化最小距离为无穷大
        min_dist = math.inf
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
#    _mode = {0 : "mode1", 1 : "mode2", 2 : "mode3"}
    _colour = {"red":red_threshold, "green":green_threshold, "blue":blue_threshold}
    def __init__(self, colour):
        self.x = None
        self.y = None
        self.colour = self._colour[colour]

    def catch(self):
        print("catch")
        closest_pair_calculation = ClosestPair()
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
                for b in bright_spot:
                    closest_pair_calculation.get_point_list( (b.x(), b.y()) )
                closest_pair_calculation.calculation()

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
        # self.ColourCardList = []
        self.ColourCardList = [1, 2]

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
            # 做一个是否有色卡列表的判断
            # while len(identify_color_cards.ColourCardList ) < 2:
            #     print("做色卡判断")
            #     identify_color_cards.find()

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
            sent_uart_data = bytearray([0xAA, 0xBB, send_colour_list[0], send_colour_list[1], 1,
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
