import tkinter as tk
import math

def draw_line_with_distance(canvas, x1, y1, x2, y2, font_size, offset_distance, color="black"):
    """Рисует линию между двумя точками, текст с расстоянием над ней,
    и поворачивает текст под углом линии. Исправленная версия!
    """

    # Рисуем линию
    canvas.create_line(x1, y1, x2, y2, fill=color)

    # Вычисляем расстояние
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    distance_str = f"{distance:.2f}"  # Форматируем расстояние

    # Вычисляем угол наклона линии (в градусах)
    angle_rad = math.atan2(y2 - y1, x2 - x1)
    angle_deg = math.degrees(angle_rad)

    # Корректируем угол для Tkinter. В Tkinter углы отсчитываются по часовой стрелке от оси X.
    #  atan2 возвращает угол против часовой стрелки от оси X.
    #  Мы просто меняем знак угла, чтобы получить угол по часовой стрелке.
    angle_deg = -angle_deg


    # Вычисляем координаты для текста.
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # Вычисляем смещение перпендикулярно линии
    offset_x = offset_distance * math.cos(angle_rad + math.pi / 2)
    offset_y = offset_distance * math.sin(angle_rad + math.pi / 2)

    text_x = mid_x + offset_x
    text_y = mid_y + offset_y

    # Создаем текст с углом наклона
    canvas.create_text(text_x, text_y,
                       text=distance_str,
                       font=("Arial", font_size),
                       fill=color,
                       angle=angle_deg)  # Поворачиваем текст

# Пример использования (тот же, что и раньше)
root = tk.Tk()
root.title("Линия с расстоянием")

canvas_width = 400
canvas_height = 300
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

x1, y1 = 50, 50
x2, y2 = 350, 200
font_size = 12
offset_distance = 10
draw_line_with_distance(canvas, x1, y1, x2, y2, font_size, offset_distance)

x3, y3 = 100, 250
x4, y4 = 200, 50
font_size2 = 10
offset_distance2 = 10
draw_line_with_distance(canvas, x3, y3, x4, y4, font_size2, offset_distance2, "blue")

root.mainloop()
