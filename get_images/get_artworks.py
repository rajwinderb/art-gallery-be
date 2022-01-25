import requests


def get_artwork_ids(formatted_search):
    response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/search?q={formatted_search}')
    response_json = response.json()
    object_ids = response_json['objectIDs'] if response_json['objectIDs'] is not None else []
    return object_ids


def get_single_artwork_info(artwork_id):
    response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{artwork_id}')
    response_json = response.json()
    is_public_domain = response_json['isPublicDomain']
    wanted_keys = ['objectID', 'isHighlight', 'primaryImage', 'primaryImageSmall', 'department', 'objectName', 'title',
                   'culture', 'period', 'dynasty', 'artistPrefix', 'artistDisplayName', 'artistDisplayBio',
                   'artistGender', 'objectDate', 'medium', 'country', 'classification', 'linkResource', 'tags']
    return_data = {wanted_key: response_json[wanted_key] for wanted_key in wanted_keys}
    if is_public_domain and return_data['primaryImage'] != "":
        return return_data
    return False


def get_all_artwork_info(artwork_ids):
    all_artwork_info = []
    artwork_ids = artwork_ids[:15] if len(artwork_ids) > 15 else artwork_ids
    for artwork_id in artwork_ids:
        single_artwork_info = get_single_artwork_info(artwork_id)
        if single_artwork_info is not False:
            all_artwork_info.append(single_artwork_info)
    return all_artwork_info


def get_from_search(search_term):
    formatted_search = search_term.replace(" ", "+")
    artwork_ids = get_artwork_ids(formatted_search)
    artwork_ids = artwork_ids[:15] if len(artwork_ids) > 15 else artwork_ids
    all_artwork_info = get_all_artwork_info(artwork_ids)
    return all_artwork_info


def main():
    search_term = input("Search term: ")
    print(get_from_search(search_term))


if __name__ == '__main__':
    main()
