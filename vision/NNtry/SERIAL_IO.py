from maix import uart
from struct import pack, unpack


class SerialIO:
    def __init__(self):
        self.device = "/dev/ttyS0" # ports = uart.list_devices() # 列出当前可用的串口
        self.serial = uart.UART(self.device, 9600)
        self.K = 2.9083
        self.middle = (224, 224)

        self.sign_position_list = None
        self.coordinate_list = None

        self.state = None
        self.mode = None

    def set_sign_position_list(self, _sign_position_list):
        self.sign_position_list = _sign_position_list

    def set_coordinate_list(self, _coordinate_list):
        self.coordinate_list = _coordinate_list

    def set_k_value(self, _k):
        self.K = _k

    def set_middle(self, _middle):
        self.middle = _middle



    # 拆分小数点
    @staticmethod
    def __split_decimal_point__(_num):
        num = abs(_num)
        left_num = int(num // 100)
        right_num = int(num % 100)
        return left_num, right_num


    def send(self, _position=None):
        """
        0xAA, 0xBB, 颜色标志位(药板), 颜色标志位(药瓶), 状态标志位 || 象限标志位, x坐标整数, x坐标小数, y坐标整数, y坐标小数, 0xFF
        颜色标志位: 1 red, 2 green, 3 blue
        状态标志位: 1 药板, 2 药瓶, 3 拧瓶盖
        象限标志位: 1 第一象限, 2 第二象限, 3 第三象限, 4 第四象限
        """
        bytes_content = b'\xAA\xBB'
        if _position is None:
            bytes_content += pack("<8B", self.sign_position_list[0], self.sign_position_list[1], self.sign_position_list[2],
                                        self.coordinate_list[0], self.coordinate_list[1], self.coordinate_list[2],
                                        self.coordinate_list[3], self.coordinate_list[4])
            print(
                "aa-bb-颜色标志位(药板):{}-颜色标志位(药瓶):{}-状态标志位:{}-象限标志位:{}-x坐标整数:{}-x坐标小数:{}-y坐标整数:{}-y坐标小数:{}-ff".format(self.sign_position_list[0],
                self.sign_position_list[1], self.sign_position_list[2], self.coordinate_list[0], self.coordinate_list[1],
                self.coordinate_list[2], self.coordinate_list[3], self.coordinate_list[4]))
        else:
            # 得到摄像头中心与小球的真实距离
            position = [None, None]
            position[0] = int((_position[0] - self.middle[0]) * self.K * 100)
            position[1] = int((self.middle[1] - _position[1]) * self.K * 100)

            # quadrant符号象限位判断
            if position[0] > 0:
                if position[1] > 0:
                    quadrant = 1
                else:
                    quadrant = 4
            else:
                if position[1] > 0:
                    quadrant = 2
                else:
                    quadrant = 3

            x_left, x_right = self.__split_decimal_point__(_num=_position[0])
            y_left, y_right = self.__split_decimal_point__(_num=_position[1])

            bytes_content += pack("<8B", self.sign_position_list[0], self.sign_position_list[1], self.sign_position_list[2],
                                        quadrant, x_left, x_right, y_left, y_right)
            print(
                "aa-bb-颜色标志位(药板):{}-颜色标志位(药瓶):{}-状态标志位:{}-象限标志位:{}-x坐标整数:{}-x坐标小数:{}-y坐标整数:{}-y坐标小数:{}-ff".format(self.sign_position_list[0],
                self.sign_position_list[1], self.sign_position_list[2], quadrant, x_left, x_right, y_left, y_right))

        bytes_content += b'\xFF'
        print("send: ", bytes_content.hex("-"))
        self.serial.write(bytes_content)
        self.sign_position_list = None
        self.coordinate_list = None

    def receive(self):
        """
        数据包格式: 0xA1,0xA2,状态位,模式位,0xFE
        状态位: 0 默认位,1 到位准备抓取,2 完成抓取
        模式位: 0 默认位,1 药板,2 药瓶,3 瓶盖
        """
        self.state = None # 清空上一次数据
        self.mode = None

        data = self.serial.read()
        if data:
            print("\nreceive: ", data) # b'\xa1\xa2\x03\x01\xfe'
            
            unpackaged_data = unpack("<ccBBc", data) # type = tuple
            if unpackaged_data[0] == b"\xa1":
                if unpackaged_data[1] == b"\xa2":
                    if unpackaged_data[4] == b"\xfe":
                        self.state = unpackaged_data[2]
                        self.mode = unpackaged_data[3]
                        return True

                    else: print("missing data")
                else: print("missing data")
            else: print("missing data")
            return None

    def get_state(self):
        print("state: ", self.state)
        return self.state

    def get_mode(self):
        print("mode: ", self.mode)
        return self.mode


if __name__ == "__main__":
    sign_position_list = [1, 1 ,1]
    coordinate_list = [0, 0, 0, 0, 0]

    serial = SerialIO()
    serial.set_sign_position_list(sign_position_list)
    serial.set_coordinate_list(coordinate_list)
    serial.send()

    print("\nsend twice:")
    serial.set_sign_position_list(sign_position_list)
    serial.send((12, 34))

    while True:
        if serial.receive():
            state = serial.get_state()
            mode = serial.get_mode()