import os
import random
import mathutils
from collections import defaultdict
import sys
from pathlib import Path
from typing import List
import bpy


class PalletGenerator:
    def __init__(
        self,
        folder_path,
        obj_positions,
        rotation_axes,
        output_dir,
        box_generator,
        camera_views,
        camera_shift=0,
        min_defects_count=0,
        max_defects_count=2,
    ):
        '''
        Инициализирует PalletGenerator с заданными параметрами.

        :param folder_path: Директория, содержащая файлы .obj объектов.
        :param obj_positions: Словарь с именами объектов и их позициями на паллете.
        :param rotation_axes: Словарь с именами объектов и осями их вращения.
        :param output_dir: Директория, куда будут сохраняться рендеры изображений.
        :param box_generator: Экземпляр класса BoxesArrangement для генерации коробок.
        :param objects_generator: Экземпляр класса PBRMaterialAssigner для применения материалов.
        :param camera_views: Список позиций камер для рендеринга изображений.
        :param camera_shift: Сдвиг камерных позиций.
        :param min_defects_count: Минимальное количество дефектов на паллете.
        :param max_defects_count: Максимальное количество дефектов на паллете.
        '''
        self.folder_path = folder_path
        self.output_dir = output_dir
        self.obj_positions = obj_positions
        self.rotation_axes = rotation_axes
        self.box_generator = box_generator
        self.min_defects_count = max(0, min_defects_count)
        self.max_defects_count = max(0, max_defects_count)
        self.part_names = [
            'desk_w100',
            'desk_w145',
            'desk_h800',
            'block',
            'sideblock',
        ]
        self.camera_views = camera_views
        self.camera_shift = camera_shift
        self.setup_scene()
        self.save_img_format = 'png'
        # self.enable_gpu_rendering()

    def setup_scene(self):
        '''
        Конфигурирует параметры рендеринга для сцены.
        '''
        # Настройка разрешения рендера
        bpy.context.scene.render.resolution_x = 1024
        bpy.context.scene.render.resolution_y = 1024

        # Устанавливаем формат рендера
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.image_settings.color_mode = (
            'RGBA'  # Включить альфа-канал
        )

        # Включаем прозрачный фон
        bpy.context.scene.render.film_transparent = True

        # Выключаем упрощение рендера
        bpy.context.scene.render.use_simplify = False

        # Включаем antialising
        bpy.context.scene.eevee.use_taa_reprojection = True

    def enable_gpu_rendering(self):
        '''
        Настраивает Blender для использования GPU для рендеринга с Cycles.
        '''
        # Устанавливаем Cycles как движок рендеринга
        bpy.context.scene.render.engine = 'CYCLES'

        # Включаем рендеринг на GPU
        bpy.context.preferences.addons[
            'cycles'
        ].preferences.compute_device_type = (
            'CUDA'  # Для RTX можно также 'OPTIX'
        )

        # Проверяем и выбираем все доступные устройства
        bpy.context.preferences.addons['cycles'].preferences.get_devices()
        for device in bpy.context.preferences.addons[
            'cycles'
        ].preferences.devices:
            device.use = True  # Включаем все устройства для рендеринга

        # Настраиваем сцену на использование GPU
        bpy.context.scene.cycles.device = 'GPU'

        # Установим параметры для рендера (опционально)
        bpy.context.scene.cycles.samples = 128  # Количество сэмплов
        bpy.context.scene.cycles.use_adaptive_sampling = (
            True  # Адаптивная выборка
        )

    def add_light(self):
        '''
        Добавляет источник света в сцену, если его еще нет.

        :return: Объект источника света.
        '''
        # Проверяем наличие источника света и добавляем его при необходимости
        light_name = 'PointLight'
        if light_name in bpy.data.objects:
            light = bpy.data.objects[light_name]
        else:
            bpy.ops.object.light_add(type='POINT')
            light = bpy.context.object
            light.name = light_name
        light.data.energy = 1500
        return light

    def look_at(self, camera_obj, target_point: List[float]):
        '''
        Настраивает камеру так, чтобы она смотрела на указанную целевую точку.

        :param camera_obj: Объект камеры, который нужно настроить.
        :param target_point: Координаты целевой точки [x, y, z].
        '''
        direction = mathutils.Vector(target_point) - camera_obj.location
        camera_obj.rotation_euler = direction.to_track_quat(
            '-Z', 'Y'
        ).to_euler()

    def set_camera_and_look_at(self, location):
        '''
        Устанавливает положение камеры и её ориентацию, чтобы она смотрела на центр сцены.

        :param location: Позиция, где будет размещена камера.
        '''
        camera = bpy.data.objects.get('Camera')
        if camera is None:
            bpy.ops.object.camera_add()
            camera = bpy.context.object
            camera.name = 'Camera'

        light = self.add_light()
        camera_distance = 6
        location = (
            location[0] * camera_distance,
            location[1] * camera_distance,
            location[2] * camera_distance,
        )
        camera.location = location
        self.look_at(camera, [0, 0, 0])
        light.location = camera.location
        light.rotation_euler = camera.rotation_euler
        bpy.context.scene.camera = camera

    def render_and_save_image(self, camera_setup_func, output_path: str):
        '''
        Рендерит изображение с заданной настройкой камеры и сохраняет его по указанному пути.

        :param camera_setup_func: Функция для настройки камеры перед рендерингом.
        :param output_path: Путь, по которому будет сохранено рендеренное изображение.
        '''
        camera_setup_func()
        bpy.context.scene.render.filepath = (
            output_path + f'.{self.save_img_format}'
        )
        bpy.ops.render.render(write_still=True)

    def rotate_obj(self, obj, axes: tuple[str]):
        '''
        Случайным образом вращает объект вокруг указанных осей.

        :param obj: Объект, который нужно повернуть.
        :param axes: Кортеж осей ('X', 'Y', 'Z'), вокруг которых можно вращать.
        '''
        for axis in axes:
            if random.randint(0, 2) == 1:
                if axis == 'X':
                    obj.rotation_euler[0] += random.choice([0, 3.14159])
                elif axis == 'Y':
                    obj.rotation_euler[1] += random.choice([0, 3.14159])
                elif axis == 'Z':
                    obj.rotation_euler[2] += random.choice([0, 3.14159])

    def import_and_place_obj(
        self,
        file_path: str,
        location: tuple[float],
        rotation_info: dict = None,
    ):
        '''
        Импортирует объект из файла .obj и размещает его в сцене с возможным поворотом.

        :param file_path: Путь к файлу .obj.
        :param location: Позиция, где объект будет размещен.
        :param rotation_info: Опциональный словарь с осями вращения.
        '''
        bpy.ops.import_scene.obj(filepath=file_path)
        imported_object = bpy.context.selected_objects[0]
        imported_object.location = location
        if rotation_info:
            self.rotate_obj(imported_object, rotation_info)

        # Передаём название объекта и пути к текстурам
        assigner = PBRMaterialAssigner(
            obj=imported_object,
            color_texture=str(
                Path(__file__).resolve().parent.parent
                / 'textures'
                / 'pallet_color_texture.png'
            ),
            roughness_texture=str(
                Path(__file__).resolve().parent.parent
                / 'textures'
                / 'pallet_roughness_texture.png'
            ),
            normal_texture=str(
                Path(__file__).resolve().parent.parent
                / 'textures'
                / 'pallet_roughness_texture.png'
            ),
        )

        # Применяем текстуру к объекту
        assigner.apply_material()

    def render_setup(self):
        '''
        Рендерит и сохраняет изображения из разных видов камер.
        '''
        for j, angle in enumerate(self.camera_views):
            angle_shift = tuple(
                a + random.uniform(-self.camera_shift, self.camera_shift)
                for a in angle
            )
            angle = angle_shift
            self.set_camera_and_look_at(angle)
            pallet_index = len(os.listdir(self.output_dir)) // len(
                self.camera_views
            )
            output_path = os.path.join(
                self.output_dir, f'pallet_{pallet_index}_view-{j}'
            )
            self.render_and_save_image(
                lambda: self.set_camera_and_look_at(angle), output_path
            )

    def create_pallet(self, num_pallets: int, good_percentage=5):
        '''
        Создает и рендерит несколько паллет с дефектами или без.

        :param num_pallets: Количество паллет для создания.
        :param good_percentage: Процент паллет без дефектов.
        '''
        if good_percentage > 0:
            good_count = int(num_pallets * (good_percentage / 100))
        else:
            good_count = 0

        self.set_camera_and_look_at((0, 0, 0))

        missing_element_last_pos_names = []
        for i in range(num_pallets):
            is_good_pallet = i < good_count
            defects_count = 0
            missing_element_count = 0
            if self.max_defects_count > self.min_defects_count:
                need_defects_count = random.randint(
                    self.min_defects_count, self.max_defects_count
                )
            elif self.max_defects_count == self.min_defects_count:
                need_defects_count = self.max_defects_count
            else:
                need_defects_count = 0

            for position_name, position in self.obj_positions.items():
                obj_name = '_'.join(position_name.split('_')[:-1])
                if is_good_pallet or defects_count > need_defects_count:
                    dir_path = os.path.join(
                        self.folder_path, f'{obj_name}_normal'
                    )
                else:
                    dir_path = os.path.join(self.folder_path, f'{obj_name}')
                    defects_count += 1

                obj_files = [
                    file
                    for file in os.listdir(dir_path)
                    if file.endswith('.obj')
                ]
                random_file = random.choice(obj_files)
                file_path = os.path.join(dir_path, random_file)

                if (
                    random.randint(0, 20) == 5
                    and missing_element_count == 0
                    and not is_good_pallet
                ):
                    missing_element_count = 1
                else:
                    self.import_and_place_obj(
                        file_path,
                        position,
                        self.rotation_axes.get(obj_name, tuple()),
                    )

            if (
                len(missing_element_last_pos_names)
                >= len(self.obj_positions) - 9
            ):
                missing_element_last_pos_names = []

            self.box_generator.generate_boxes()

            self.render_setup()
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)
            self.set_camera_and_look_at((0, 0, 0))


