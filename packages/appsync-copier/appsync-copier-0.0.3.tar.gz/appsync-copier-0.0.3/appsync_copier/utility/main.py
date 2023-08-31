def singular_to_plural(input_word: str):
    if input_word.endswith('y'):
        return input_word[:-1] + 'ies'
    elif input_word.endswith('s'):
        return input_word + 'es'
    else:
        return input_word + 's'
