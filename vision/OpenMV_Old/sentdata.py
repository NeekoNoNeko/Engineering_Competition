# Untitled - By: sonkin - Tue Aug 27 2024
from machine import UART
import sensor, image, time


uart = UART(3, 19200)


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

def usart_send():

    data = bytearray([0xAA, 0xBB, 0xFF])# 帧头，帧头，颜色标志位，状态标志位，X坐标，Y坐标，帧尾
    uart.write(data)
    print("hello")



while(True):
    clock.tick()
    img = sensor.snapshot()
#    print(clock.fps())
    usart_send()










