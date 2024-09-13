import requests


url = 'http://localhost:8000/metrics'

response = requests.get(url)

# Чекаем успешность запроса
if response.status_code == 200:
    print(response.text)
else:
    print(f'Error: {response.status_code}, {response.text}')
