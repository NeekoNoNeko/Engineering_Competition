# Ulab is a numpy-like module for micropython, meant to simplify and speed up common
# mathematical operations on arrays. This basic example shows mean/std on an image.
# Ulab是micropython的一个类似于numpy的模块，用于简化和加速对数组的常见数学操作。
# 这个基本的例子显示了图像上的平均值/std。
#
# NOTE: ndarrays cause the heap to be fragmented easily. If you run out of memory,
# there's not much that can be done about it, lowering the resolution might help.
# 注意:ndarrays会导致堆很容易被分割。如果你的内存用完了，
# 那就没办法了，降低分辨率可能会有帮助。

import sensor, image, time
import ulab as np

sensor.reset()                      # 复位并初始化传感器

sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种

sensor.set_framesize(sensor.QQVGA)   # 将图像大小设置为 (320x240)
clock = time.clock()                 # 创建一个时钟对象来跟踪FPS帧率。

while (True):
    img = sensor.snapshot()         # 拍一张照片并返回图像
    img = np.numpy.array(img, dtype=np.numpy.uint8)
    print(img)
