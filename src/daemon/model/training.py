from pydantic import BaseModel


# Иммитация ответа дообучения
class TrainingResponse(BaseModel):
    message: str


def train_model() -> TrainingResponse:
    # Заглушка для дообучения
    return TrainingResponse(message='Model training initiated.')
