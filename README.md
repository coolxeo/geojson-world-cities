# European Cities Filter

This script filters a GeoJSON file of cities to keep only those located in Europe.

## Requirements

- Python 3.6+
- No external dependencies required (uses only the standard library)

## Usage

1. Make sure your `cities.geojson` file is in the same directory as the script.
2. Run the script:

```bash
python filter_european_cities.py
```

3. The script will create a new file called `european_cities.geojson` containing only cities in Europe.

## How it works

The script uses two methods to identify European cities:

1. By country name - if the GeoJSON has a 'country' property, it checks if the country is in the list of European countries.
2. By geographic coordinates - it uses a bounding box to determine if a city's coordinates fall within Europe.

The bounding box used is a rough approximation of Europe's boundaries: longitude between -25° and 40°, and latitude between 34° and 72°. 