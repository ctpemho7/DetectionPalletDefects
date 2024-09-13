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
    <img src="https://github.com/user-attachments/assets/e802b0c2-f200-4b1c-b443-81c21f61767c" width="200" height="200" />
    <img src="https://github.com/user-attachments/assets/8722cd96-2d29-4ff5-b935-f0d0e05618db" width="200" height="200" />
    <img src="https://github.com/user-attachments/assets/57bcbcae-b6ee-42e7-b3a5-8593086f3cb7" width="200" height="200" />
    <img src="https://github.com/user-attachments/assets/627ecaa1-3efd-4745-b25d-72d058c6265d" width="200" height="200" />
</p>
<p align="left">
    <img src="https://github.com/user-attachments/assets/a774c801-4596-4c62-8dcc-1e06920436c7" width="200" height="200" />
    <img src="https://github.com/user-attachments/assets/9f6bbd63-f88f-4437-9def-492956c1a6f3" width="200" height="200" />
    <img src="https://github.com/user-attachments/assets/6254c16f-5213-491a-b329-04f57477e52e" width="200" height="200" />
    <img src="https://github.com/user-attachments/assets/b3963a1c-ff55-4e13-9a0b-c4a3b9d5ef48" width="200" height="200" />
</p>

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
> Зайти на Swagger можно поссылке http://localhost:8000/docs

---

# **Генератор изображений паллет**

Эта система представляет собой инструмент для создания реалистичных изображений паллет с различными конфигурациями и дефектами. Используя комбинацию Blender и Python, проект позволяет генерировать изображения паллет с различными типами грузов и дефектами.
Главная цель этой системы - расширить данные для машинного обучения, используя генерированные изображения паллет.

- Генерация изображений паллет с различными конфигурациями и дефектами
- Поддержка различных типов грузов и дефектов
- Настройка параметров генерации: количество паллет, процент целых паллет и максимальное количество дефектных элементов
- Использование Blender для рендеринга изображений
- Экспорт изображений в различных форматах

## **Установка и запуск**

1. Скачайте и установите Blender: [Blender Download](https://www.blender.org/download/)
2. В файле `/pallete_gen/src/config.py` укажите путь к исполняемому файлу Blender
3. Запустите файл `/pallete_gen/src/main.py`
4. Результаты будут сохранены в директории `/pallete_gen/output/`

## **В случае ошибок**

Для получения трассировки ошибок запустите скрипт через консоль:

- Для Windows:
  ```bash
  "C:/Program Files/Blender Foundation/Blender 4.2/blender.exe" --background --python ".../pallete_gen/src/pallet_data_generator_v1.py" -- "1" "10" "4"
  ```
- Для Linux:
  ```bash
  "/usr/bin/blender" --background --python ".../pallete_gen/src/pallet_data_generator_v1.py" -- "1" "10" "4"
  ```

**Аргументы после `--`**:

- Аргумент №1: количество паллет для генерации (например, `"1"`)
- Аргумент №2: % целых паллет от общего числа (например, `"10"`)
- Аргумент №3: максимальное количество дефектных элементов на одном паллете (например, `"4"`)

## **Постобработка**

После генерации изображений паллет рекомендуется провести постобработку для улучшения их качества и реалистичности. Процесс включает следующие этапы:

- **ControlNet Canny**: выделение деталей и контуров объектов на изображении.
- **ControlNet SoftEdge**: смягчение краев и углов объектов.
- **Генеративная модель**: доработка изображений для достижения большей реалистичности.

## **Результаты постобработки**

Изображения паллет, прошедшие постобработку, становятся более реалистичными и детализированными. Однако результаты могут варьироваться.

## **Источники**

- [automatic1111 web-ui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [model](https://civitai.com/models/121716/helloobjects)
- [control-net](https://github.com/Mikubill/sd-webui-controlnet)
- [control-net-models](https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main)

## **Генерация данных**

```
object,(pine wood pallet with cargo cardboard boxes),(masterpiece),realistic photography,solo focus,professional photograph,simple white background
Negative prompt: (two tails:1.2),FastNegativeV2,(bad-artist:1),(loli:1.2),(worst quality, low quality:1.4),(bad_prompt_version2:0.8),bad-hands-5,lowres,bad anatomy,bad hands,((text)),(watermark),error,missing fingers,extra digit,fewer digits,cropped,worst quality,low quality,normal quality,((username)),blurry,(extra limbs),bad-artist-anime,badhandv4,EasyNegative,ng_deepnegative_v1_75t,verybadimagenegative_v1.3,BadDream,(three hands:1.1),(three legs:1.1),(more than two hands:1.2),(more than two legs:1.2),
Steps: 20, Sampler: DPM++ 2M, Schedule type: Karras, CFG scale: 7, Seed: 1944526060, Size: 512x512, Model hash: 6d82a674e1, Model: helloobjects_V15evae, ControlNet 0: "Module: canny, Model: control_v11p_sd15_canny [d14c016b], Weight: 1.0, Resize Mode: Crop and Resize, Processor Res: 512, Threshold A: 192.0, Threshold B: 255.0, Guidance Start: 0.0, Guidance End: 1.0, Pixel Perfect: False, Control Mode: ControlNet is more important", ControlNet 1: "Module: softedge_pidinet, Model: control_v11p_sd15_softedge [a8575a2a], Weight: 1.0, Resize Mode: Crop and Resize, Processor Res: 512, Threshold A: 0.5, Threshold B: 0.5, Guidance Start: 0.0, Guidance End: 1.0, Pixel Perfect: False, Control Mode: Balanced", Version: v1.10.1
```

## **Требования**

- Blender 2.8 или выше
- Python 3.7 или выше
- Операционная система: Windows или Linux (macOS не тестировалась)

---

# Полезные материалы:
- https://universe.roboflow.com/browse/logistics/pallets
- https://universe.roboflow.com/esprit-moito/mask_rcnn-73vt5
- https://universe.roboflow.com/emmsolutions/logistic-vat7c
- https://datasetninja.com/wood-defect-detection
- https://universe.roboflow.com/grp12palletclassification/classification_pallet_v1

---
# RoadMap проекта (4.09.24 — 13.09.24)

[Miro](https://miro.com/app/board/uXjVKi3ZjdI=/?share_link_id=999335134571)
<p align="left">
    <img src="https://github.com/user-attachments/assets/cc670e94-47d2-4644-80ff-325a89c1f562" width="1280" height="670" />
</p>


