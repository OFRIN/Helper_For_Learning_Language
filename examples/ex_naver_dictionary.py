import os
import sys

filepath = os.path.dirname(__file__)
filepath = os.path.abspath(filepath)

sys.path.append(os.path.dirname(filepath))

import time
from core.english_modules import NAVER_Dictionary_Downloader

if __name__ == '__main__':
    naver_dict = NAVER_Dictionary_Downloader()

    while True:
        word = input('# Word ? ')
        naver_dict.put(word)

        time.sleep(1)