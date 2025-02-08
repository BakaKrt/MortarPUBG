import win32api
import win32con
import time

import threading



class _ListenerData:
    data = {}
    def __init__(self, name: str, func, keys:list[int], sleep_time:float = 0.1):
        self.name = name
        self.func = func
        self.keys = keys
        self.prev_state: bool = False

        _ListenerData.data[name] = self
    @staticmethod
    def get(name:str):
        return _ListenerData.data[name]


class AllListener:
    def __init__(self, listenedFunctions: list[_ListenerData]):
        self.listenFunctions = listenedFunctions
        self._running = False  # Флаг для управления потоком
        self._thread = None

    @staticmethod
    def get_mouse_pos():
        return win32api.GetCursorPos()

    def _run(self):
        """Метод, выполняющийся в потоке"""
        self._running = True
        while self._running:
            for func in self.listenFunctions:
                allButtonsPressed = True
                for key in func.keys:
                    allButtonsPressed *= (win32api.GetAsyncKeyState(key) < 0)
                #print(f"DEBUG: {func.name} {func.keys} state {allButtonsPressed}")
                if allButtonsPressed == True and func.prev_state == 0:
                    func.func()
                func.prev_state = allButtonsPressed
            time.sleep(0.05) # Можно изменить задержку


    def start(self):
        """Запускает слушателя в отдельном потоке"""
        if not self._running:
            self._thread = threading.Thread(target=self._run)
            self._thread.daemon = True  # Поток завершится при выходе основной программы
            self._thread.start()
        else:
            print("AllListener already running")


    def stop(self):
        """Останавливает слушателя"""
        if self._running:
            self._running = False
            if self._thread:
                self._thread.join() #  Ждем, пока поток завершится.
            self._thread = None
            print("AllListener stopped")
        else:
            print("AllListener is not running")