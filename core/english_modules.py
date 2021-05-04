import os
import sys
import json

import requests
import urllib.request

import queue
import multiprocessing as mp

from tools.json_utils import read_json

from tools.english_utils import check_english_sentence
from tools.english_utils import check_sentence_or_word

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

# Interpret english word to english explanation and korean expression
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

        # if 'association' in class_names:
        #     url = self.url_format.format('example')
        #     response = requests.request("GET", url, headers=self.headers, params=querystring)

        #     data = json.loads(response.text)

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
                    return ''
            except:
                pass

        return ''

# Interpret english word to english explanation
class WordsAPI:
    """
    # Definitions
    ### url = "https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"

    # Examples
    ### url = "https://wordsapiv1.p.rapidapi.com/words/{word}/examples"

    # Syllables
    ### url = "https://wordsapiv1.p.rapidapi.com/words/{word}/syllables"

    # Synonyms
    ### url = "https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
    """
    def __init__(self, client_id, client_secret):
        self.headers = {
            'x-rapidapi-host': client_id,
            'x-rapidapi-key': client_secret
        }

        self.url_format = "https://wordsapiv1.p.rapidapi.com/words/{}/{}/"
        self.class_names = ['definitions', 'examples', 'synonyms', 'syllables']

    def get(self, word, class_names=None):
        if class_names is None: 
            class_names = self.class_names

        results = {}
        for class_name in class_names:
            url = self.url_format.format(word, class_name)
            response = requests.request("GET", url, headers=self.headers)

            data = json.loads(response.text)
            # data = json.dumps(data, indent='\t')
            
            results[class_name] = data

        return results

class English_Manager:
    def __init__(self, json_path):
        read_json(json_path)