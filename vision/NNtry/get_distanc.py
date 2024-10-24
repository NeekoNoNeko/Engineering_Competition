#/tmp/maixpy_run/ 工作目录
from maix import camera, display, nn, app
import sys, math

sys.path.append(r'/root/neeko')
from NNDetector import NNDetector
from SERIAL_IO import SerialIO
from IdentifyColorCards import IdentifyColorCards

dis = display.Display()
serial = SerialIO()
identify_color_cards = IdentifyColorCards(_is_it_card_colour_by_hand=True)

#需要修改的参数
"""=================================================================================================================="""
identify_color_cards.set_card_colour_list([0, 1])           # 色卡顺序 测试时修改 0:red 1:blue 2:green
detection_distance = 5                                      # 距离数值, 用来检测是否重复小球
strength = 1.7                                              # 消除镜头畸变, 调整strength的值直到画面不再畸变
model_path = "/root/models/maixhub/147350/model_147350.mud" # 模型位置
serial.set_k_value(2.9083)
serial.set_middle((224, 224))
"""=================================================================================================================="""

all_object_list = []
detector = nn.YOLOv5(model=model_path, dual_buff = True)
nnDetector = NNDetector(_detector=detector)
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
while True:
    img = cam.read().lens_corr(strength=strength)
    position_list, img = nnDetector.detect(_img=img, colour_number=0)
    print("\n\n\nposition_list:", position_list, "\n\n")
    dis.show(img)
    for position in position_list:
        sign_position_list = [1, 1, 1]
        serial.set_sign_position_list(sign_position_list)
        serial.set_sign_position_list(sign_position_list)
        serial.send(_position=position)