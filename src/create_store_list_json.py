import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
import pandas as pd
import os
from time import sleep

from config.secrets import APIKEY

SRC_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.split(SRC_PATH)[0]

from resources.json_components import out_start_str, out_end_str, store_str


def join_addrs(x):
    return '{} {} {}'.format(*x)


def convert_store_address():
    # Read stores data
    path = os.path.split(os.path.dirname(__file__))[0]
    store_list_fn = os.path.join(path, 'new-store-list.tsv')

    # TODO: FIX COLUMNS

    columns = ['name', 'street', 'city', 'state']
    store_list_df = pd.read_csv(store_list_fn, sep='\t', names=columns)
    store_list_df.fillna('', inplace=True)
    store_list_df = store_list_df.sort_values(['name'])
    store_list_df['address'] = store_list_df[['street', 'city', 'state']].apply(join_addrs, axis=1)
    print(store_list_df.columns.to_list())
    print(store_list_df.head())

    # create store list json
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = GoogleV3(api_key=APIKEY)
    n_stores = store_list_df.shape[0]
    print('Number of stores in file:', n_stores)
    store_addrs = []
    stores_without_location = 0
    for storeid in range(n_stores):
        prop = {
            'category': 'grocery',
            'description': '',
            'name': '',
            'address': '',
            'phone': '',
            'website': '',
            'storeid': 0,
            'lat': 0,
            'long': 0
        }
        id = str(storeid + 1).zfill(3)
        prop['storeid'] = id
        prop['name'] = store_list_df.iloc[storeid]['name']
        prop['address'] = store_list_df.iloc[storeid].address
        try:
            location = geolocator.geocode(prop['address'])
            # location = geolocator.geocode(prop['address'], timeout=5)
            prop['lat'] = location.latitude
            prop['long'] = location.longitude
        except Exception as e:
            stores_without_location += 1
            print(e)
            print('No address for:', prop['name'])
            print(prop['address'])
        store_addrs.append(store_str.format(**prop))
        sleep(0.5)

    json_file = out_start_str + ','.join(store_addrs) + out_end_str
    print('-' * 50)
    print(json_file)
    print('-' * 50)
    print('Did not find location for {} stores'.format(stores_without_location))
    out_fn = os.path.join(PROJECT_PATH, 'resources', 'results.json')
    with open(out_fn, 'w') as f:
        f.write(json_file)
    return json_file


def get_address_coordinates(address):
    """ Use google API to get the longitude and latitude of an address """
    lat = 0
    long = 0
    return lat, long


if __name__ == '__main__':
    convert_store_address()
