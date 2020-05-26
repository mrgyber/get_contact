import base64
import random
import re
import os
import string

import numpy as np
import pytesseract
import cv2


class CaptchaDecode:
    def __init__(self):
        pass

    def decode_response(self, response):
        image_b64 = response['result']['image']
        image_data = base64.b64decode(image_b64)
        path = 'captcha/' + ''.join([random.choice(string.ascii_letters) for _ in range(10)]) + '.jpg'
        with open(path, 'wb') as f:
            f.write(image_data)
        return self.decrypt(path), path

    @staticmethod
    def decrypt(path):
        frame = cv2.imread(path)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, np.array([30, 120, 0]), np.array([255, 255, 255]))
        text = pytesseract.image_to_string(mask)
        text = re.sub("[^A-Za-z0-9]", '', text)

        os.remove(path)

        return text
