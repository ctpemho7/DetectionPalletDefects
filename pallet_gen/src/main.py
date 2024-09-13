import subprocess
import config


def main():
    print('Генерация вроде бы началась :)')
    subprocess.run(
        [
            config.BLENDER_PATH,
            '--background',                 # Запуск Blender без графического интерфейса
            '--python',                 
            config.PYTHON_SCRIPT_PATH,      # Выполнение Python-скрипта
            '--',                           # Отделяет параметры Blender от пользовательских аргументов
            str(config.num_pallets),        # Количество паллет, необходимых для генерации
            str(config.good_percentage),    # % целых паллет от общего числа
            str(config.max_defects_count),  # Максимальное число поврежденных деталей паллета
        ],
        text=True,
        check=True,
        capture_output=True,
    )


if __name__ == '__main__':
    main()
