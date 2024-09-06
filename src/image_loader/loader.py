import requests
from pathlib import Path

image_path = Path('images') / 'image1.jpg'

url = 'http://localhost:8000/infer/'

# Открываем картинку в бинарном режиме
with open(image_path, 'rb') as image_file:
    # Заголовок запроса
    files = {'file': image_file}

    response = requests.post(url, files=files)

# Чекаем успешность запроса
if response.status_code == 200:
    print(response.json())
else:
    print(f'Error: {response.status_code}, {response.text}')
