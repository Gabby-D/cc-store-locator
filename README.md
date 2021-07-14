# convert-store-adresses
Convert a CSV/TSV store address data to JSON formatted for a google map

### References:
#### Creating Google cloud bucket and copy code into it 
- `gsutil mb gs://cultcrackers-store-locator` 
- `gsutil defacl ch -u AllUsers:R gs://cultcrackers-store-locator`
- `gsutil -h "Cache-Control:no-cache" -m cp * gs://cultcrackers-store-locator`

Store locator link: 
`http://storage.googleapis.com/cultcrackers-store-locator/index.html` 

### Process
get the store info file as a TSV, put it in the code 
running the code will print the Stores list JSON 

### Links to help
- https://developers.google.com/maps/documentation/javascript/places 
- https://cloud.google.com/storage/docs/listing-objects 
- https://console.cloud.google.com/storage/browser/cultcrackers-store-locator?project=simple-store-locator-264304 
- https://codelabs.developers.google.com/codelabs/google-maps-simple-store-locator/#6

\