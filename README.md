# DetectionPalletDefects
Система компьютерного зрения для поиска дефектов паллетов.
### Система создана с целью:
- Уменьшения расходов
- Ускорения процесса проверки качества паллет
- Снижения нагрузки на специалистов

### Основное отличие нашего проекта: 
Датасет дополнен сгенерированными данными 3D моделей Blender

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
1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. python ./src/daemon/daemon.py

# Полезные материалы:
- https://universe.roboflow.com/browse/logistics/pallets
- https://universe.roboflow.com/esprit-moito/mask_rcnn-73vt5
- https://universe.roboflow.com/emmsolutions/logistic-vat7c
- https://datasetninja.com/wood-defect-detection

