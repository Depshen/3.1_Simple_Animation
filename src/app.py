"""Модуль графического интерфейса и логики анимации случайного пути."""

import math
import random
import tkinter as tk


class App:
    """Класс главного окна приложения для отрисовки случайного пути."""

    def __init__(self, root: tk.Tk) -> None:
        """Инициализирует главное окно, холст и элементы управления."""
        self.root = root
        self.root.title("Случайный путь")
        self.width = 800
        self.height = 600

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self._create_widgets()

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg="black",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Начальные координаты точки (центр холста)
        self.x = self.width / 2
        self.y = self.height / 2

        self._walk_step()

    def _create_widgets(self) -> None:
        """Создает ползунки для интерактивного управления анимацией."""
        self.step_scale = tk.Scale(
            self.control_frame,
            from_=1,
            to=30,
            orient=tk.HORIZONTAL,
            label="Величина шага",
        )
        self.step_scale.set(5)
        self.step_scale.pack(side=tk.LEFT, padx=20)

        self.angle_scale = tk.Scale(
            self.control_frame,
            from_=0,
            to=360,
            orient=tk.HORIZONTAL,
            label="Направление (градусы)",
        )
        self.angle_scale.set(90)
        self.angle_scale.pack(side=tk.LEFT, padx=20)

        self.gravity_scale = tk.Scale(
            self.control_frame,
            from_=0.0,
            to=1.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            label="Сила притяжения (0-1)",
        )
        self.gravity_scale.set(0.1)
        self.gravity_scale.pack(side=tk.LEFT, padx=20)

    def _walk_step(self) -> None:
        """Вычисляет следующий шаг точки и отрисовывает сегмент линии."""
        step_size = self.step_scale.get()
        prio_angle_deg = self.angle_scale.get()
        gravity = self.gravity_scale.get()

        # Вычисление единичного вектора случайного направления
        rand_angle = random.uniform(0, 2 * math.pi)
        rand_dx = math.cos(rand_angle)
        rand_dy = math.sin(rand_angle)

        # Вычисление единичного вектора приоритетного направления
        prio_angle_rad = math.radians(prio_angle_deg)
        prio_dx = math.cos(prio_angle_rad)
        prio_dy = math.sin(prio_angle_rad)

        # Линейная интерполяция векторов с учетом силы притяжения
        vx = rand_dx * (1 - gravity) + prio_dx * gravity
        vy = rand_dy * (1 - gravity) + prio_dy * gravity

        # Нормализация итогового вектора направления
        length = math.hypot(vx, vy)
        if length != 0:
            vx /= length
            vy /= length

        new_x = self.x + vx * step_size
        new_y = self.y + vy * step_size

        self.canvas.create_line(
            self.x, self.y, new_x, new_y, fill="white"
        )

        # Возврат точки в центр при выходе за границы холста
        if not (0 <= new_x <= self.width and 0 <= new_y <= self.height):
            self.x = self.width / 2
            self.y = self.height / 2
        else:
            self.x = new_x
            self.y = new_y

        self.root.after(20, self._walk_step)
