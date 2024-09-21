# Untitled - By: sonkin - Fri Aug 30 2024
#找色块后找亮光
import sensor, image, time
from machine import UART
red_threshold = [(0, 51, 36, 62, 19, 50)]
blue_threshold = [(19, 55, -8, 30, -65, -32)]
green_threshold = [(23, 57, -35, 0, -24, 14)]


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
    img.gaussian(2)
    img.binary(green_threshold)
    img.erode(1)
    img.flood_fill(10, 10, clear_background=False)
    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变
#    img.dilate(1)
