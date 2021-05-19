import os
import sys

filepath = os.path.dirname(__file__)
filepath = os.path.abspath(filepath)

sys.path.append(os.path.dirname(filepath))

from tools import english_utils

for input_string in [
        '  word, ',
        'string ',
        ' string',
        ' string; string; ',
        'I have to refine the words,',
        ';; I have to refine the words,,;',
        'belongs to',
        'to belongs',
        'to belongs from'
    ]:
    refined_string = english_utils.remove_wrong_keyword(input_string)
    print('\"{}\"'.format(input_string), "->", '\"{}\"'.format(refined_string))


