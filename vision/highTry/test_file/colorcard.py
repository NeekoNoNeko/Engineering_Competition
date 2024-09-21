# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光

import sensor, image, time, pyb, math
from machine import UART


red_threshold = [(10, 50, 10, 54, 4, 52)]
(10, 50, 10, 54, 4, 52)
(16, 81, 15, 61, 0, 61)
(22, 44, 33, 66, 9, 52)
blue_threshold = [(17, 58, -20, 30, -66, -7)]
green_threshold = [(38, 77, -59, -15, -5, 36)]
(38, 77, -59, -15, -5, 36)
(36, 64, -60, -14, 0, 36)
(36, 64, -48, -15, -5, 36)

(27, 70, -63, -23, 2, 69)
(27, 70, -55, -14, 0, 35)
(39, 73, -56, -30, -9, 21)

# 下面的阈值一般跟踪红色/绿色的东西。你可以调整它们…
# red:001, green:010, blue:100

manyThresholds = [(33, 74, 7, 35, 12, 52), # generic_red_thresholds -> index is 0 so code == (1 << 0)
                 (19, 100, -59, 3, 6, 61), # generic_green_thresholds -> index is 1 so code == (1 << 1)
                 (0, 100, -46, 21, -53, -16)] # generic_blue_thresholds -> index is 2 so code == (1 << 2)
# 当“find_blobs”的“merge = True”时，code代码被组合在一起。

middle = (160, 120)
K = 0.5767220
uartAddr = UART(3, 9600)
send_flag = True

#pyb.delay(5000)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False)                         #关闭白平衡
sensor.set_contrast(3)      # 设置相机图像对比度。-3至+3。
sensor.set_brightness(3)   # 设置相机图像亮度。-3至+3。
sensor.set_saturation(3)   # 设置相机图像饱和度。-3至+3。
sensor.skip_frames(time = 2000)

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
            pass
#            pyb.delay(5000)
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


icard = IdentifyColorCards()
while True:
    img = sensor.snapshot().lens_corr(strength=1.5, zoom=1.0)  # 消除镜头鱼眼畸变
    i = icard.find()
#    movement = Movement("green")
#    val = movement.catch()
#    print(val)
