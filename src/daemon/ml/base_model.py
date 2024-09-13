from abc import ABC, abstractmethod
from typing import List
from PIL import Image


class BaseModel(ABC):
    def __init__(self, weights_path: str):
        self.weights_path = weights_path
        self.model = None
        self.load_weights()  # Загрузить веса при инициализации

    @abstractmethod
    def load_weights(self) -> None:
        """
        Метод для загрузки весов модели из файла.
        """
        pass

    @abstractmethod
    def predict(self, data: List[Image.Image]) -> List:
        """
        Метод для выдачи предсказаний.
        :param data: Входные данные для предсказания.
        :return: Результат предсказания.
        """
        pass

    @abstractmethod
    def train(self, training_data, labels) -> None:
        """
        Метод для обучения модели на основе предоставленных данных и меток.
        :param training_data: Данные для обучения.
        :param labels: Метки для данных.
        :return: None
        """
        pass

    @abstractmethod
    def get_response(prediction_list):
        """
        Получение ответа модели в необходимом для задачи формате
        """
        pass
