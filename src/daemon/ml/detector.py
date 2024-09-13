from ultralytics import YOLO
from typing import List
from PIL import Image

from ..ml.base_model import BaseModel
from ..ml.responses import DetectionInferenceResponse, BoxResponse

class YOLOModel(BaseModel):
    def load_weights(self) -> None:
        """
        Загрузка весов модели.
        """
        self.model = YOLO(self.weights_path)

    def predict(self, images: List[Image.Image]) -> List:
        """
        Выполнение предсказаний на основе списка изображений.
        
        :param images: Список изображений (PIL Image)
        :return: Список результатов предсказаний
        """
        predictions = self.model(source=images)
        # predictions = []
        # for img in images:
            # img_array = np.array(img)  # Преобразуем изображение в массив NumPy
            # result = self.model(img_array)  # Выполняем предсказание
            # predictions.append(result)
        return predictions

    def train(self, images: List[Image.Image], labels: List) -> None:
        """
        Метод обучения модели. 
        """
        raise NotImplementedError("Обучение для YOLO не реализовано в этом классе.")


    def get_response(prediction_list):
        """
        Получение ответа модели в необходимом для задачи формате
        """
        # тк одна картинка берем только её
        predict_result = prediction_list[0]

        # достали классы
        classes = predict_result.boxes.cls.tolist()
        # достали ббоксы
        boxes = predict_result.boxes.xywh.tolist()

        # формируем ответ 
        box_responses = []
        for i in range(len(classes)):
            box_class = int(classes[i])
            box = boxes[i]
            class_name = predict_result.names[box_class]  # Получаем название класса по id
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


        return DetectionInferenceResponse(
            class_name="OK" if len(box_responses) == 0 else "Broken",
            class_id=0 if len(box_responses) == 0 else 1,
            boxes=box_responses
        )
