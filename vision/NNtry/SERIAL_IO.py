from maix import uart, time
from struct import pack, unpack


class SerialIO:
    def __init__(self, _sign_position_list, _coordinate_list):
        self.device = "/dev/ttyS0" # ports = uart.list_devices() # 列出当前可用的串口
        self.serial = uart.UART(self.device, 9600)

        self.sign_position_list = _sign_position_list
        self.coordinate_list = _coordinate_list

        self.state = None
        self.mode = None

    def send(self):
        """
        0xAA, 0xBB, 颜色标志位(药板), 颜色标志位(药瓶), 状态标志位 || 象限标志位, x坐标整数, x坐标小数, y坐标整数, y坐标小数, 0xFF
        颜色标志位: 1 red, 2 green, 3 blue
        状态标志位: 1 药板, 2 药瓶, 3 拧瓶盖
        象限标志位: 1 第一象限, 2 第二象限, 3 第三象限, 4 第四象限
        """
        bytes_content = b'\xAA\xBB'
        bytes_content += pack("<8B", self.sign_position_list[0], self.sign_position_list[1], self.sign_position_list[2],
                                    self.coordinate_list[0], self.coordinate_list[1], self.coordinate_list[2],
                                    self.coordinate_list[3], self.coordinate_list[4])
        bytes_content += b'\xFF'
        print(bytes_content.hex("-"))
        self.serial.write(bytes_content)

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
            print("\ndata: ", data) # b'\xa1\xa2\x03\x01\xfe'
            
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

    ser = SerialIO(_sign_position_list=sign_position_list, _coordinate_list=coordinate_list)
    ser.send()

    while True:
        if ser.receive():
            state = ser.get_state()
            mode = ser.get_mode()