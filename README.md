# convert-store-addresses
Convert a CSV/TSV store address data to JSON formatted for a google map

### References:
#### Creating Google cloud bucket and copy code into it

### Update store list
When changing the stores follow this process:
- update stores map 
  * Download the google sheet to an `xlsx` file 
  * change name to `new-store-list.xlsx`
  * copy the new file into `C:\Users\gabby\Projects\cc-store-locator\resources`   
  * run `create_store_list_json.py`  should create new "results.json"
  * open `results.json` copy into `cultcrackers_stores.json` replacing everything in it
  * push to git (right click `cc-store-locator` choose [git] -> [commit directory] -> [commit and push] -> [push])
  * go to [Google cloud consul](https://shell.cloud.google.com/?hl=en_US&fromcloudshell=true&show=ide%2Cterminal) 
  * you might need to clink (reconnect) 
  * type in `cd cc-store-locator/store-locator/` 
  * type in `git reset -- hard` and then `git pull`   
  * then type 
    - `gcloud config set project cc-store-locator` authorize
    - if you do it for the first time, type: `gsutil mb gs://cult-crackers-store-locator` 
    - `gsutil defacl ch -u AllUsers:R gs://cult-crackers-store-locator`
    - `gsutil -h "Cache-Control:no-cache" -m cp * gs://cult-crackers-store-locator`  
  * to check go to Store locator link: 
    `https://storage.googleapis.com/cult-crackers-store-locator/index.html` 

### Update store list
- Update store list
  * If you haven't done so, download the google sheet to an `xlsx` file 
  * change name to `new-store-list.xlsx`
  * copy the new file into `C:\Users\gabby\Projects\cc-store-locator\resources`   
  * Note that the Excel `new-store-list.xlsx` should contain columns  
      ['name', 'address', 'longitude', 'latitude', 'state', 'city']  
  * run `exel_to_html_list.py`, this should create/update a file `new_stores.html`
    * Open the [Cult Crackers shopify site](https://cult-crackers.myshopify.com/admin)   
    * Navigate to [Online Store] -> [Themes] -> [Action] -> [Edit Code] -> [static-page-find-us.liquid]   
    * Replace the current stores list HTML, below `<div class="no-mobile-view" id="mobilesizes">`,
      and before `{{ page.content }}` with the code in `new_stores.html`  
      **before replacing, copy the existing code to `backup_store_list.html` in case you need to revert to old list**  
    * Click [Preview] to verify that it looks OK
    * Save and exit   

### Process
get the store info file as a TSV, put it in the code 
running the code will print the Stores list JSON 

### Links to help
- [places](https://developers.google.com/maps/documentation/javascript/places) 
- [listing-objects](https://cloud.google.com/storage/docs/listing-objects) 
- [simple-store-locator](https://console.cloud.google.com/storage/browser/cultcrackers-store-locator?project=simple-store-locator-264304) 
- [google-maps-simple-store-locator](https://codelabs.developers.google.com/codelabs/google-maps-simple-store-locator/#6)

