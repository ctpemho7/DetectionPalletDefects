from pydantic import BaseModel
from typing import List
import random
from PIL import Image
from io import BytesIO

from model.model_settings import model



class BoxResponse(BaseModel):
    class_name: str  # Название класса дефекта
    class_id: int    # Идентификатор класса дефекта
    x: float           # Координата X верхнего левого угла области дефекта
    y: float           # Координата Y верхнего левого угла области дефекта
    h: float           # Высота области дефекта
    w: float           # Ширина области дефекта

class InferenceResponse(BaseModel):
    class_name: str             # Название класса дефекта
    class_id: int               # Идентификатор класса дефекта
    boxes: List[BoxResponse]    # Список со всеми bounding boxes



# Функция для генерации случайного класса
def infer_defect(image_bytes: bytes) -> InferenceResponse:
    """
    Запускает процесс инференса модели и выдает ответ от модели. 
    Возвращает результат в виде объекта InferenceResponse.

    Параметры:
        image_bytes (bytes): Изображение в виде массива байт.

    Returns:
        BoxResponse: Ответ модели, содержащий информацию о дефекте.
    """

    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    predict_results = model.predict(source=image)

    # достали классы
    classes = [item.item() for result in predict_results for item in result.boxes.cls]
    # достали ббоксы
    boxes = [[item.item() for item in tensor] for result in predict_results for tensor in result.boxes.xywh]

    # формируем ответ 
    box_responses = []
    for i in range(len(classes)):
        box_class = int(classes[i])
        box = boxes[i]
        class_name = predict_results[0].names[box_class]  # Получаем название класса по id
        x, y, w, h = box  # Распаковываем координаты и размеры

        response = BoxResponse(
            class_name=class_name,
            class_id=box_class,
            x=x,
            y=y,
            w=w,
            h=h
        )        
        box_responses.append(response)


    return InferenceResponse(
        class_name="OK" if len(box_responses) == 0 else "Broken",
        class_id=0 if len(box_responses) == 0 else 1,
        boxes=box_responses
    )
