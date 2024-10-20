# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光
import sensor, image, time
from machine import UART
red_threshold = [(0, 66, 14, 127, 12, 66)]
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

clock = time.clock()

while(True):
    print("-----------begin----------")
    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变
    blobs = img.find_blobs(red_threshold, area_threshold=300, margin=10)# type(blob) is list
#    print(blobs)
    print("blobs数量:", len(blobs))
    # 寻找对应阈值的色块，阈值小于300像素的色块过滤掉，合并相邻像素在10个像素内的色块

    for b in blobs:
        print(b.pixels())
        print(b.compactness())
        img.draw_rectangle(b.rect())
        img.draw_cross(b.cx(), b.cy())
        img.draw_line((159, 120, b[5], b[6]), color=(0, 0, 0), thickness=2)# color is black
    # print("\n\n")
    img.draw_cross(160, 120, color=(0, 255, 0), size=20, thickness=3)# green
    print("==========================end==========================\n\n\n")
