from word_forms.lemmatizer import lemmatize
from word_forms.word_forms import get_word_forms

# print(lemmatize("revealing"))
# print(lemmatize("stood"))
print(lemmatize("reveling"))

data_dict = get_word_forms('stood')
print(data_dict)