def dict_clean(dictionary):
    for k, v in dictionary.items():
        if v is '':
            dictionary[k] = None
    return dictionary
