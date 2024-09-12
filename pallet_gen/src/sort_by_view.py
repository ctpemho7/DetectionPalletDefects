import os
import shutil
from pathlib import Path

# Путь к директории, где находятся файлы
source_directory = Path(__file__).resolve().parent.parent / 'output'

# Путь к директории, куда будут перемещены файлы (вы можете указать ту же директорию, если нужно создать папки внутри)
source_directory = source_directory

# Получаем список всех файлов в исходной директории
files = os.listdir(source_directory)

# Проходим по каждому файлу
for file_name in files:
    # Проверяем, является ли элемент файлом (чтобы исключить папки)
    if os.path.isfile(os.path.join(source_directory, file_name)):
        # Извлекаем часть названия с 'view_X'
        view_folder = file_name.split('_')[2].split('.')[0]

        # Папка назначения
        target_folder = os.path.join(source_directory, view_folder)

        # Создаем папку, если она не существует
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Полные пути для перемещения файла
        source_path = os.path.join(source_directory, file_name)
        destination_path = os.path.join(target_folder, file_name)

        # Перемещаем файл
        shutil.move(source_path, destination_path)

print('Файлы успешно рассортированы.')
