from pydantic import BaseModel
from typing import List


class InferenceResponse(BaseModel):
    class_name: str             # Название класса дефекта
    class_id: int               # Идентификатор класса дефекта


# для детекции
class BoxResponse(BaseModel):
    class_name: str  # Название класса дефекта
    class_id: int    # Идентификатор класса дефекта
    x: float           # Координата X верхнего левого угла области дефекта
    y: float           # Координата Y верхнего левого угла области дефекта
    h: float           # Высота области дефекта
    w: float           # Ширина области дефекта


class DetectionInferenceResponse(InferenceResponse):
    boxes: List[BoxResponse]    # Список со всеми bounding boxes


class ClassificationInferenceResponse(InferenceResponse):
    confidence: float          # Уверенность модели классификации
