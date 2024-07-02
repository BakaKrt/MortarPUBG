import pyscreenshot
import cv2
import numpy as np
import keyboard
import os
import configparser

class PHOTO:
    photo_name = None
    photo_size = []
    photo_readed = []
    pixels_to_center = []
    cv_file = None
    def __init__(self, photo: str, px_to_center: dict, size: dict = []):
        self.photo_name = photo
        self.photo_size = size
        self.pixels_to_center = px_to_center
        self.cv_file = cv2.imread(photo)
    def get_size(self):
        return self.photo_size
    def get_photo_name(self):
        return self.photo_name
    def get_ptc(self):
        return self.pixels_to_center
    def get_len(self):
        return max(self.photo_size[0], self.photo_size[1])
    def get_cv_file(self):
        return self.cv_file

def get_color():
    r = 0
    g = 0
    b = 0
    r_full = False
    g_full = False
    b_full = False
    while r < 255 and g < 255 and b < 255:
        if r == 0 and g == 0 and b == 0:
            return (r, g, b)
            b+=255
        elif ():
            pass
            


class Mortar:
    threshold = 0.0
    teammates = []
    grids = []
    enemy = []
    config = configparser.ConfigParser()
    config.read('config.ini')
    screenshot = PHOTO
    finded_player_1 = [None, None]
    finded_enemy_1  = [None, None]
    def __init__(self, screenshot:str):
        self.screenshot = PHOTO(photo=screenshot, px_to_center=[0,0])
        self.__init_teammates()
        self.__init_grids()
        self.__init_enemies()
        print(self.find_objects_on_screenshot(self.teammates[0], self.enemy[0], self.grids[0]))

    def __init_teammates(self):
        for names in self.config['TEAMMATE']:
            path = self.config.get('TEAMMATE', names)
            if path != None:
                temp = PHOTO(photo=path, px_to_center = [10,10])
                self.teammates.append(temp)
    def __init_grids(self):
        for names in self.config['GRID']:
            path = self.config.get('GRID', names)
            if path != None:
                temp = PHOTO(photo=path, px_to_center = [0,0])
                self.grids.append(temp)
    def __init_enemies(self):
        for names in self.config['ENEMY']:
            path = self.config.get('ENEMY', names)
            if path != None:
                temp = PHOTO(photo=path, px_to_center = [8,20])
                self.enemy.append(temp)
    def set_screen(self, screen: str):
        self.screenshot = screen
    def match_template(self, image, template):
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return max_loc, max_val
    
    def draw_at_screen(self, object, screenshot = screenshot, color = (0, 0, 255), border_px: int = 3):
        cv2.rectangle(screenshot, object, (object[0], object[1]), color, border_px)

    def find_objects_on_screenshot(self, player:PHOTO, enemy:PHOTO, grid:PHOTO):
        grid_template   = grid.get_cv_file()
        player_template = player.get_cv_file()
        enemy_template  = enemy.get_cv_file()
        screenshot      = self.screenshot.get_cv_file()

        grid_loc, grid_val     = self.match_template(screenshot, grid_template)
        player_loc, player_val = self.match_template(screenshot, player_template)
        enemy_loc, enemy_val   = self.match_template(screenshot, enemy_template)

        print(enemy_loc, player_loc, grid_val, player_val, enemy_val)
        if grid_val >= self.threshold and player_val >= self.threshold and enemy_val >= self.threshold:
            player_x, player_y = player_loc
            enemy_x, enemy_y = enemy_loc

            if self.finded_player_1 == [None, None]:
                self.finded_player_1 = [player_x, player_y]
            if self.finded_enemy_1 == [None, None]:
                self.finded_enemy_1 == [enemy_x, enemy_y]
            return {
                "player_x": player_x,
                "player_y": player_y,
                "enemy_x": enemy_x,
                "enemy_y": enemy_y
            }
        else:
            return None
    

mrt = Mortar("photos\\user_screen.png")