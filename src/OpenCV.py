import cv2
import numpy as np
import os

from src.Screen import MyScreen
from src.OnScreenObject import OnScreenObject


class OpenCV:
    mainPhoto = None
    def __init__(self, mainPhoto = None):
        if mainPhoto == None:
            return
        OpenCV.mainPhoto = mainPhoto

    @staticmethod
    def setMainPhoto(mainPhoto):
        if type(mainPhoto) == str:
            print("установили по пути фотки")
            OpenCV.mainPhoto = cv2.imread(mainPhoto)
        else:
            print("установили по скриншоту из PyAutoGUI")
            OpenCV.mainPhoto = MyScreen.get_screenshot() # обычный скриншот
            OpenCV.mainPhoto = np.array(OpenCV.mainPhoto)
            OpenCV.mainPhoto = OpenCV.mainPhoto[:, :, ::-1].copy()


    @staticmethod
    def apply_shadow_boost(image, shadow_boost_factor=1.2):
        lut = np.arange(256, dtype=np.uint8)
        for i in range(256):
            lut[i] = np.clip(i * (shadow_boost_factor if i < 128 else 1), 0, 255)
        shadow_boosted_image = cv2.LUT(image, lut)
        return shadow_boosted_image


    @staticmethod
    def change_saturation(image, saturation_scale=1.5):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        s = cv2.multiply(s, saturation_scale)
        s = np.clip(s, 0, 255).astype(np.uint8)
        hsv_image = cv2.merge([h, s, v])
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return bgr_image

    # @staticmethod
    # def match_template(image, template):
    #     result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #     return max_loc, max_val
    
    @staticmethod
    def match_template(image, template):
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return max_loc, max_val

    @staticmethod
    def find_objects_on_screenshot(_object1:str, _object2:str) -> list[OnScreenObject] | None:
        screenshot = OpenCV.mainPhoto

        screenshot = OpenCV.change_saturation(screenshot, 1.3)
        screenshot = cv2.convertScaleAbs(screenshot, alpha=2, beta=0)
        screenshot = OpenCV.apply_shadow_boost(screenshot) 

        object1 = cv2.imread(_object1)
        object2 = cv2.imread(_object2)
        
        obj1_loc, obj1_val = OpenCV.match_template(object1, screenshot)
        
        obj2_loc, obj2_val = OpenCV.match_template(object2, screenshot)

        print(f"obj1 = {obj1_val}, obj2 = {obj2_val}")

        threshold = 0.4  # You can adjust this threshold based on your requirement
        res = []
        if obj1_val >= threshold:
            h, w = object1.shape[:2]
            obj1 = OnScreenObject(_object1, obj1_loc[0], obj1_loc[1], obj1_loc[0] + w, obj1_loc[1] + h)
            cv2.rectangle(screenshot, obj1_loc, (obj1_loc[0] + w, obj1_loc[1] + h), (255, 0, 55), 3)
            res.append(obj1)

        if obj2_val >= threshold:
            h, w = object2.shape[:2]
            obj2 = OnScreenObject(_object2, obj2_loc[0], obj2_loc[1], obj2_loc[0] + w, obj2_loc[1] + h)
            cv2.rectangle(screenshot, obj2_loc, (obj2_loc[0] + w, obj2_loc[1] + h), (0, 0, 255), 3)

            res.append(obj2)
        
        cv2.imshow('Screen', screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return res