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

1. By city name - if the city name is in a predefined list of known European cities, it's included.
2. By geographic coordinates - it uses a polygon that approximates Europe's borders to determine if a city's centroid falls within Europe.

The polygon-based approach is more accurate than a simple bounding box, as it follows the general shape of Europe's borders, including the Mediterranean coastline, the Atlantic coast, and the borders with Asia.

## Polygon Definition

The Europe polygon is defined by the following points (longitude, latitude):

```
[
    (-10.0, 35.0),  # Southwest corner (Atlantic)
    (-10.0, 60.0),  # Northwest corner
    (-5.0, 65.0),   # Iceland area
    (0.0, 70.0),    # Northern Norway
    (30.0, 72.0),   # Northern Russia
    (40.0, 65.0),   # Eastern Russia
    (40.0, 45.0),   # Black Sea area
    (35.0, 35.0),   # Turkey/Cyprus
    (25.0, 35.0),   # Mediterranean
    (10.0, 35.0),   # North Africa coast
    (-10.0, 35.0)   # Back to start
]
```

This polygon is a simplified representation of Europe's borders and may not be perfectly accurate for all edge cases. 