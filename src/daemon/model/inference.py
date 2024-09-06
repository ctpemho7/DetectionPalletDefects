from pydantic import BaseModel
import random


# Иммитация ответа модели
class InferenceResponse(BaseModel):
    class_name: str  # Название класса дефекта
    class_id: int    # Идентификатор класса дефекта
    x: int           # Координата X верхнего левого угла области дефекта
    y: int           # Координата Y верхнего левого угла области дефекта
    h: int           # Высота области дефекта
    w: int           # Ширина области дефекта


# Функция для генерации случайного класса
def infer_defect(image_bytes: bytes) -> InferenceResponse:
    """
    Имитирует процесс инференса модели и генерирует случайный ответ.

    Функция выбирает случайный класс дефекта из предопределенного списка, а также 
    случайные координаты и размеры для области дефекта. Возвращает результат в виде
    объекта InferenceResponse.

    Параметры:
        image_bytes (bytes): Данные изображения (не используются сейчас).

    Returns:
        InferenceResponse: Имитация ответа модели, содержащая информацию о дефекте.
    """

    # Список возможных классов
    classes = {
        1: 'трещина',
        2: 'потертость',
        3: 'все_гуд'
    }

    # Генерируем случайные данные
    class_id = random.choice(list(classes.keys()))
    class_name = classes[class_id]
    x, y = random.randint(0, 40), random.randint(0, 40)
    h, w = random.randint(40, 80), random.randint(40, 90)

    return InferenceResponse(
        class_name=class_name, class_id=class_id, x=x, y=y, h=h, w=w
    )
