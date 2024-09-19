# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光
import sensor, image, time
from machine import UART
red_threshold = [(0, 100, 9, 127, -128, 127)]
#(9, 35, -9, 36, -31, 28)
blue_threshold = []
green_threshold = []
middle = (160, 120)
K = 0.5767220
uartAddr = UART(3, 9600)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_whitebal(False)                         #关闭白平衡
#sensor.skip_frames(time = 2000)


class SendData:
    def __init__(self, data, x_position, y_position):

#        self.uartAddr = UART(3, 9600)
        self.relative_data = []
        self.data = data
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

    def uartSend(self):

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
        data = bytearray([0xAA, 0xBB, 1, 1, quadrant,x_data0,x_data1,y_data0,y_data1, 0xFF])
    #    data = bytearray([0xAA, 0xBB, 1, 1, relative_data[0], relative_data[1], 0xFF])

        # 帧头，帧头，颜色标志位，状态标志位，符号象限位，X坐标前，后，Y坐标前，后，帧尾
        uartAddr.write(data)
        print(data.hex('-'))#print打印会将16进制转成对应字符
    #    print("has been sent")

#data = uart.read().decode()
class Movement():
#    _mode = {0 : "mode1", 1 : "mode2", 2 : "mode3"}
    _colour = {"red":"_threshold", "green":"green_threshold", "blue":"blue_threshold"}
    def __init__(self, colour):
#        self.uartAddr = UART(3, 9600)
#        self.mode = self._mode[mode]
        self.colour = self._colour[colour]

    def catch(self):
        img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变

        img.mean(1)             #均值滤波,均值滤波是最快的滤波,size=1则是3x3的核，size=2则是5x5的核,不应该使用大于2的值。
        img.binary(self.colour)
        img.erode(3)
        img.flood_fill(10, 10, clear_background=False)

        blob = img.find_blobs([(0, 76, -128, 127, -128, 127)], area_threshold=10, margin=100)
        #寻找对应阈值的色块，阈值小于300像素的色块过滤掉，合并相邻像素在10个像素内的色块

        if blob:                                            #如果找到了目标颜色
            for b in blob:
            #迭代找到的目标颜色区域
#                img.draw_cross(b[5], b[6],color=(255,0,0))                  #画十字 cx,cy

    #            blob.cx() 返回色块的外框的中心x坐标（int），也可以通过blob[5]来获取。
    #            blob.cy() 返回色块的外框的中心y坐标（int），也可以通过blob[6]来获取。

                img.draw_line((160, 120, b[5], b[6]), color=(0,0,255), thickness=2)
#                usart_send(b[5], b[6])
                return b[5], b[6]

class AnalyzeData():
#    _uartData = None

    def __init__(self):
        self._uartData = None
        self.mode = None

    def readUart(self):
        self._uartData = uartAddr.read()
        if self._uartData:
            print(self._uartData)
            print(self._uartData.hex("-"))

            if self._uartData.startswith(b"\xa1", 0):
                if self._uartData.startswith(b"\xa2", 1):
                    if self._uartData.endswith(b"\xfe"):
                        mode = self._uartData[2]
                        print(mode)
                    else:
                        print("no!!!")
                else:
                    print("no!!!")
            else:
                print("no!!!")

            self._uartData = None
            print(self._uartData)


        return True

    def doAnalyze(self):
        #解析数据包
        pass

        mode = 0

        if mode < 3:
            movement = Movement(1)
            val = movement.catch()
            if val:
                send = SendData(0, val[0], val[1])
                send.uartSend()

analyzeData = AnalyzeData()
print("go")
while(True):
    analyzeData.readUart()

#    analyzeData.doAnalyze()

print("break")
