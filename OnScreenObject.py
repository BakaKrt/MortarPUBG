from Screen import MyScreen
from DistanceCalc import DistanceCalc


class OnScreenObject:
    ALL_OBJECTS = {}
    SCREEN: MyScreen
    def __init__(self, name:str, x1:int, y1:int, x2:int, y2:int):
        self.name = name
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.center_x_offset = 0
        self.center_y_offset = 0

        if name.__contains__("ping"):
            self.center_x_offset = abs(x2-x1)/2
            self.center_y_offset = y2-y1
        elif name.__contains__("teammate"):
            self.center_x_offset = abs(x2-x1)/2
            self.center_y_offset = abs(y2-y1)/2

        OnScreenObject.ALL_OBJECTS[name] = self

    def draw(self, screen:MyScreen, x:int, y:int):
        print(DistanceCalc.oneKilometerInPixels)
        if self.name.__contains__("teammate") and DistanceCalc.oneKilometerInPixels != None:
            pixels = DistanceCalc.fromGameMetersToMonitor(700)
            screen.canvas.create_oval(
                x - pixels, y - pixels,
                x + pixels, y + pixels,
                outline="#f11",fill="", width=2
            )
        screen.draw_image(self.name, x, y)
        
    @staticmethod
    def get(name:str):
        return OnScreenObject.ALL_OBJECTS[name]
    def __str__(self):
        return f"Имя: {self.name}\nВерхний левый угол: {self.x1}, {self.y1}\nПравый нижний угол: {self.x2}, {self.y2}\nДо центра от левого верхнего угла: {self.center_x_offset}, {self.center_y_offset}"

