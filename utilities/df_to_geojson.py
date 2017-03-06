"""Converts pandas DataFrame to geojson."""
import json


def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    """Create a new python dict to contain our geojson data, using geojson format."""
    # Geojson template to fill
    geojson = {'type': 'FeatureCollection', 'features': []}

    # Drop any rows that lack lat/long data and print resultant row count
    df_geo = df.dropna(subset=[lat, lon], axis=0, inplace=False)
    print('We have {} geotagged rows'.format(len(df_geo)))

    # Loop through each row in the dataframe and convert each row to geojson format
    for i, row in df.iterrows():
        # Create a feature template to fill in
        feature = {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Point',
                'coordinates': []
            }
        }

        # Fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon], row[lat]]

        # For each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]

        # Add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)

    # Save the geojson result to a file
    output_filename = 'output.geojson'
    with open(output_filename, 'w') as output_file:
        output_file.write(json.dumps(geojson))

    # How many features did we save to the geojson file?
    print('{} geotagged features saved to file'.format(len(geojson['features'])))

    return geojson
