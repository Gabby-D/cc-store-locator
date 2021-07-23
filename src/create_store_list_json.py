import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
import pandas as pd
import os
from time import sleep

pd.set_option('display.max_columns',30)

from config.secrets import APIKEY

SRC_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.split(SRC_PATH)[0]

from resources.json_components import out_start_str, out_end_str, store_str


def join_addrs(x):
    return '{} {} {}'.format(*x)


def convert_store_address():
    # Read stores data
    path = os.path.split(os.path.dirname(__file__))[0]
    store_list_fn = os.path.join(path, r'resources', r'new-store-list.xlsx')

    # TODO: FIX COLUMNS

    # columns = ['name', 'street', 'city', 'state']
    # store_list_df = pd.read_csv(store_list_fn, sep='\t', header=0)
    assert os.path.isfile(store_list_fn)
    print('Reading ',store_list_fn)
    store_list_df = pd.read_excel(store_list_fn, engine='openpyxl')

    # store_list_df.fillna('', inplace=True)
    # store_list_df.dropna('', inplace=True)
    store_list_df = store_list_df.iloc[:, :4].dropna()
    store_list_df = store_list_df.sort_values(['name'])
    # store_list_df['address'] = store_list_df[['street', 'city', 'state']].apply(join_addrs, axis=1)
    print(store_list_df.columns.to_list())
    print(store_list_df.head())
    assert store_list_df.columns.to_list() == ['name', 'address', 'longitude', 'latitude']

    # create store list json
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = GoogleV3(api_key=APIKEY)
    n_stores = store_list_df.shape[0]
    print('Number of stores in file:', n_stores)
    store_addrs = []
    stores_without_location = 0
    i = 1
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
        id = str(i).zfill(3)
        prop['storeid'] = id
        prop['name'] = store_list_df.iloc[storeid]['name']
        prop['address'] = store_list_df.iloc[storeid].address
        prop['lat'] = store_list_df.iloc[storeid].latitude
        prop['long'] = store_list_df.iloc[storeid].longitude
        if not prop['long']:
            try:
                location = geolocator.geocode(prop['address'])
                # location = geolocator.geocode(prop['address'], timeout=5)
                prop['lat'] = location.latitude
                prop['long'] = location.longitude
                sleep(0.5)
            except Exception as e:
                stores_without_location += 1
                print(e)
                print('No address for:', prop['name'])
                print(prop['address'])
        if prop['long']:
            store_addrs.append(store_str.format(**prop))
            i += 1

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
