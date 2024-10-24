# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor
import time

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()  # Take a picture and return the image.
    img.binary([(52, 100, 16, 55, -3, 38)])
#    img.binary([(0, 100, 11, 75, -28, 72)])
#
    img.flood_fill(0,0,invert=True)
    img.dilate(1)">
#    img.erode(2) #8 QVGA
#    img.dilate(3)

    for blob in img.find_blobs([(16, 100, -128, 127, -128, 127)]):
        img.draw_cross(blob.cx(), blob.cy(),(255, 0, 0))
    # to the IDE. The FPS should increase once disconnected.
#
