import pandas as pd
import os
import re

"""
- Update store list
  * after the previous section run, the `update store`  
  * run `exel_to_html_list.py`, this should create/update a file `new_stores.html`  
    * Note that the Excel `new-store-list.xlsx` should contain columns  
      ['name', 'address', 'longitude', 'latitude', 'state', 'city']  
    * Open the [Cult Crackers shopify site](https://cult-crackers.myshopify.com/admin)   
    * Navigate to [Online Store] -> [Themes] -> [Action] -> [Edit Code] -> [static-page-find-us.liquid]   
    * Replace the current stores list HTML, below `<div class="no-mobile-view" id="mobilesizes">`,
      and before `{{ page.content }}` with the code in `new_stores.html` 
    * Click [Preview] to verify that it looks OK
    * Save and exit   
"""

pd.set_option('display.max_columns', 30)
START_HTML = '''\
<!-- Start store HTML Code -->
<div class="no-mobile-view" id="mobilesizes">   
\t<div class="grid-locations">
\t\t<div class="grid-column" style="padding: 0px, 10px, 0px, 10px"></div>
\t</div>\n'''

STATE_HTML = '\t\t\t\t\t<div class="find-us-state-tall">{}</div>'

ROW_HTML = '\t<div class="grid-locations">'
COL_START = '\t\t<div class="grid-column">'
COMMENT_COL_START = '\n\t\t<!-- Column {} Content Starts here -->'
COMMENT_COL_END = '\t\t<!-- Column {} Content Ends here -->'
LIST_START_HTML = '	\t\t<ul class="aaa">\n'

CITY_1ST_STORE_HTML = '''\
\t\t\t\t\t<div class="find-us-city-mid">{city}</div>
\t\t\t\t\t<div class="find-us-name-short">{name}</div>
\t\t\t\t\t<div class="find-us-address">{address}</div>'''

STORE_HTML = '''\
\t\t\t\t\t<div class="find-us-name">{name}</div>
\t\t\t\t\t<div class="find-us-address">{address}</div>'''

SRC_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.split(SRC_PATH)[0]


def read_excel():
    path = os.path.split(os.path.dirname(__file__))[0]
    store_list_fn = os.path.join(path, r'resources', r'new-store-list.xlsx')
    assert os.path.isfile(store_list_fn)
    print('Reading ', store_list_fn)
    try:
        store_list_df = pd.read_excel(store_list_fn, engine='openpyxl')
    except Exception as e:
        print('Make sure that all the States and Cities columns are populated...')
    store_list_df = store_list_df.iloc[:, :6].dropna()
    store_list_df = store_list_df.sort_values(['state', 'city', 'name', 'address'])
    store_list_df['store'] = store_list_df.city + store_list_df.name + store_list_df.address
    assert store_list_df.columns.to_list() == ['name', 'address', 'longitude', 'latitude', 'state', 'city', 'store']
    store_list_df = store_list_df[['name', 'address', 'state', 'city', 'store']]
    g = store_list_df.groupby('state')['store'].nunique()
    store_list_df = store_list_df.merge(g, on='state')
    store_list_df.rename(columns={'city_x': 'city', 'store_y': 'n_stores', 'address': 'addr'}, inplace=True)
    store_list_df['address'] = store_list_df.addr.apply(remove_zip)
    return store_list_df[['name', 'address', 'state', 'city', 'n_stores']]


def remove_zip(s):
    p = re.match('(.*) ([0-9]{5}.*)', s)
    if p:
        return p.group(1)
    else:
        return s


class BuildStoresHTML:

    def __init__(self):
        self.params = dict()
        self.stores_html = [START_HTML]

    def update_params(self, name='', address='', state='', city=''):
        self.params['name'] = name if name else self.params['name']
        self.params['address'] = address if address else self.params['address']
        self.params['state'] = state if state else self.params['state']
        self.params['city'] = city if city else self.params['city']
        return self.params

    def end_section(self, col_count):
        self.stores_html.append('\t\t\t</ul>')
        self.stores_html.append('\t\t</div>')
        self.stores_html.append(COMMENT_COL_END.format(col_count))

    def create_stores_html(self, df, save_to_file=False):
        """
        This function creates a stores HTML that can be copied to the shopify store

        - If a state have 3 or more cities, show the state in a single row section with 3 columns
          In such case you need to start section with MULTI_COL_STATE_START
        - Is a state have less than 3 stores, use STATE_HTML

        """
        current_state = ''
        current_city = ''
        col_count = 1
        store_count = 0
        for i in range(df.shape[0]):
            [name, address, state, city, n_stores] = df.iloc[i, :].to_list()
            self.update_params(name, address, state, city)
            if state != current_state:
                # new state
                row_count = 0

                current_state = state
                if n_stores > 5:
                    # if a store is in 6 or more stores it is by itself
                    r = 0
                    r1 = (n_stores // 3) + ((n_stores % 3) > 0) * 1
                    r2 = (n_stores // 3) + ((n_stores % 3) == 2) * 1
                    r3 = (n_stores // 3)
                    col_count = 1
                    multi_col_state = True
                else:
                    r = n_stores
                    r1 = 0
                    r2 = 0
                    r3 = 0
                    multi_col_state = False

            # Fixme: does not appear to add proper breaks, avoid adding empty sections, close ROW_HTML
            # Column start
            if row_count == 0:
                # Start new Column
                if col_count == 1:
                    self.stores_html.append(ROW_HTML)
                self.stores_html.append(COMMENT_COL_START.format(col_count))
                self.stores_html.append(COL_START)
                self.stores_html.append(LIST_START_HTML)

            self.stores_html.append('\t\t\t\t<li>')
            if row_count == 0:
                if multi_col_state and col_count != 2:
                    self.stores_html.append(STATE_HTML.format(' - '))
                else:
                    self.stores_html.append(STATE_HTML.format(self.params['state']))

            if city != current_city or row_count == 0:
                current_city = city
                self.stores_html.append(CITY_1ST_STORE_HTML.format(**self.params))
            else:
                self.stores_html.append(STORE_HTML.format(**self.params))
            self.stores_html.append('\t\t\t\t</li>\n')

            # Adjust row counting
            # print(current_state, col_count, row_count)
            row_count += 1
            store_count += 1
            if col_count == 1 and (row_count == r1 or row_count == r):
                row_count, col_count = 0, 2
                self.end_section(1)
            elif col_count == 2 and (row_count == r2 or row_count == r):
                row_count, col_count = 0, 3
                self.end_section(2)
            elif col_count == 3 and (row_count == r3 or row_count == r):
                row_count, col_count = 0, 1
                self.end_section(3)
                self.stores_html.append('\t</div>\n')

        # End the HTML
        self.stores_html.append('\t</div>')
        self.stores_html.append('</div>')

        assert store_count == df.shape[0], 'Did not process all stores...\n'

        stores_html = '\n'.join(self.stores_html)
        if save_to_file:
            out_fn = os.path.join(PROJECT_PATH, 'resources', 'new_stores.html')
            with open(out_fn, 'w') as f:
                f.write(stores_html)
            print(f'Save HTML Code to {out_fn}')
        else:
            print('-' * 40)
            for l in stores_html.splitlines():
                print(l)
            print('-' * 40)
        return stores_html


if __name__ == '__main__':
    o = BuildStoresHTML()
    df = read_excel()
    stores_html = o.create_stores_html(df, save_to_file=True)