class BoxesArrangement:
    def __init__(
        self,
        pallet_x_min: float,
        pallet_x_max: float,
        pallet_y_min: float,
        pallet_y_max: float,
        box_size_x: float,
        box_size_y: float,
        box_height: float,
        offset_x: float,
        offset_y: float,
        box_offset_x: float,
        box_offset_y: float,
        box_base_height: float,
        layers_count: int,
        count_boxes_delete: int,
        box_color: tuple[float, float, float, float],
    ):
        '''
        Инициализирует параметры для размещения коробок на паллете.

        :param pallet_x_min: Минимальная координата X паллеты.
        :param pallet_x_max: Максимальная координата X паллеты.
        :param pallet_y_min: Минимальная координата Y паллеты.
        :param pallet_y_max: Максимальная координата Y паллеты.
        :param box_size_x: Размер коробки по оси X.
        :param box_size_y: Размер коробки по оси Y.
        :param box_height: Высота коробки.
        :param offset_x: Смещение по оси X для размещения коробок.
        :param offset_y: Смещение по оси Y для размещения коробок.
        :param box_offset_x: Отступ между коробками по оси X.
        :param box_offset_y: Отступ между коробками по оси Y.
        :param box_base_height: Высота основания коробки на паллете.
        :param layers_count: Количество слоев коробок.
        :param count_boxes_delete: Количество коробок для случайного удаления.
        :param box_color: Цвет коробок в формате RGBA.
        '''
        self.pallet_x_min = pallet_x_min
        self.pallet_x_max = pallet_x_max
        self.pallet_y_min = pallet_y_min
        self.pallet_y_max = pallet_y_max
        self.box_size_x = box_size_x
        self.box_size_y = box_size_y
        self.box_height = box_height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.box_offset_x = box_offset_x
        self.box_offset_y = box_offset_y
        self.box_base_height = box_base_height
        self.layers_count = layers_count
        self.count_boxes_delete = count_boxes_delete
        self.box_color = box_color

    def generate_boxes(self):
        '''
        Генерирует коробки на паллете.
        '''
        if self.layers_count > 0:
            self.clear_previous_boxes()
            self.create_box_material()
            self.calculate_box_positions()
            self.create_boxes()
        else:
            print('Количество слоев указано 0')

    def clear_previous_boxes(self):
        '''
        Удаляет все предыдущие коробки на паллете.
        '''
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and 'Cube' in obj.name:
                obj.select_set(True)
        bpy.ops.object.delete()

    def create_box_material(self):
        '''
        Создает материал для коробок с заданным цветом.
        '''
        # Создание черного материала
        self.black_material = bpy.data.materials.new(name='BoxMaterial')
        self.black_material.diffuse_color = (
            self.box_color
        )  # RGB + Alpha (1 = полностью непрозрачный)
        self.black_material.use_nodes = True
        bsdf = self.black_material.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = self.box_color

    def calculate_box_positions(self):
        '''
        Вычисляет позиции коробок на паллете.
        '''
        # Границы размещения коробок на паллете
        pallet_x_min = self.pallet_x_min
        pallet_x_max = self.pallet_x_max
        pallet_y_min = self.pallet_y_min
        pallet_y_max = self.pallet_y_max

        # Границы размещения коробок на паллете с учетом отступов
        pallet_x_min += self.offset_x
        pallet_x_max -= self.offset_x
        pallet_y_min += self.offset_y
        pallet_y_max -= self.offset_y

        # Вычисление доступного пространства для коробок
        available_width_x = self.pallet_x_max - self.pallet_x_min
        available_width_y = self.pallet_y_max - self.pallet_y_min

        # Вычисление количества коробок
        num_boxes_x = int(
            available_width_x // (self.box_size_x + self.box_offset_x)
        )
        num_boxes_y = int(
            available_width_y // (self.box_size_y + self.box_offset_y)
        )

        # Центральное смещение для выравнивания коробок
        center_offset_x = (
            available_width_x
            - (
                num_boxes_x * (self.box_size_x + self.box_offset_x)
                - self.box_offset_x
            )
        ) / 2
        center_offset_y = (
            available_width_y
            - (
                num_boxes_y * (self.box_size_y + self.box_offset_y)
                - self.box_offset_y
            )
        ) / 2

        # Позиции коробок по слоям
        self.box_positions = defaultdict(list)
        for layer in range(self.layers_count):
            for i in range(num_boxes_x):
                for j in range(num_boxes_y):
                    box_x = (
                        pallet_x_min
                        + center_offset_x
                        + i * (self.box_size_x + self.box_offset_x)
                        + self.box_size_x / 2
                    )
                    box_y = (
                        pallet_y_min
                        + center_offset_y
                        + j * (self.box_size_y + self.box_offset_y)
                        + self.box_size_y / 2
                    )
                    box_z = (
                        self.box_base_height
                        + self.box_height / 2
                        + layer * self.box_height
                    )
                    self.box_positions[layer].append((box_x, box_y, box_z))

        # Удаление коробок случайным образом
        self.remove_random_boxes()

    def remove_random_boxes(self):
        '''
        Создает коробки на паллете на основе вычисленных позиций и материала.
        '''
        for _ in range(self.count_boxes_delete):
            layer_id = random.randint(0, self.layers_count - 1)
            layer_boxes_count = len(self.box_positions[layer_id])
            if layer_boxes_count > 0:
                box_id = random.randint(0, layer_boxes_count - 1)
                self.box_positions[layer_id][box_id] = tuple()
                while self.layers_count - 1 > layer_id >= 0:
                    layer_id += 1
                    if layer_id < self.layers_count:
                        self.box_positions[layer_id][box_id] = tuple()

    def create_boxes(self):
        '''
        Удаляет случайное количество коробок на паллете.
        '''
        for positions in self.box_positions.values():
            for position in positions:
                if position:
                    x, y, z = position
                    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
                    box = bpy.context.object
                    box.scale = (
                        self.box_size_x,
                        self.box_size_y,
                        self.box_height,
                    )

                    # Применение черного материала к коробке
                    if len(box.data.materials) == 0:
                        box.data.materials.append(self.black_material)
                    else:
                        box.data.materials[0] = self.black_material


