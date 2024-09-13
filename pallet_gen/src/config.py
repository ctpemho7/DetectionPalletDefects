from pathlib import Path


# Путь к исполняемому файлу Blender
BLENDER_PATH = (
    # 'C:/Program Files/Blender Foundation/Blender 4.2/blender-launcher.exe'  # для Windows
    # '/usr/bin/blender'  # для Linux
)

# Путь к вашему Python-скрипту
PYTHON_SCRIPT_PATH = (
    Path(__file__).parent.resolve() / 'pallet_data_generator_v1.py'
)


# -------------------
# Настройки генерации

# Количество паллет
num_pallets = 10

# Процент идеальных паллет
good_percentage = 10  # %

# Максимальное количество дефектных частей у паллеты
max_defects_count = 4
