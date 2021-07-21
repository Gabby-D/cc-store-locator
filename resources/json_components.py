out_start_str = '''\
{
    "type": "FeatureCollection",
    "features": [
'''

out_end_str = '''\
    ]
}
'''

store_str = '''\
        {{
            "geometry": {{
                "type": "Point",
                "coordinates": [{long}, {lat}]
            }},
            "type": "Feature",
            "properties": {{
                "category": "{category}",
                "description": "{description}",
                "name": "{name}",
                "address": "{address}",
                "phone": "{phone}",
                "website": "{website}",
                "storeid": "{storeid}"
            }}
       }}
'''