class PBRMaterialAssigner:
    def __init__(
        self,
        obj,
        color_texture: str,
        roughness_texture: str = None,
        normal_texture: str = None,
    ):
        '''
        Инициализация класса для применения PBR текстур.
        :param obj_name: Название объекта, на который нужно наложить материал.
        :param color_texture: Путь к текстуре цвета (Base Color).
        :param roughness_texture: Путь к текстуре шероховатости (Roughness).
        :param normal_texture: Путь к текстуре нормалей (Normal Map).
        '''
        self.obj = obj
        self.color_texture = color_texture
        self.roughness_texture = roughness_texture
        self.normal_texture = normal_texture

        # Проверяем, существует ли объект с таким названием
        if not self.obj:
            raise ValueError(f"Объект '{obj.name}' не найден на сцене")

    def create_pbr_material(self):
        '''Создаёт PBR материал для объекта.'''
        material = bpy.data.materials.new(self.obj.name + "_Material")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Удаляем стандартный Diffuse BSDF
        nodes.clear()

        # Добавляем PBR Shader
        principled_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        principled_bsdf.location = (0, 0)

        # Убираем отражения
        principled_bsdf.inputs['Specular'].default_value = 0.0

        # Устанавливаем полную матовость
        principled_bsdf.inputs['Roughness'].default_value = 1.0

        # Подключение текстур
        if self.color_texture:
            tex_image = nodes.new(type='ShaderNodeTexImage')
            tex_image.image = bpy.data.images.load(self.color_texture)
            tex_image.location = (-300, 0)
            links.new(
                tex_image.outputs['Color'],
                principled_bsdf.inputs['Base Color'],
            )

        if self.roughness_texture:
            tex_roughness = nodes.new(type='ShaderNodeTexImage')
            tex_roughness.image = bpy.data.images.load(self.roughness_texture)
            tex_roughness.location = (-300, -200)
            tex_roughness.image.colorspace_settings.name = 'Non-Color'
            links.new(
                tex_roughness.outputs['Color'],
                principled_bsdf.inputs['Roughness'],
            )
            # Отключаем фиксированное значение Roughness, если есть текстура
            principled_bsdf.inputs['Roughness'].default_value = 1.0

        # Подключение к выходу материала
        material_output = nodes.new(type='ShaderNodeOutputMaterial')
        material_output.location = (300, 0)
        links.new(
            principled_bsdf.outputs['BSDF'], material_output.inputs['Surface']
        )

        return material

    def apply_material(self):
        '''Применяет созданный материал к объекту.'''
        material = self.create_pbr_material()

        if self.obj.data.materials:
            self.obj.data.materials[0] = material
        else:
            self.obj.data.materials.append(material)


