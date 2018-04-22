# house-annotator
tools to help with zillow houses


When using the python-zillow package, must change function Place.set\_data and add the following lines at the start of the function:
```
    if isinstance(source_data, list):
        source_data = source_data[0]
```

This is because the data in ['response']['results']['result'] for the Deep Search Results returns two entries if there are two posts for the same property.
