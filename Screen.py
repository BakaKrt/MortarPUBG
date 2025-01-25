import tkinter as tk
from tkinter import ttk
import pyautogui


class MyScreen:

    def __init__(self):
        
        self.root = tk.Tk()
        self.screen_width, self.screen_height = pyautogui.size()
        self.root.title("Transparent Overlay")
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        self.root.wm_attributes("-transparentcolor", "grey")
        self.root.wm_attributes("-topmost", True) # Запускает окно поверх всех остальных
        self.root.overrideredirect(True) # Убирает заголовок окна, чтобы окно занимало весь экран
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, bg="grey", highlightthickness=0)
        self.canvas.pack()


        self.window_visible:tk.BooleanVar = True

        self.printed_elements = []
        self.all_images:list[tk.PhotoImage] = []

        # видимость приложения
        self.checkbutton = ttk.Checkbutton(
            self.root,
            text="Visible",
            variable=self.window_visible,
            command=self.toggle_window,
            style="TCheckbutton"
        )
        self.checkbutton.place(x=0, y=self.screen_height*0.1) # Размещаем в углу
        # конец видимости приложения


        # выбор размерной сетки
        self.available_scales = [100, 1000, 500]
        self.pixel_scale:tk.IntVar = tk.IntVar(value=1000)
        y_offset = 0
        for value in self.available_scales:
            radio_button = ttk.Radiobutton(
                self.root,
                text=str(value),
                variable=self.pixel_scale,
                value=value,
                style="TRadiobutton"
            )
            radio_button.place(x=self.checkbutton.winfo_reqwidth(), y=self.screen_height*0.1 + y_offset) # Располагаем вертикально
            y_offset = y_offset + 25
        # конец выбора размерной сетки


        # кнопка метки себя/союзника
        self.teammates:tuple = {}
        self.is_append_teammate:bool = False
        self.btn_teammate_add = ttk.Button(
            self.root, text="Добавить себя/тиммейта", command=self.btn_teammate_add_impl
        )
        self.btn_teammate_add.place(x = self.checkbutton.winfo_reqwidth(), y = self.screen_height*0.1 + y_offset)
        # конец метки себя


    def btn_teammate_add_impl(self):
        if self.is_append_teammate:
            self.is_append_teammate = False
        else:
            self.is_append_teammate = True

    def draw_teammate_at_screen(self, x:int, y:int):
        from OnScreenObject import OnScreenObject
        teammate = OnScreenObject("teammate_1.png", 0, 0, 16, 17)
        teammate.draw(self, x, y)
        self.teammates["teammate_1.png"] = teammate
        self.is_append_teammate = False

    def get_teammate_add(self):
        return self.is_append_teammate

    def get_visible(self):
        return self.window_visible

    @staticmethod
    def get_screen_size():
        return pyautogui.size()

    @staticmethod
    def get_screenshot():
        print("Сделали скриншот")
        screen_width, screen_height = pyautogui.size()
        return pyautogui.screenshot(region=(
            int(screen_width*0.1),  int(screen_height*0.1),
            int(screen_height*0.9), int(screen_height*0.9)
        ))

    def stepback(self):
        if len(self.printed_elements)!= 0:
            self.canvas.delete(self.printed_elements[-1])
            self.printed_elements.pop(-1)

    def run(self):
        self.root.mainloop()


    def draw_line(self, start_x, start_y, end_x, end_y, color="red", width=2):
        """Рисует линию на canvas."""
        self.root.after(0, self._draw_line_impl, start_x, start_y, end_x, end_y, color, width)
        
    
    def _draw_line_impl(self, start_x, start_y, end_x, end_y, color, width):
        element = self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=width)
        self.printed_elements.append(element)


    def draw_text(self, x, y, text, color="black", angle=0, font=("Arial", 14)):
        """Выводит текст на заданных координатах с заданным углом."""
        self.root.after(0, self._draw_text_impl, x, y, text, color, angle, font)


    def _draw_text_impl(self, x, y, text, color, angle, font):
        """Внутренняя функция для отрисовки текста."""
        element = self.canvas.create_text(x, y, text=text, fill=color, font=font, angle=angle)
        self.printed_elements.append(element)


    def draw_triangle(self, x1, y1, x2, y2, x3, y3, color="red", width=2):
        """Рисует треугольник."""
        self.root.after(0, self._draw_triangle_impl, x1, y1, x2, y2, x3, y3, color, width)

    def _draw_triangle_impl(self, x1, y1, x2, y2, x3, y3, color, width):
        """Внутренняя функция для отрисовки треугольника."""
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill='', outline=color, width=width)

    def draw_image(self, filename:str, x:int, y:int):
        image = tk.PhotoImage(file = filename)
        self.all_images.append(image)
        self.canvas.create_image(x, y, image = self.all_images[-1])

    def toggle_window(self):
        """Показывает или скрывает окно."""
        if self.window_visible:
            self.root.withdraw()  # Hide the window
            self.window_visible = False
        else:
            self.root.deiconify() # Show the window
            self.window_visible = True