# Импорт параметров в процесс
args = sys.argv
num_pallets = int(args[args.index('--') + 1])
good_percentage = int(args[args.index('--') + 2])
max_defects_count = int(args[args.index('--') + 3])

# Основные рабочие директории
output_dir = Path(__file__).resolve().parent.parent / 'output'
assets_folder_path = Path(__file__).resolve().parent.parent / 'assets'

# Точки для размещения
obj_positions = {
    'desk_w100_r': (1.05, 0.0, 0.033),
    'desk_h800_t': (0.0, 1.5825, 0.33),
    'block_bl': (-1.05, -1.5825, 0.183),
    'desk_w145_upl': (0.9825, 0.0, 0.399),
    'desk_w100_upr': (0.495, 0.0, 0.399),
    'desk_w145_upm': (0.0, 0.0, 0.399),
    'desk_w145_upr': (-0.9825, 0.0, 0.399),
    'desk_w100_upl': (-0.495, 0.0, 0.399),
    'desk_w100_l': (-1.05, 0.0, 0.0329),
    'desk_w145_m': (0.0, 0.0, 0.0329),
    'desk_h800_m': (0.0, 0.0, 0.333),
    'desk_h800_b': (0.0, -1.5825, 0.333),
    'block_ml': (-1.05, 0.0, 0.183),
    'block_tl': (-1.05, 1.5825, 0.183),
    'block_tr': (1.05, 1.5825, 0.183),
    'block_mr': (1.05, 0.0, 0.183),
    'block_br': (1.05, -1.5825, 0.183),
    'sideblock_b': (0.0, -1.65, 0.183),
    'block_m': (0.0, 0.0, 0.183),
    'sideblock_t': (0.0, 1.65, 0.183),
}

