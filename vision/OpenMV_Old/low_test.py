#高度12CM
#5417.35 垂直距离K
#27.743小球像素距离Bpix
#16mm小球直径
#0.5767220K值
#Y = kX Y：实际距离 X：像素距离

import sensor
import time
from machine import UART

uart = UART(3, 9600)
#threshold =[(44, 75, 15, 127, -9, 127)]
threshold =[(9, 27, 2, 37, -10, 21)]

relative_x : float
relative_y : float
middle = (160, 120)
K = 0.5767220


sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
sensor.set_auto_whitebal(False)                         #关闭白平衡
clock = time.clock()  # Create a clock object to track the FPS.


##得到摄像头中心与小球的真实距离
def get_relative_data(x, y):

    data_x = (x - middle[0]) * K
    data_y = (middle[1] - y) * K

    data_x *= 100
    data_y *= 100

    data_x = int(data_x)
    data_y = int(data_y)

#    print([data_y, data_x])
    return [data_y, data_x] #操作板与摄像头的坐标互换


##拆分小数点
def split_decimal_point(num):
    num = abs(num)
    left_num = int(num // 100)
    right_num = int(num % 100)

    return left_num, right_num


##使用串口发送字节数据
def usart_send(x, y):

    relative_data = get_relative_data(x, y)# 得到四位数

    #quadrant符号象限位判断
    if relative_data[0] > 0:
        if relative_data[1] > 0:
            quadrant = 1
        else:
            quadrant = 4
    else:
        if relative_data[1] > 0:
            quadrant = 2
        else:
            quadrant = 3

    #进行拆分小数点
    x_data0, x_data1 = split_decimal_point(relative_data[0])
    y_data0, y_data1 = split_decimal_point(relative_data[1])
#    print(x_data0,"  ",x_data1,"  ", y_data0,"  ", y_data1)

    #发送字节数据
    data = bytearray([0xAA, 0xBB, 1, 1, quadrant,x_data0,x_data1,y_data0,y_data1, 0xFF])
#    data = bytearray([0xAA, 0xBB, 1, 1, relative_data[0], relative_data[1], 0xFF])

    # 帧头，帧头，颜色标志位，状态标志位，符号象限位，X坐标前，后，Y坐标前，后，帧尾
    uart.write(data)
    print(data.hex('-'))#print打印会将16进制转成对应字符
#    print("has been sent")


while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变

#    img.mean(2)                                                 #中值滤波
    blob = img.find_blobs(threshold, area_threshold=400, margin=10)
    #寻找对应阈值的色块，阈值小于300像素的色块过滤掉，合并相邻像素在10个像素内的色块

    if blob:                                            #如果找到了目标颜色
        for b in blob:
        #迭代找到的目标颜色区域
            img.draw_cross(b[5], b[6])                  #画十字 cx,cy
#            blob.cx() 返回色块的外框的中心x坐标（int），也可以通过blob[5]来获取。
#            blob.cy() 返回色块的外框的中心y坐标（int），也可以通过blob[6]来获取。

            img.draw_line((160, 120, b[5], b[6]), color=(0,0,255), thickness=2)
            usart_send(b[5], b[6])

    img.draw_cross(160, 120, color=(0, 255, 0), size=20,  thickness=3)
    img.draw_arrow((160,120,210,120), color=(255,0,0))
    img.draw_arrow((160,120,160,70), color=(255,0,0))   #中心箭头，操作板方向
    img.draw_arrow((0,0,160,0), color=(255,0,0))
    img.draw_arrow((0,0,0,120), color=(255,0,0))   #原点箭头，相机方向

    img.draw_circle(0, 0, 5, color=(255,255,255),fill=True)#白色相机原点









