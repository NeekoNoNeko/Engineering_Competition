#高度12CM

import sensor
import time

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变

#    img = img.histeq(adaptive=True, clip_limit=3)

#    img.gaussian(2)
    img.mean(4)
#    img.median(1, percentile=0.5) #
#    img.midpoint(1, bias=0.5)
#    img.mode(1)
#    img.mode(1, threshold=True, offset=5, invert=True)

#    img.binary([(56, 100, 9, 127, 1, 82)])
    img.binary([(44, 75, 15, 127, -9, 127)])
#    (44, 75, 15, 127, -9, 127)

    img.erode(2)

    blobs = img.find_blobs([(30, 100, -128, 127, -128, 127)])

#    for blob in img.find_blobs(thresholds, pixels_threshold=100, area_threshold=100, merge=True):
#            i
#                img.draw_rectangle(blob.rect())
#                img.draw_cross(blob.cx(), blob.cy())
#                img.draw_string(blob.x() + 2, blob.y() + 2, "r/g")

    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    # to the IDE. The FPS should increase once disconnected.

    #对高亮部分单独识别并填充

#(29, 100, -128, 127, -128, 127)







