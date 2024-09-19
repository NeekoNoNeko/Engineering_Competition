#高度12CM
#5417.35 垂直距离K
#27.743小球像素距离Bpix
#16mm小球直径
#0.5767220K值
#Y = kX Y：实际距离 X：像素距离

import sensor
import time
from ulab import numpy as np
from machine import UART

uart = UART(3, 19200)
threshold = (0, 100, 17, 127, 1, 127)
relative_x : float
relative_y : float
middle = (160, 120)
K = 0.5767220

np.set_printoptions(threshold=10, edgeitems=3)    #调整打印格式


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



#定义了 Solution 类中的一个方法 updateMatrix，它接受一个二维列表 matrix 作为参数，并返回一个同样大小的二维列表 dist。
class Solution:
    def updateMatrix(self, matrix):
        m, n = len(matrix), len(matrix[0])   #获取输入矩阵的行数和列数，分别存储在变量 m 和 n 中
#        dist = [[0] * n for _ in range(m)]  #创建一个与输入矩阵同样大小的二维列表 dist，初始化所有元素为0。
        dist = np.empty(matrix.shape)
        zeroes_pos = [(i, j) for i in range(m) for j in range(n) if matrix[i][j] == 0]
        # 将所有的 0 添加进初始队列中,使用列表推导式找出矩阵中所有值为0的元素的位置，并存储在列表 zeroes_pos 中。
        print("yes")

        q = zeroes_pos[:]#将 zeroes_pos 中的元素添加到 collections.deque 对象 q 中，这是一个双端队列，用于实现广度优先搜索。
        seen = set(zeroes_pos)  #将 zeroes_pos 中的元素添加到集合 seen 中，用于记录已经访问过的元素。

        # 广度优先搜索
        while q:         #开始一个循环，只要队列 q 中还有元素，就继续执行循环。
            i, j = q.pop(0) #从队列 q 中弹出（即移除并返回）第一个元素，即当前要处理的元素的行索引 i 和列索引 j。
            for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]: #对当前元素的四个相邻元素（上、下、左、右）进行遍历。
                if 0 <= ni < m and 0 <= nj < n and (ni, nj) not in seen:  #检查相邻元素是否在矩阵范围内，并且是否尚未被访问过。
                    dist[ni][nj] = dist[i][j] + 1   #如果满足条件，将该相邻元素在 dist 矩阵中对应的值设置为当前元素的 dist 值加1，表示从最近的0到这个位置的距离。
                    q.append((ni, nj))    #将满足条件的相邻元素添加到队列 q 的末尾，以便后续处理。
                    seen.add((ni, nj))   #将新访问的元素添加到 seen 集合中，以避免重复访问。

        return dist  #在所有元素都被处理后，返回最终的 dist 矩阵。



#while True:
for i in range(3):

    clock.tick()  # Update the FPS clock.

    img = sensor.snapshot().lens_corr(strength = 1.5, zoom = 1.0)# 消除镜头鱼眼畸变
    img.mean(2)                                                #中值滤波

    img.binary([threshold])
    #寻找对应阈值的色块，阈值小于300像素的色块过滤掉，合并相邻像素在10个像素内的色块


    img =np.array(img, dtype=np.uint8) #图像转换为矩阵


    #遍历矩阵，使255改为1
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] == 0:
                pass
            else:
                img[i, j] = 1

    solutions = Solution()

    # 计算距离矩阵
    distance_matrix = solutions.updateMatrix(img)
    distance_matrix = np.array(distance_matrix, dtype=np.uint8)
    print(distance_matrix)

    print(img)
#    print(type(img))
    np.ndinfo(img)
    print("______________")

#    print(img)
























