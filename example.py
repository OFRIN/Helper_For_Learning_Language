
# 1. keyboard and mouse
# from core.mouse_api import Customized_Mouse_API
# from core.keyboard_api import Customized_Keyboard_API

# keyboard = Customized_Keyboard_API()

# functions = {
#     'drag' : lambda: keyboard.copy(),
#     'left_up' : lambda: print('left_up'),
#     'right_up' : lambda: print('right_up'),
#     'double_click' : lambda: keyboard.copy()
# }
# mouse = Customized_Mouse_API(functions)

# while True:
#     pass

# 2. translate using Papago
# from core.papago import Papago

# from utility import *

# model = Papago()

# while True:
#     sentence = input('sentence ? ')

#     if not check_string_type(sentence):
#         print('error')
#         continue

#     if check_sentence_or_word(sentence):
#         if check_korean_sentence(sentence):
#             translated_sentence = model.ko2en_translate(sentence)
#         else:
#             translated_sentence = model.en2ko_translate(sentence)

#         print('# Translation using Papago')
#         print(sentence)
#         print(translated_sentence)
    
#     else:
#         print('Word')


# 3. Naver Dictionary
import requests
from bs4 import BeautifulSoup

class Naver_Translator:
    def __init__(self):
        self.url = "http://endic.naver.com/search.nhn?query="
    
    def get(self, word):
        response = requests.get(self.url + word)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # print(soup.prettify())
        open('example.html', 'w').write(soup.prettify())
        
        try:
            result = soup.find('dl', {'class':'list_e2'}).find('dd').find('span', {'class':'fnt_k05'}).get_text()
            # result = soup.find('dl', {'class':'list_e2'}).find('dd').get_text()
        except:
            result = None
        
        return result

obj = Naver_Translator()
print(obj.get('선호하다'))