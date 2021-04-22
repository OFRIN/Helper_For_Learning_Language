import json
import requests

class Google_Dictionary:
    def __init__(self):
        self.get_url_fn = lambda word: 'http://api.dictionaryapi.dev/api/v3/entries/en/{}'.format(word)

    def get(self, word):
        url = self.get_url_fn(word)
        response = requests.get(url)

        results = json.loads(response.text)
        results = json.dumps(results, indent='\t')

        print(results)

