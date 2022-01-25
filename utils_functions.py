def dict_clean(dictionary):
    for k, v in dictionary.items():
        if v == '':
            dictionary[k] = None
    return dictionary
