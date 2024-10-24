from maix import image, camera, display, nn

detector = nn.YOLOv5(model="/root/models/maixhub/147350/model_147350.mud", dual_buff = True)
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
dx = detector.input_width()//2
dy = detector.input_height()//2
dis = display.Display()
print("dx:{},dy:{}".format(dx,dy))
k = 2.6
# 根据色块颜色选择对应配置
thresholds = [[0, 80, 40, 80, 10, 80]]      # red
# thresholds = [[0, 80, -120, -10, 0, 30]]    # green
# thresholds = [[0, 80, 30, 100, -120, -60]]  # blue

while 1:
    img = cam.read().lens_corr(strength=1.5)
    img.draw_cross(x=dx, y=dy, color=image.Color.from_rgb(0, 255, 0), size=50, thickness=2)
    blobs = img.find_blobs(thresholds, pixels_threshold=50)
    for blob in blobs:
        _x = int(blob.x()+blob.w()/2)
        _y = int(blob.y()+blob.h()/2)
        img.draw_cross(x=_x, y=_y, color=image.Color.from_rgb(0, 0, 255), size=5, thickness=3)
        # img.draw_rect(blob[0], blob[1], blob[2], blob[3], image.COLOR_GREEN)
        # img.draw_string(blob.x(), blob.y(), "w:{}, h:{}".format(blob.w(), blob.h()), image.Color.from_rgb(0,255,0), scale=2)
    dis.show(img)
