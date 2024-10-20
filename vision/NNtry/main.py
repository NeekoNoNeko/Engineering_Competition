#/tmp/maixpy_run/ 工作目录
from maix import camera, display, image, nn, app
import sys
sys.path.append(r'/root/neeko')
from NNDetector import NNDetector

detector = nn.YOLOv5(model="/root/models/maixhub/147350/model_147350.mud", dual_buff = True)
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
dis = display.Display()

nnDetector = NNDetector(_detector=detector, _cam=cam)
while not app.need_exit():
    _, img = nnDetector.detect(colour_number=0) # 测试时修改 0:red 1:blue 2:green
    dis.show(img)