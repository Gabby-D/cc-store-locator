# convert-store-adresses
Convert a CSV/TSV store address data to JSON formatted for a google map

### References:
#### Creating Google cloud bucket and copy code into it 
- `gcloud config set project cc-store-locator`
- `cd ~/cc-store-locator/store-locator`
- `gsutil mb gs://cult-crackers-store-locator` 
- `gsutil defacl ch -u AllUsers:R gs://cult-crackers-store-locator`
- `gsutil -h "Cache-Control:no-cache" -m cp * gs://cult-crackers-store-locator`

When changing the stores follow this process:
- update stores  
  * Download the google sheet to an `xlsx` file 
  * copy the new file into   

Store locator link: 
`https://storage.googleapis.com/cult-crackers-store-locator/index.html` 

### Process
get the store info file as a TSV, put it in the code 
running the code will print the Stores list JSON 

### Links to help
- https://developers.google.com/maps/documentation/javascript/places 
- https://cloud.google.com/storage/docs/listing-objects 
- https://console.cloud.google.com/storage/browser/cultcrackers-store-locator?project=simple-store-locator-264304 
- https://codelabs.developers.google.com/codelabs/google-maps-simple-store-locator/#6

\