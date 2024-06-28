import pyscreenshot
import cv2
import numpy as np
import keyboard
import os

#285px = 1km = 1000m

def save_image_with_unique_name(image, base_path):
    if not os.path.exists(base_path):
        cv2.imwrite(base_path, image)
        return base_path
    else:
        # Определение уникального имени файла
        base, ext = os.path.splitext(base_path)
        counter = 1
        new_path = f"{base}({counter}){ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}({counter}){ext}"
        cv2.imwrite(new_path, image)
        return new_path

def apply_shadow_boost(image, shadow_boost_factor=1.2):
    lut = np.arange(256, dtype=np.uint8)
    for i in range(256):
        lut[i] = np.clip(i * (shadow_boost_factor if i < 128 else 1), 0, 255)
    shadow_boosted_image = cv2.LUT(image, lut)
    return shadow_boosted_image

def change_saturation(image, saturation_scale=1.5):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)
    s = cv2.multiply(s, saturation_scale)
    s = np.clip(s, 0, 255).astype(np.uint8)
    hsv_image = cv2.merge([h, s, v])
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return bgr_image

def process_images_in_folder(folder_path, grid_templates,player_template_path, enemy_template_path):
    all_processed_photos = []
    for filename in os.listdir(folder_path):
        if filename.startswith("PlayerUnknown's") and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image from {image_path}")
                continue
            
            screenshot = change_saturation(image)
            screenshot = cv2.convertScaleAbs(screenshot, alpha=2, beta=0)
            screenshot = apply_shadow_boost(screenshot)

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

            #print(f"игрок = {player_val}, враг = {enemy_val}")

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
                #print(grids_templates[0])
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

                distance = get_distance(player_x, player_y, enemy_x, enemy_y)
                save_image_with_unique_name(screenshot, "opencv/opencv_screen.png")
                all_processed_photos.append(screenshot)
    return all_processed_photos


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
    screenshot = cv2.convertScaleAbs(screenshot, alpha=2, beta=0)
    screenshot = apply_shadow_boost(screenshot)

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

    #print(f"игрок = {player_val}, враг = {enemy_val}")

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

        distance = get_distance(player_x, player_y, enemy_x, enemy_y)
        #grid_width = grid_template.shape[1]
        #grid_height = grid_template.shape[0]
        #grid_size = (grid_x + grid_width, grid_y + grid_height)
        return f"ДИСТАНЦИЯ {round(distance*1000/one_kilometr)} | {round(distance)} px \
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

    screen = process_images_in_folder("G:\AMD_RELIVE\PlayerUnknown's Battlegrounds", grid_template_path, player_template_path, enemy_template_path)
    for x in screen:
        cv2.imshow('Screen', x)    

    #result, screen = find_objects_on_screenshot(screenshot_path, grid_template_path, player_template_path, enemy_template_path)
    #print(result)
    
    #cv2.imshow('Screen', screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    keyboard.add_hotkey('Ctrl + 1', main)
    keyboard.add_hotkey('Ctrl + Space', main)
    keyboard.wait('Ctrl + Q')

    #main()