import os
import sys
import json

import requests
import urllib.request

import queue
import multiprocessing as mp

from tools.json_utils import read_json

from tools.english_utils import check_english_sentence
from tools.english_utils import *

# Interpret english word to english explanation
class Google_Dictionary:
    def __init__(self, version='v3'):
        self.searching_format = f'http://api.dictionaryapi.dev/api/{version}' + '/entries/en/{}'

    def get_url(self, word):
        return self.searching_format.format(word)

    def get(self, word):
        url = self.get_url(word)
        response = requests.get(url)

        results = json.loads(response.text)
        # results = json.dumps(results, indent='\t', ensure_ascii=False)

        """
        [
            {
                    "word": "decide",
                    "phonetics": [
                            {
                                    "text": "/dəˈsaɪd/",
                                    "audio": "https://lex-audio.useremarkable.com/mp3/decide_us_1.mp3"
                            }
                    ],
                    "meaning": {
                            "transitive verb": [
                                    {
                                            "definition": "Come to a resolution in the mind as a result of consideration.",
                                            "synonyms": [
                                                    "form the opinion",
                                                    "come to the conclusion",
                                                    "conclude",
                                                    "decide",
                                                    "determine"
                                            ],
                                            "example": "they decided to appoint someone else"
                                    }
                            ]
                    }
            }
        ]
        """
        return results

# Interpret english word to english explanation aend korean expression
class Twinword:
    def __init__(self, client_id, client_secret):
        self.headers = {
            'x-rapidapi-host': client_id,
            'x-rapidapi-key': client_secret
        }

        self.url_format = "https://twinword-word-graph-dictionary.p.rapidapi.com/{}/"
        self.class_names = ['definition_kr', 'example']

    def get(self, word, class_names=None):
        if class_names is None: 
            class_names = self.class_names

        results = {}
        querystring = {"entry":word}
        
        if 'definition_kr' in class_names:
            url = self.url_format.format('definition_kr')
            response = requests.request("GET", url, headers=self.headers, params=querystring)

            data = json.loads(response.text)
            # data = json.dumps(data, indent='\t')

            if 'meaning' in data:
                results['meaning'] = data['meaning']
                results['meaning']['korean'] = data['meaning']['korean']
            
            # ipa is UK style.
            # if 'ipa' in data:
            #     results['phonetic'] = data['ipa']

        if 'example' in class_names:
            url = self.url_format.format('example')
            response = requests.request("GET", url, headers=self.headers, params=querystring)

            data = json.loads(response.text)

            if 'example' in data:
                results['example'] = data['example']

        return results

# Translate english word or sentence
class Papago:
    def __init__(self, client_ids, client_secrets):
        self.client_ids = client_ids
        self.client_secrets = client_secrets
        
    def get(self, text):
        is_english = check_english_sentence(text)

        if is_english:
            result = self.predict(text, 'en', 'ko')
        else:
            result = self.predict(text, 'ko', 'en')

        return result
    
    def predict(self, text, source='ko', target='en'):
        encText = urllib.parse.quote(text)
        data = "source={}&target={}&text={}".format(source, target, encText)
        
        for client_id, client_secret in zip(self.client_ids, self.client_secrets):
            try:
                request = urllib.request.Request("https://openapi.naver.com/v1/papago/n2mt")
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)

            
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            
                rescode = response.getcode()
                if rescode == 200:
                    response_body = response.read()
                    results = json.loads(response_body.decode('utf-8'))
                    return results['message']['result']['translatedText']
                else:
                    return None
            except:
                pass

class Manager(mp.Process):
    def __init__(self, print_fn):
        super().__init__()

        # self.daemon = True
        self.print_fn = print_fn

        self.info_dic = read_json('./data/private_information.json')

        self.papago = Papago(**self.info_dic['papago'])
        self.twinword = Twinword(**self.info_dic['twinword'])
        self.google_dict = Google_Dictionary()

        self.queue = mp.Queue(maxsize=50)

    def push(self, text):
        self.queue.put(text)
    
    def run(self):
        while True:
            text = self.queue.get()

            result = self.google_dict.get(text)
            self.print_fn(result)
            
            # if check_string_type(text):
            #     text = preprocessing_for_string(text)

            #     if len(text) > 0:
            #         # 1. word or sentence
            #         if check_sentence_or_word(text):
            #             # 1.1. [sentence] korean or english
            #             if check_korean_sentence(text):
            #                 result = self.papago.ko2en_translate(text)
            #             else:
            #                 result = self.papago.en2ko_translate(text)

            #         else:
            #             # 2.1. [Word] korean or english
            #             if check_korean_sentence(text):
            #                 result = self.papago.ko2en_translate(text)
            #                 result = self.twinword.get(result)
            #             else:
            #                 result = self.twinword.get(text)

            #         self.print_fn(result)