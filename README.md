# DetectionPalletDefects
Система компьютерного зрения для поиска дефектов паллетов.
### Система создана с целью:
- Уменьшения расходов
- Ускорения процесса проверки качества паллет
- Снижения нагрузки на специалистов

### Основное отличие нашего проекта: 
Датасет дополнен сгенерированными данными 3D моделей Blender.
 
 **Примеры данных, которые мы можем генерировать:**
<p align="left">
    <img src="https://github.com/user-attachments/assets/dcf0fbbf-c8db-4310-8ac0-354490e4856e" width="200" height="200" alt="Scikit-learn" />
    <img src="https://github.com/user-attachments/assets/6e7deebb-2332-4dc1-b467-d735002d9758" width="200" height="200" alt="Scikit-learn" />
    <img src="https://github.com/user-attachments/assets/c4b5562b-7b01-4ed0-bc19-b118b8c538a9" width="200" height="200" alt="Scikit-learn" />
    <img src="https://github.com/user-attachments/assets/6a4f2695-af96-4570-94ca-09361fc27c46" width="200" height="200" alt="Scikit-learn" />
</p>
<p align="left">
    <img src="https://github.com/user-attachments/assets/ac0fe907-e031-479b-bfe4-da68b57dcc1b" width="200" height="200" alt="Scikit-learn" />
    <img src="https://github.com/user-attachments/assets/819349df-a803-4271-a3c9-13d29544b6dc" width="200" height="200" alt="Scikit-learn" />
    <img src="https://github.com/user-attachments/assets/447d7db1-911d-4462-b021-398ffe506fa9" width="200" height="200" alt="Scikit-learn" />
    <img src="https://github.com/user-attachments/assets/f24ab598-5362-4b28-a2f3-a85c90947123" width="200" height="200" alt="Scikit-learn" />

## Видение продукта:
- Автоматическая детекция дефектов паллет 
- Возможность работы в реальном времени 
- Уведомление о дефектах и отчетность 

  **Дополнительно:**
- Дообучение модели 
- Мониторинг и логирование
- UI для валидации данных

# Сборка и установка
> Предварительно необходимо зайти в папку DetectionPalletDefects
1. `python3 -m venv .venv`
2. `source .venv/bin/activate` (Для Windows: `.venv/Scripts/activate`)
3. `pip install -r requirements.txt`
4. `python ./src/daemon/daemon.py`

# Полезные материалы:
- https://universe.roboflow.com/browse/logistics/pallets
- https://universe.roboflow.com/esprit-moito/mask_rcnn-73vt5
- https://universe.roboflow.com/emmsolutions/logistic-vat7c
- https://datasetninja.com/wood-defect-detection

