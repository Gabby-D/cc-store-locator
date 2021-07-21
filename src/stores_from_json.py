import json
import os

SRC_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.split(SRC_PATH)[0]


def json_to_tsv():
    fn = os.path.join(PROJECT_PATH, 'store-locator', 'cultcrackers_stores.json')
    with open(fn) as f:
        data = json.load(f)

    data = data.get('features')
    out_data = [['name', 'address', 'longitude', 'latitude']]
    for x in data:
        (longitude, latitude) = x['geometry']['coordinates']
        store_name = x['properties']['name']
        address = x['properties']['address'].replace('\t', ' ').replace('  ', ' ')
        out_data.append([store_name, address, str(longitude), str(latitude)])

    out_data = ['\t'.join(x) for x in out_data]
    out_file = os.path.join(PROJECT_PATH, "resources", "store_list.tsv")
    with open(out_file, 'w') as f:
        f.write('\n'.join(out_data))
    print(f'Saved data to {out_file}')
    print('Done')


if __name__ == '__main__':
    json_to_tsv()
