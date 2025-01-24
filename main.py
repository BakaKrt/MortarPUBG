from pynput import mouse

import keyboard

from DistanceCalc import DistanceCalc
from Screen import MyScreen
from OpenCV import OpenCV


def on_mouse_click(x, y, button, pressed):
    """Слушатель мыши, возвращает координаты при левом клике"""
    if pressed and button == mouse.Button.left and screen.get_visible():
        DistanceCalc.push(x, y)

def kb_test(screen):
    print("вызвали тестовую")
    OpenCV.setMainPhoto(MyScreen.get_screenshot())
    #OpenCV.setMainPhoto("PlayerUnknown's Battlegrounds_2025.01.23-22.58_1.png")
    for obj in OpenCV.find_objects_on_screenshot("ping_1.png", "teammate_1.png"):
        print(obj)
        screen.draw_line(obj.x1+obj.center_x_offset, obj.y1+obj.center_y_offset, 1920/2, 1080/2, "blue")


openCV = OpenCV()
screen = MyScreen()  # Создаем экземпляр MyScreen в главном потоке


distance_calc = DistanceCalc(screen)  #Передаем screen

mouseListener = mouse.Listener(on_click=on_mouse_click)
mouseListener.start()


keyboard.add_hotkey('Ctrl + 1', lambda: kb_test(screen))
keyboard.add_hotkey('m', lambda: screen.toggle_window())
keyboard.add_hotkey('-', lambda: screen.stepback())

screen.run()


mouseListener.join()