# Возможные оси вращения для деталей
rotation_axes = {
    'desk_h800': ('Y', 'Z'),
    'desk_w100': ('X', 'Z'),
    'desk_w145': ('X', 'Z'),
    'block': ('Z'),
}

camera_views = [
    # Вид сверху
    (0, 0, -0.9),           # Сверху
    # Вид сбоку
    (0, -0.9, 0),           # Сбоку, слева
    (0, 0.9, 0),            # Сбоку, справа
    # Вид спереди и сзади
    (1.1, 0, -0),           # Спереди
    (1.1, 0, -0),           # Сзади
    # Вид сбоку с высоты
    (0.4, -0.9, 0.5),       # Под углом, сбоку, чуть сдвинутый вперед
    (-0.4, -0.9, 0.5),      # Под углом, сбоку, чуть сдвинутый назад
    (0.4, -0.9, 0.5),       # Под углом, сбоку, более выраженный
    (-0.4, -0.9, 0.5),      # Под углом, сбоку, более выраженный
    # Диагональные виды на уровне паллеты
    (0.8, 0.8, 0.216),      # Диагонально справа на уровне паллеты
    (-0.8, 0.8, 0.216),     # Диагонально слева на уровне паллеты
    (0.8, -0.8, 0.216),     # Диагонально вперед на уровне паллеты
    (-0.8, -0.8, 0.216),    # Диагонально назад на уровне паллеты
]


box_generator = BoxesArrangement(
    pallet_x_min=-1.2,
    pallet_x_max=1.2,
    pallet_y_min=-1.8,
    pallet_y_max=1.8,
    box_size_x=1,
    box_size_y=random.choice([1, 1.5]),
    box_height=0.5,
    offset_x=0.05,
    offset_y=0.05,
    box_offset_x=0.1,
    box_offset_y=0.1,
    box_base_height=0.432,
    layers_count=random.randint(2, 3),
    count_boxes_delete=0,
    box_color=(0.296, 0.141, 0.028, 1),
)

pallets_generator = PalletGenerator(
    assets_folder_path,
    obj_positions,
    rotation_axes,
    output_dir,
    box_generator,
    camera_views,
    camera_shift=0,
    max_defects_count=max_defects_count,
    min_defects_count=1,
)

pallets_generator.create_pallet(
    num_pallets=num_pallets, good_percentage=good_percentage
)
