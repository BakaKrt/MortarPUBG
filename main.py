import pyscreenshot
import cv2
import numpy as np
import keyboard

#285px = 1km = 1000m


def change_saturation(image, saturation_scale=1.5):
    """
    Изменение насыщенности изображения.

    :param image: Входное изображение в формате BGR.
    :param saturation_scale: Коэффициент изменения насыщенности (больше 1 увеличивает насыщенность, меньше 1 уменьшает).
    :return: Изображение с измененной насыщенностью.
    """
    # Преобразование изображения в цветовое пространство HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Разделение изображения на три канала: H, S, V
    h, s, v = cv2.split(hsv_image)

    # Изменение насыщенности
    s = cv2.multiply(s, saturation_scale)

    # Ограничение значений, чтобы они оставались в допустимом диапазоне [0, 255]
    s = np.clip(s, 0, 255).astype(np.uint8)

    # Объединение каналов обратно в изображение
    hsv_image = cv2.merge([h, s, v])

    # Преобразование изображения обратно в цветовое пространство BGR
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return bgr_image


def get_distance(x1, y1, x2, y2):
    dist = pow((pow(abs(x1-x2),2) + pow(abs(y1-y2),2)), 0.5)
    return dist

def match_template(image, template):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc, max_val
    
def find_objects_on_screenshot(screenshot_path, grid_templates, player_template_path, enemy_template_path):
    screenshot = cv2.imread(screenshot_path)

    screenshot = change_saturation(screenshot)


    grid_templates_for_color = []
    grids_templates = []
    for x in grid_templates:
        temp_readed = cv2.imread(x)
        grid_templates_for_color.append(temp_readed)
        temp_loc, temp_val = match_template(temp_readed, screenshot)
        if (temp_val > 0.4):
            grids_templates.append([temp_loc, temp_val])

    
    player_template = cv2.imread(player_template_path)
    enemy_template  = cv2.imread(enemy_template_path)
    
    player_loc, player_val = match_template(player_template, screenshot)
    enemy_loc,  enemy_val  = match_template(enemy_template, screenshot)


    print(f"игрок = {player_val}, враг = {enemy_val}")


    threshold = 0.4  # You can adjust this threshold based on your requirement
    
    if any(grids_templates) >= threshold and player_val >= threshold and enemy_val >= threshold:
        h, w = player_template.shape[:2]
        cv2.rectangle(screenshot, player_loc, (player_loc[0] + w, player_loc[1] + h), (255, 0, 0), 3)


        h, w = enemy_template.shape[:2]
        cv2.rectangle(screenshot, enemy_loc, (enemy_loc[0] + w, enemy_loc[1] + h), (0, 0, 255), 3)
        
        grid_x,   grid_y   = grids_templates[0][0]
        player_x, player_y = player_loc
        enemy_x,  enemy_y  = enemy_loc
        
        temp_grid = grid_templates_for_color
        h, w = temp_grid[0][0].shape[:2]
        print(grids_templates[0])
        cv2.rectangle(screenshot, grids_templates[0][0], (grids_templates[0][0][0] + w, grids_templates[0][0][1] + h), (0, 255, 0), 3)
        

        # Коррекция координат
        player_x += 12
        player_y += 12

        enemy_y += 20
        enemy_x += 8

        grid_x += 4
        grid_y += (4 + 51)
        grid_x_con = grid_x + 285
        one_kilometr = grid_x_con - grid_x

        distance = get_distance(player_x, player_y, enemy_x, enemy_y) * 1000 / one_kilometr



        #grid_width = grid_template.shape[1]
        #grid_height = grid_template.shape[0]
        
        #grid_size = (grid_x + grid_width, grid_y + grid_height)
        
        return f"ДИСТАНЦИЯ {round(distance)} \
            \nкоордината игрока {player_x, player_y} \
            \nкоордината вражеского игрока{enemy_x, enemy_y} \
            \nкоордината сетки {grid_x, grid_y} и {grid_x_con, grid_y}", screenshot
        
    else:
        return None, None


grids = ["grid_vertical.png", "grid_vertical_vikendi.png"]

def main():
    #image = pyscreenshot.grab().save('user_screen.png')
    #screenshot_path = "image.png"
    screenshot_path = "user_screen.png"
    grid_template_path = grids
    player_template_path = "teammate_1.png"
    enemy_template_path = "enemy_1.png"

    result, screen = find_objects_on_screenshot(screenshot_path, grid_template_path, player_template_path, enemy_template_path)
    print(result)
    cv2.imshow('Screen', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    keyboard.add_hotkey('Ctrl + 1', main)
    keyboard.add_hotkey('Ctrl + Space', main)
    keyboard.wait('Ctrl + Q')

    #main()