from maix import camera, display, image, nn, app


class NNDetector:
    def __init__(self, _detector):
        # 初始化设备用到的参数
        self.detector = _detector
        # self.dis = _dis

    # 进行检测函数
    def detect(self, colour_number, _img):
        _position_list = [] # 存放 所有 目标 小球中心位置的列表
        target_obj_list = [] # 存放 所有 目标 小球的object的列表
        # _img = self.cam.read() # 读取图像

        objs = self.detector.detect(img=_img, conf_th=0.5, iou_th=0.45) # 进行检测获得 所有 小球的object (type:list)

        # 读取所有小球的object, 提取出target_obj_list
        for obj in objs:
            if obj.class_id == colour_number:
                target_obj_list.append(obj)

            if obj.class_id == 0:
                _img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
            elif obj.class_id == 1:
                _img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_BLUE)
            elif obj.class_id == 2:
                _img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_GREEN)

        # 读取目标 小球的object的列表提取出中心位置position_list
        for obj in target_obj_list:
            position_x = obj.x + obj.w/2
            position_y = obj.y + obj.h/2
            _position_list.append((position_x, position_y)) # tuple

        print("position_list:", _position_list)
        return _position_list, _img # 返回中心位置列表和图像


if __name__ == '__main__':
    detector = nn.YOLOv5(model="/root/models/maixhub/147350/model_147350.mud", dual_buff = True)
    cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
    dis = display.Display()

    nnDetector = NNDetector(_detector=detector)
    while not app.need_exit():
        img = cam.read()
        position_list, img = nnDetector.detect(colour_number=0, _img=img) # 测试时修改 0:red 1:blue 2:green
        dis.show(img)


