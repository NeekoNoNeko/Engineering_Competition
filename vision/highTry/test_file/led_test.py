
# Main Module Example
#
# 当OpenMV摄像头从电脑断开时，它会运行SD卡上的main.py脚本(如果插了内存卡)或你的OpenMV摄像头内部Flash里的main.py脚本。


import time, pyb

#将蓝灯赋值给变量led
led = pyb.LED(3) # Red LED = 1, Green LED = 2, Blue LED = 3, IR LEDs = 4.
usb = pyb.USB_VCP() # This is a serial port object that allows you to
# communciate with your computer. While it is not open the code below runs.


#如果openmv未连接到电脑，蓝灯亮150ms，延时100ms，亮150ms，延时600ms，循环。
while(not usb.isconnected()):
    led.on()            #亮灯
    time.sleep_ms(150)     #延时150ms
    led.off()           #暗灯
    time.sleep_ms(100)
    led.on()
    time.sleep_ms(150)
    led.off()
    time.sleep_ms(600)

#变量led此时代表绿灯
led = pyb.LED(3) # 切换到使用绿色led。

#如果openmv已连接到电脑
while(usb.isconnected()):
    led.on()
    time.sleep_ms(150)
    led.off()
    time.sleep_ms(100)
    led.on()
    time.sleep_ms(150)
    led.off()
    time.sleep_ms(600)
