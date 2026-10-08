"""Модуль, содержащий логику и графический интерфейс анимации случайного пути."""

import tkinter as tk
import math
import random

class App:
    """
    Класс приложения для визуализации случайного пути точки.
    
    Обеспечивает настройку главного окна, создание интерактивных
    элементов управления и логику математического расчета шагов.
    """

    def __init__(self, root):
        """
        Инициализирует графическое приложение.

        Args:
            root (tk.Tk): Корневое окно tkinter.
        """
        self.root = root
        self.root.title("Случайный путь")
        self.width = 800
        self.height = 600

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Храним координаты как прямые атрибуты класса (без лишних словарей)
        self.x = self.width / 2
        self.y = self.height / 2

        self._create_widgets()
        self._walk_step()

    def _create_widgets(self):
        """Создает слайдеры для интерактивного управления анимацией."""
        self.step_scale = tk.Scale(
            self.control_frame, from_=1, to=30, orient=tk.HORIZONTAL, label="Величина шага"
        )
        self.step_scale.set(5)
        self.step_scale.pack(side=tk.LEFT, padx=20)

        self.angle_scale = tk.Scale(
            self.control_frame, from_=0, to=360, orient=tk.HORIZONTAL, label="Направление (градусы)"
        )
        self.angle_scale.set(90)
        self.angle_scale.pack(side=tk.LEFT, padx=20)

        self.gravity_scale = tk.Scale(
            self.control_frame, from_=0.0, to=1.0, resolution=0.01, 
            orient=tk.HORIZONTAL, label="Сила притяжения (0-1)"
        )
        self.gravity_scale.set(0.1)
        self.gravity_scale.pack(side=tk.LEFT, padx=20)

    def _walk_step(self):
        """Вычисляет новые координаты точки и отрисовывает шаг."""
        step_size = self.step_scale.get()
        prio_angle_deg = self.angle_scale.get()
        gravity = self.gravity_scale.get()

        # СЛОЖНЫЙ МАТЕМАТИЧЕСКИЙ БЛОК: Расчет случайного вектора движения
        # 1. Генерируем абсолютно случайный вектор направления
        rand_angle = random.uniform(0, 2 * math.pi)
        rand_dx = math.cos(rand_angle)
        rand_dy = math.sin(rand_angle)

        # 2. Вычисляем вектор заданного приоритетного направления
        prio_angle_rad = math.radians(prio_angle_deg)
        prio_dx = math.cos(prio_angle_rad)
        prio_dy = math.sin(prio_angle_rad)

        # 3. Линейная интерполяция (смешивание) векторов на основе силы притяжения
        vx = rand_dx * (1 - gravity) + prio_dx * gravity
        vy = rand_dy * (1 - gravity) + prio_dy * gravity

        # 4. Нормализация итогового вектора для сохранения точной длины шага
        length = math.hypot(vx, vy)
        if length != 0:
            vx /= length
            vy /= length

        # Расчет новых координат
        new_x = self.x + vx * step_size
        new_y = self.y + vy * step_size

        # Рисуем линию белым цветом
        self.canvas.create_line(self.x, self.y, new_x, new_y, fill="white", width=2)

        # Возврат в центр при выходе за границы экрана
        if not (0 <= new_x <= self.width and 0 <= new_y <= self.height):
            new_x, new_y = self.width / 2, self.height / 2

        # Обновляем текущие координаты
        self.x, self.y = new_x, new_y
        
        self.root.after(20, self._walk_step)