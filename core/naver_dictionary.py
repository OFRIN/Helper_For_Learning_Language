# Copyright (C) 2020 * Ltd. All rights reserved.
# author : Sanghyeon Jo <josanghyeokn@gmail.com>

import requests
from bs4 import BeautifulSoup

class Naver_Translator:
    def __init__(self):
        self.url = "http://endic.naver.com/search.nhn?query="
        
    def get(self, word):
        response = requests.get(self.url + word)
        soup = BeautifulSoup(response.content, "lxml")
        
        try:
            result = soup.find('dl', {'class':'list_e2'}).find('dd').findall('span', {'class':'fnt_k05'}).get_text()
        except:
            result = None

        return result

