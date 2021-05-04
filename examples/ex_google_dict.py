import os
import sys

filepath = os.path.dirname(__file__)
filepath = os.path.abspath(filepath)

sys.path.append(os.path.dirname(filepath))

from core.english_modules import Google_Dictionary

model = Google_Dictionary()

# results = model.get('have')
results = model.get('had')
print(results, len(results))