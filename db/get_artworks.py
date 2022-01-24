import requests
import json
from pprint import pprint


def get_artwork_ids():
    response = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects')
    response_json = response.json()
    object_ids = response_json['objectIDs']
    return len(object_ids)


def add_to_json(all_artwork_info):
    with open('artwork_info.json', 'w') as file:
        json.dump(all_artwork_info, file)


def get_single_artwork_info(artwork_id):
    response = requests.get(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{artwork_id}')
    response_json = response.json()
    is_public_domain = response_json['isPublicDomain']
    if is_public_domain:
        return response_json
    return False


def get_all_artwork_info(object_ids):
    all_artwork_info = []
    for artwork_id in object_ids:
        single_artwork_info = get_single_artwork_info(artwork_id)
        if single_artwork_info is not False:
            all_artwork_info.append(single_artwork_info)
    return all_artwork_info


def main():
    artwork_ids = get_artwork_ids()
    all_artwork_info = get_all_artwork_info(artwork_ids)
    add_to_json(all_artwork_info)


if __name__ == '__main__':
    main()
