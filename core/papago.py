import os
import sys
import json
import urllib.request

class Papago:
    def __init__(self, client_id="tBx3EbbN6U66M8XG4yvj", client_secret="dPFiBXCDE5"):
        self.client_id = client_id
        self.client_secret = client_secret
        
    def ko2en_translate(self, text):
        return self.predict(text, 'ko', 'en')
    
    def en2ko_translate(self, text):
        return self.predict(text, 'en', 'ko')
    
    def predict(self, text, source='ko', target='en'):
        encText = urllib.parse.quote(text)
        data = "source={}&target={}&text={}".format(source, target, encText)
        
        request = urllib.request.Request("https://openapi.naver.com/v1/papago/n2mt")
        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)

        response = urllib.request.urlopen(request, data=data.encode("utf-8"))

        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body.decode('utf-8'))
            return results['message']['result']['translatedText']
        else:
            return None