import json
import requests

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

if __name__ == '__main__':
    obj = Twinword()
    print(obj.get('hello'))

