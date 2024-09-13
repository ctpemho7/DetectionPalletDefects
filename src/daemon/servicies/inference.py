from typing import List
from PIL import Image
from io import BytesIO

from ..ml.detector import YOLOModel
from ..ml.classifier import EfficientNetClassifierModel
from ..ml.responses import InferenceResponse


def infer_defect(image_bytes: bytes) -> InferenceResponse:
    """
    Запускает процесс инференса модели и выдает ответ от модели. 
    Возвращает результат в виде объекта InferenceResponse.

    Параметры:
        image_bytes (bytes): Одно изображение в виде массива байт.

    Returns:
        BoxResponse: Ответ модели, содержащий информацию о дефекте.
    """
    weights_path = "./daemon/ml/weights/efficientnet-1.pth"
    model = EfficientNetClassifierModel(weights_path)
    
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    predict_result = model.predict([image])
    response = model.get_response(predict_result)
    return response
