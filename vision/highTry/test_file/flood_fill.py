# Untitled - By: sonkin - Mon Sep 16 2024

import sensor, image, time
red_threshold = [(0, 50, 4, 60, 0, 60)]
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

while(True):
    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)
    img.binary(red_threshold)
    img.erode(2)
    img.flood_fill(10, 10, clear_background=False)
    bright_spot = img.find_blobs([(0, 76, -128, 127, -128, 127)], area_threshold=10, margin=100)
    bnum = 0
    #60
    for b in bright_spot:
        if b.pixels() > 60:
            continue
        img.draw_cross(b.cx(), b.cy(), color=(255, 0, 255), thickness=3)
        bnum += 1
    print("number: ", bnum)
    print("===============\n\n\n")
#    img.mean(1)
