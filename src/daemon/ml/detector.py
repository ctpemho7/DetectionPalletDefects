from ultralytics import YOLO
from typing import List
from PIL import Image
from ml.base_model import BaseModel


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
