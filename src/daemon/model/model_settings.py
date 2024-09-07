from ultralytics import YOLO


# Список возможных классов
CLASSES = {
    1: 'трещина',
    2: 'потертость',
    3: 'все_гуд'
}

PATH_TO_WEIGHTS = './daemon/model/weights/best.pt'
model = YOLO(PATH_TO_WEIGHTS)
