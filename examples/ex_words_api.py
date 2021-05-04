import os
import sys

filepath = os.path.dirname(__file__)
filepath = os.path.abspath(filepath)

sys.path.append(os.path.dirname(filepath))

from core.english_modules import WordsAPI

from tools.json_utils import read_json
from tools.json_utils import dict_to_json

info_dic = read_json('./data/private_information.json')
model = WordsAPI(**info_dic['wordsapi'])

# results = model.get('empty')
# results = model.get('stand')
results = model.get('reveling')
print(dict_to_json(results))

