# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光
import sensor, image, time
from machine import UART
red_threshold = [(0, 50, 4, 60, 0, 60)]
#(9, 35, -9, 36, -31, 28)
blue_threshold = [(0, 60, -10, 127, -128, -10)]
green_threshold = [(24, 70, -128, -5, -128, 15)]


# 下面的阈值一般跟踪红色/绿色的东西。你可以调整它们…
manyThresholds = [(0, 100, 20, 127, -128, 127), # generic_red_thresholds -> index is 0 so code == (1 << 0)
                 (27, 80, -45, -15, 13, 51), # generic_green_thresholds -> index is 1 so code == (1 << 1)
                 (41, 78, -29, 37, -76, -26)] # generic_blue_thresholds -> index is 2 so code == (1 << 2)
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


class Movement:

    _colour = {"red":red_threshold, "green":green_threshold, "blue":blue_threshold}
    def __init__(self, colour):
        self.x = None
        self.y = None
        self.colour = self._colour[colour]

    def catch(self):
        print("catch")
        # sensor.skip_frames(time=2000)
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
        # print("\n\n")
        img.draw_cross(160, 120, color=(0, 255, 0), size=20, thickness=3)# green

        # 500-1000 色块大小
        if blobs:
            print("进入比较色块大小")
            if 500 < blobs[0].pixels() < 1000:
                print("进入500-1000")
                img.draw_cross(blobs[0].cx(), blobs[0].cy(), color=(255, 0, 255), thickness=3)
                print("X:", blobs[0].cx(), " Y:", blobs[0].cy())
                self.x = blobs[0].cx()
                self.y = blobs[0].cy()
                return self.x, self.y

            elif blobs[0].pixels() > 1000:
                print("进入>1000")
                roi = blobs[0].rect()
                # img.mean(2)             #均值滤波,均值滤波是最快的滤波,size=1则是3x3的核，size=2则是5x5的核,不应该使用大于2的值。
                img.binary(self.colour)
                img.erode(2)
                img.flood_fill(10, 10, clear_background=False)
                bright_spot = img.find_blobs([(0, 76, -128, 127, -128, 127)], area_threshold=10, margin=100, roi=roi)
                # img = sensor.snapshot().lens_corr(strength=1.5, zoom=1.0)  # 消除镜头鱼眼畸变
                if bright_spot:
                    for b in bright_spot:
                        if b.pixels() > 60:
                            continue
                        img.draw_cross(b.cx(), b.cy(), color=(255, 0, 255), thickness=3)
                        print("X:", b.cx(), " Y:", b.cy())
                        self.x = b.cx()
                        self.y = b.cy()
                        return self.x, self.y
                        # blob.cx() 返回色块的外框的中心x坐标（int），也可以通过blob[5]来获取。
                        # blob.cy() 返回色块的外框的中心y坐标（int），也可以通过blob[6]来获取。
        else: return None

while True:
    print("-----------begin----------")
    movement = Movement("red")
    movement.catch()
    print("==========================end==========================\n\n\n")