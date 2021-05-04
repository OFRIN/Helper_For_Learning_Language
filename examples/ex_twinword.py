import os
import sys

filepath = os.path.dirname(__file__)
filepath = os.path.abspath(filepath)

sys.path.append(os.path.dirname(filepath))

from core.english_modules import Twinword

from tools.json_utils import read_json
from tools.json_utils import dict_to_json

info_dic = read_json('./data/private_information.json')
model = Twinword(**info_dic['twinword'])

# results = model.get('empty')
results = model.get('stood')
print(dict_to_json(results))

"""
{'meaning': {'korean': '비우다, 비어 있는, 빈', 'noun': '(nou) a container that has been emptied', 'verb': '(vrb) make void or empty of contents\n(vrb) become empty or void of its content\n(vrb) leave behind empty; move out of\n(vrb) remove\n(vrb) excrete or discharge from the body', 'adverb': '', 'adjective': '(adj) holding or containing nothing\n(adj) devoid of significance or point\n(adj) needing nourishment\n(adj) emptied of emotion'}, 'example': ['I always empty and clean ashtrays and wastebaskets.', 'The higher the resolution the bigger the empty space.', 'The more empty space, the more readily the humidity will drop.', 
'Gases always intermix since free molecules will always move into empty space.', 'On the scale of the clumps within the rings there is much empty space.', 'On the scale of the clumps within the rings there is a lot of empty space.', 'An analogous case concerns the empty conjunction and the empty disjunction.', 'There were empty seats galore.', 'The streets are empty and desolate.', 'They did not empty the cruet.']}
"""

