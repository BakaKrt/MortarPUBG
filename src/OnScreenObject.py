from abc import ABC, abstractmethod
import os
import tkinter as tk
import math

class OnScreenObject(ABC):
    ALL_OBJECTS:list['OnScreenObject'] = []
    from src.Screen import MyScreen
    def __init__(self, screen:MyScreen):
        self.screen = screen
        self.canvas = screen.canvas
        self.item_id = None  # id отрисованного объекта
    
    @abstractmethod
    def draw(self):
        """Абстрактный метод для отрисовки объекта на холсте."""
        pass

    def _append(self):
        OnScreenObject.ALL_OBJECTS.append(self)

    @abstractmethod
    def delete(self):
        """Абстрактный метод для удаления объекта с холста."""
        pass
    
    @staticmethod
    def delete_last():
        if len(OnScreenObject.ALL_OBJECTS) > 0:
            print(OnScreenObject.ALL_OBJECTS[-1])
            print(OnScreenObject.ALL_OBJECTS[-1].item_id)
            if OnScreenObject.ALL_OBJECTS[-1] == None:
                OnScreenObject.delete_last()
            else:
                OnScreenObject.ALL_OBJECTS[-1].delete()
                OnScreenObject.ALL_OBJECTS.pop()

class OnScreenText(OnScreenObject):
    from src.Screen import MyScreen
    def __init__(self, screen:MyScreen, x:int, y:int, text:str|int, color:str="red", angle:int = 0, fontSize:int = 14):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.text = str(text)
        self.color = color
        self.angle = angle
        self.fontSize = fontSize
        self.x_offset = (self.fontSize + 4) * math.cos(math.radians(angle) + math.pi / 2)
        self.y_offset = (self.fontSize + 4) * math.sin(math.radians(angle) + math.pi / 2)
        print(f"оффсеты {self.x_offset}, {self.y_offset}")
    
    def draw(self) -> int:
        self.item_id = self.canvas.create_text(
            self.x + self.x_offset, self.y + self.y_offset, text = self.text,
            angle = self.angle, fill = self.color, font = ("Arial", self.fontSize)
        )
        super()._append()
        return self.item_id

    def delete(self):
        if self.item_id:
            self.canvas.delete(self.item_id)




class OnScreenLine(OnScreenObject):
    from src.Screen import MyScreen
    def __init__(self, screen:MyScreen, x1:int, y1:int, x2:int, y2:int, color:str="black", width:int=4):
        super().__init__(screen)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.width = width
        
    def draw(self) -> int:
        self.item_id = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.width)
        super()._append()
        return self.item_id

    def delete(self):
        if self.item_id:
            self.canvas.delete(self.item_id)

class OnScreenLineAndText(OnScreenObject):
    from src.Screen import MyScreen
    def __init__(self, screen:MyScreen, x1:int, y1:int, x2:int, y2:int, text:str|int, color:str="red", angle:int = 0, width:int=4, fontSize:int = 14):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.width = width
        self.text_obj = OnScreenText(screen, (self.x1+self.x2)/2, (self.y1+self.y2)/2, text, color, angle, fontSize)

        super().__init__(screen)
        
    def draw(self):
        self.item_id = []
        self.item_id.append(self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.width))
        self.item_id.append(self.text_obj.draw())
        super()._append()

    def delete(self):
        if len(self.item_id) > 0:
            for item in self.item_id:
                self.canvas.delete(item)
            self.item_id = []


class OnScreenLines(OnScreenObject):
    from src.Screen import MyScreen
    def __init__(self, screen:MyScreen, coords:list[list[int]]=None, color:str="black", width:int=4):
        self.coords:list[list[int]] = coords
        self.color = color
        self.width = width
        self.item_id:list[int] = []

        super().__init__(screen)
    
    def draw(self):
        self.item_id = []
        for coords in self.coords:
            self.item_id.append(self.canvas.create_line(coords[0], coords[1], coords[2], coords[3], fill=self.color, width=self.width))
            super()._append()
        

    def delete(self):
        if len(self.item_id) > 0:
            for item in self.item_id:
                self.canvas.delete(item)
            self.item_id = []


class OnScreenCircle(OnScreenObject):
    from src.Screen import MyScreen
    def __init__(self, screen:MyScreen, x:int, y:int, radius:int, color:str="black", width:int = 2):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.width = width
    
    def draw(self):
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        self.item_id = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, width=self.width)
        super()._append()

    def delete(self):
        if self.item_id:
            self.canvas.delete(self.item_id)

class OnScreenImage(OnScreenObject):
    def __init__(self, screen, x, y, image_path):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.image_path = image_path
        self.photo = None


    def draw(self) ->int | None:
        if not os.path.exists(self.image_path):
            print(f"Error: Image file not found at: {self.image_path}")
            return

        try:
            self.photo = tk.PhotoImage(file=self.image_path)
            self.canvas.image = self.photo # Keep a reference!
            self.item_id = self.canvas.create_image(self.x, self.y, image=self.photo)
            super()._append()
            return self.item_id

        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def delete(self):
        if self.item_id:
            self.canvas.delete(self.item_id)