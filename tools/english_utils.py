
def remove_wrong_keyword(data):
    lowered_data = data.lower()
    lowered_alphabet = 'abcdefghijknmlopqrstuvwxyz'

    start_index = 0
    end_index = len(data)

    cond_fn = lambda i: lowered_data[i] in lowered_alphabet
    
    # find start index (->)
    for i in range(len(data) - 1):
        # If this is alphabet, loop statement is finished. 
        if cond_fn(i):
            break
        
        if not cond_fn(i) and cond_fn(i + 1):
            start_index = i + 1
            break

    # find end index (<-)
    # if cond_fn(data[-1]):
    #     end_index = len(data)
    # else:
    for i in range(len(data))[::-1]:
        if cond_fn(i):
            end_index = i + 1
            break
        
        elif cond_fn(i - 1) and not cond_fn(i):
            end_index = i
            break

    # print(start_index, end_index)
    return data[start_index:end_index]

def remove_kindle_option(data):
    if 'Kindle' in data:
        data = data.replace('\n\n' + data.split('\n\n')[-1], '')
    
    return data

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

def check_english_sentence(data):
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
        return True
    return False

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