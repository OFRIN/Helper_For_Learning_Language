
from pynput import keyboard

def check_string_type(data):
    if type(data) == type(''):
        if data != '':
            return True
        else:
            return False
    return False

def check_sentence_or_word(data):
    if '.' in data or ',' in data:
        return True
    return False

def check_korean_sentence(data):
    alphabet_large = 'ABCDEFGHIJKNMLOPQRSTUVWXYZ'
    alphabet_lower = alphabet_large.lower()

    numbers = '0123456789'
    special_character = '~!@#$%^&*()_+ '

    en_count, ko_count = 0, 0

    for character in data:
        if character in alphabet_large or character in alphabet_lower \
            or character in numbers or character in special_character:
            en_count += 1
        else:
            ko_count += 1

    if en_count > ko_count:
        return False
    return True

def preprocessing_for_string(data):
    data = data.replace('\n', ' ')

    alphabet_large = 'ABCDEFGHIJKNMLOPQRSTUVWXYZ'
    alphabet_lower = alphabet_large.lower()
    
    for index, character in enumerate(data):
        if character in alphabet_large:
            data = data[index:]
            break

        elif character in alphabet_lower:
            data = character.upper() + data[index+1:]
            break
    
    return data
