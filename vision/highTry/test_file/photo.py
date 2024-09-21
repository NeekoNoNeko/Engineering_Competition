# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光
import sensor, image, time
from machine import UART
red_threshold = [(19, 36, 1, 53, -9, 51)]
blue_threshold = [(9, 42, -28, 27, -54, -1)]
green_threshold = [(28, 60, -59, -16, -11, 74)]


# 下面的阈值一般跟踪红色/绿色的东西。你可以调整它们…
manyThresholds = [(0, 100, 6, 68, 12, 65), #  Red generic_red_thresholds -> index is 0 so code == (1 << 0)
                 (0, 100, -65, -16, 13, 56), # Green generic_green_thresholds -> index is 1 so code == (1 << 1)
                 (0, 99, -40, -6, -53, 2) ] # Blue generic_blue_thresholds -> index is 2 so code == (1 << 2)
# 当“find_blobs”的“merge = True”时，code代码被组合在一起。
middle = (160, 120)
K = 0.5767220
uartAddr = UART(3, 9600)
send_flag = True

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False)    # 白平衡
sensor.set_auto_exposure(False)#    自动曝光
sensor.set_contrast(3)      # 设置相机图像对比度。-3至+3。
sensor.set_brightness(3)   # 设置相机图像亮度。-3至+3。
sensor.set_saturation(3)   # 设置相机图像饱和度。-3至+3。

sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
#    print("-----------begin----------")
    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变
#    img.gaussian(2)
#    img.binary(green_threshold)
#    img.erode(1)
#    img.flood_fill(10, 10, clear_background=False)
#    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变
#    img.dilate(1)
