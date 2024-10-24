# 多颜色跟踪示例
#
# 这个例子显示了使用OpenMV的多色跟踪。

import sensor, image, time, math

# 颜色跟踪阈值(L Min, L Max, A Min, A Max, B Min, B Max)
# 下面的阈值跟踪一般红色/绿色的东西。你不妨调整他们...
thresholds = [(30, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (19, 73, -14, 52, -86, -39)] # generic_blue_thresholds
# 您最多可以传递16个阈值。
# 但是，在颜色阈值开始重叠之前，实际上不可能使用16个阈值对任何场景进行分段。
sensor.reset()
#初始化摄像头，reset()是sensor模块里面的函数

sensor.set_pixformat(sensor.RGB565)
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种

sensor.set_framesize(sensor.QVGA)
#设置图像像素大小

sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False) # 颜色跟踪必须关闭白平衡
clock = time.clock()

# 只有比“pixel_threshold”多的像素和多于“area_threshold”的区域才被
# 下面的“find_blobs”返回。 如果更改相机分辨率，
# 请更改“pixels_threshold”和“area_threshold”。 “merge = True”合并图像中所有重叠的色块。

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(thresholds, pixels_threshold=100, area_threshold=100, merge = False):
        # These values depend on the blob not being circular - otherwise they will be shaky.
#        if blob.elongation() > 0.5:
#            img.draw_edges(blob.min_corners(), color=(255,0,0))
#            img.draw_line(blob.major_axis_line(), color=(0,255,0))
#            img.draw_line(blob.minor_axis_line(), color=(0,0,255))

        # 这些值始终是稳定的。
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # 注意-色块rotation仅在0-180范围内唯一。
#        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
    print(clock.fps())
