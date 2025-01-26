from src.DistanceCalc import DistanceCalc
from src.Screen import MyScreen
from src.OpenCV import OpenCV
from src.Listeners import _ListenerData, AllListener


from src.OnScreenObject import OnScreenObject
#тестово

def myPush():
    if screen.get_visible():
        x, y = AllListener.get_mouse_pos()
        DistanceCalc.push(x, y)

def teammate_add():
    if screen.get_teammate_add():
        x, y = AllListener.get_mouse_pos()
        screen.draw_teammate_at_screen(x, y)

# def setk_redraw():
#     print("dgnkjdsgs")
#     if screen.get_visible():
#         DistanceCalc.setNeedToReset()
#         myPush()


# def kb_test(screen):
#     print("вызвали тестовую")
#     OpenCV.setMainPhoto(MyScreen.get_screenshot())
#     #OpenCV.setMainPhoto("PlayerUnknown's Battlegrounds_2025.01.23-22.58_1.png")
#     for obj in OpenCV.find_objects_on_screenshot("ping_1.png", "teammate_1.png"):
#         print(obj)
#         screen.draw_line(obj.x1+obj.center_x_offset, obj.y1+obj.center_y_offset, 1920/2, 1080/2, "blue")
# пока не удалять

openCV = OpenCV()
screen = MyScreen()  # Создаем экземпляр MyScreen в главном потоке


distance_calc = DistanceCalc(screen)  #Передаем screen


ctrl_lftmb_lstnr = _ListenerData("ctrl_lftmb",      myPush,               [0x1, 0x11])
overlay_toggle   = _ListenerData("toggle_overlay",  screen.toggle_window, [0x4D]     )
stepback         = _ListenerData("screen_stepback", OnScreenObject.delete_last,[0xBD])
#redraw_setka     = _ListenerData("redraw_setka"   , setk_redraw,          [0x1, 0x12])
teammate_append  = _ListenerData("teammateappnd"  , teammate_add,         [0x1]      )
# скан коды: 1) https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
#            2) https://api.farmanager.com/ru/winapi/virtualkeycodes.html
Listener = AllListener([ctrl_lftmb_lstnr, overlay_toggle, stepback, teammate_append])
Listener.start()


#DistanceCalc.oneKilometerInPixels = 500
# testScreenObj = OnScreenObject("teammate_1.png", 0, 0, 16, 17)
# testScreenObj.draw(screen, 1920/2, 1080/2)




screen.run()