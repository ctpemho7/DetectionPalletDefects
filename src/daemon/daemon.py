import time
import random
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from prometheus_client import Counter, Gauge, Summary, generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from fastapi.responses import PlainTextResponse
from model.inference import infer_defect, InferenceResponse
from model.training import train_model, TrainingResponse


app = FastAPI()


# Определение метрик
# Общее кол-во инференсов
inference_counter = Counter('inference_total', 'Total number of inferences')
# Кол-во дефектов для каждого класса
defect_counter = Counter(
    'defect_classes', 'Number of defects by class', ['defect_class']
)
# Время выполнения инференса
inference_time = Summary(
    'inference_processing_seconds', 'Time spent inference processing'
)


# Обработчик POST запросов на детекцию дефектов
@app.post('/infer/', response_model=InferenceResponse)
async def infer_image(file: UploadFile = File(...)):
    """
    Выполняет инференс для определения дефектов на переданном изображении.

    Функция принимает изображение в формате файла, выполняет его обработку с помощью 
    функции `infer_defect()` для определения дефекта. В процессе работы функция 
    фиксирует время обработки и обновляет метрики для мониторинга.

    Параметры:
        file (UploadFile): Файл изображения, содержащий изображение для анализа.

    Returns:
        InferenceResponse: Ответ, содержащий информацию о дефекте или его отсутствии.

    Raises:
        HTTPException: Порождает исключение с кодом 500 и описанием ошибки,
        если возникает проблема во время инференса.
    """
    start_time = time.time()  # Зафиксировать время начала

    try:
        image_bytes = await file.read()
        response = infer_defect(image_bytes)

        # Получаем название дефекта
        defect_class = response.class_name

        # Увеличиваем общий счетчик инференсов
        inference_counter.inc()

        # Увеличиваем счетчик для обнаруженного класса дефекта
        defect_counter.labels(defect_class=defect_class).inc()

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Error during inference: {str(e)}'
        )

    finally:
        # Измерить время выполнения
        spent_time = time.time() - start_time
        inference_time.observe(spent_time)


# Обработчик POST запросов на дообучение
@app.post('/train/', response_model=TrainingResponse)
async def train():
    """
    Запускает процесс дообучения модели машинного обучения.
    
    Функция вызывает `train_model()`, которая инициирует дообучение модели. 
    Если процесс проходит успешно, возвращает результат в формате `TrainingResponse`. 
    В случае ошибки, генерирует HTTPException с кодом 500 и сообщением об ошибке.

    Returns:
        TrainingResponse: Результат выполнения процесса дообучения модели.
        
    Raises:
        HTTPException: Порождает исключение, если произошла ошибка в процессе дообучения.
    """
    try:
        response = train_model()
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Error during training: {str(e)}'
        )


# Обработчик GET запросов на получение метрик
@app.get('/metrics')
async def metrics():
    """
    Генерирует и возвращает текстовое представление всех зарегистрированных метрик
    в формате, ожидаемом Prometheus. Метрики возвращаются с правильным MIME-типом
    для корректного сбора Prometheus.
    """
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
