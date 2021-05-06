import os
import sys

filepath = os.path.dirname(__file__)
filepath = os.path.abspath(filepath)

sys.path.append(os.path.dirname(filepath))

import cv2
import time

from core import english_modules

if __name__ == '__main__':
    crawler = english_modules.NAVER_Dictionary_Crawler(image_dir='./data/images/', chrome_path='./data/chromedriver.exe', delay=1.0)

    while True:
        word = input('# Word ? ')

        image_path = crawler(word)
        if image_path is not None:
            image = cv2.imread(image_path)
            
            cv2.imshow('NAVER', image)
            cv2.waitKey(0)
            cv2.destroyWindow('NAVER')
