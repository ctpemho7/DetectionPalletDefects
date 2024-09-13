from typing import List
from PIL import Image
import torch
from torchvision import transforms
import numpy as np

from ..ml.base_model import BaseModel
from ..ml.responses import ClassificationInferenceResponse


class EfficientNetClassifierModel(BaseModel):
    def load_weights(self) -> None:
        """
        Загрузка весов модели.
        """
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = torch.load(self.weights_path, map_location=self.device)
        self.model.eval()

    def predict(self, images: List[Image.Image]) -> List:
        """
        Выполнение предсказаний на основе списка изображений.
        
        :param images: Список изображений (PIL Image)
        :return: Список результатов предсказаний
        """
        
        predictions = []
        for image in images:
            predictions.append(self._predict(image))
        return predictions

    def _predict(self, image):
        # Load and preprocess the image
        image = np.array(image)
        preprocess = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        image = preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)
            confidence = torch.nn.functional.softmax(outputs, dim=1)[0][predicted].item() * 100

        return [predicted.item(), confidence]

    def train(self, images: List[Image.Image], labels: List) -> None:
        """
        Метод обучения модели. 
        """
        raise NotImplementedError("Обучение для YOLO не реализовано в этом классе.")

    def get_response(self, prediction_list) -> ClassificationInferenceResponse:
        """
        Получение ответа модели в необходимом для задачи формате
        """
        # тк одна картинка берем только её
        predict_result = prediction_list[0]

        return ClassificationInferenceResponse(
            class_id=predict_result[0],
            class_name="Broken" if predict_result[0] else "OK",
            confidence=predict_result[1]
        )
