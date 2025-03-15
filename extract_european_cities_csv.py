#!/usr/bin/env python3
import csv
import json
import sys
import os

# Define European countries
european_countries = {
    'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina',
    'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia',
    'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland',
    'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg',
    'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia',
    'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia',
    'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine',
    'United Kingdom', 'Vatican City'
}

# Define Europe's borders as a polygon (longitude, latitude pairs)
# This is a simplified polygon of Europe's borders
europe_polygon = [
    # Western Europe (Atlantic)
    (-10.0, 35.0),  # Southwest corner
    (-10.0, 60.0),  # Northwest corner
    # Northern Europe
    (-5.0, 65.0),   # Iceland area
    (0.0, 70.0),    # Northern Norway
    (30.0, 72.0),   # Northern Russia
    # Eastern Europe
    (40.0, 65.0),   # Eastern Russia
    (40.0, 45.0),   # Black Sea area
    # Southern Europe
    (35.0, 35.0),   # Turkey/Cyprus
    (25.0, 35.0),   # Mediterranean
    (10.0, 35.0),   # North Africa coast
    (-10.0, 35.0)   # Back to start
]

def point_in_polygon(point, polygon):
    """
    Determine if a point is inside a polygon using the ray casting algorithm.
    
    Args:
        point: A tuple of (longitude, latitude)
        polygon: A list of (longitude, latitude) tuples forming a polygon
        
    Returns:
        bool: True if the point is inside the polygon, False otherwise
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def is_in_europe(lon, lat):
    """Check if a point is in Europe using the polygon."""
    try:
        lon_val = float(lon)
        lat_val = float(lat)
        return point_in_polygon((lon_val, lat_val), europe_polygon)
    except (TypeError, ValueError):
        return False

def is_european_country(country_name):
    """Check if a country name is in the list of European countries."""
    return country_name in european_countries

def parse_coordinates(coord_str):
    """Parse coordinates from string format."""
    try:
        if coord_str:
            parts = coord_str.split(',')
            if len(parts) == 2:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                return lon, lat  # GeoJSON uses [longitude, latitude] order
    except (ValueError, TypeError):
        pass
    return None, None

def main():
    input_file = 'geonames-all-cities-with-a-population-1000@public.csv'
    output_file = 'european_cities.geojson'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    print(f"Processing {input_file}...")
    
    # Create a list to store European city features
    european_features = []
    
    # Process the CSV file
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        # CSV file uses semicolon as delimiter
        reader = csv.DictReader(csvfile, delimiter=';')
        
        row_count = 0
        european_count = 0
        
        for row in reader:
            row_count += 1
            
            # Extract coordinates
            lon, lat = parse_coordinates(row.get('Coordinates', ''))
            
            # Check if the city is in Europe
            is_european = False
            
            # Check by country name
            country_name = row.get('Country name EN', '')
            if country_name and is_european_country(country_name):
                is_european = True
            
            # If coordinates are available and not already determined to be European,
            # check by coordinates
            if not is_european and lon is not None and lat is not None:
                if is_in_europe(lon, lat):
                    is_european = True
            
            # If the city is in Europe, create a GeoJSON feature
            if is_european:
                european_count += 1
                
                # Extract the fields we want
                name = row.get('Name', '')
                country_name = row.get('Country name EN', '')
                alternate_names = row.get('Alternate Names', '')
                population = row.get('Population', '0')
                country_code = row.get('Country Code', '')
                
                # Create a GeoJSON feature
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [lon, lat]
                    },
                    'properties': {
                        'name': name,
                        'country_name': country_name,
                        'alternate_names': alternate_names,
                        'population': int(population) if population.isdigit() else 0,
                        'country_code': country_code
                    }
                }
                
                european_features.append(feature)
                
                # Print progress every 1000 features
                if european_count % 1000 == 0:
                    print(f"Processed {row_count} rows, found {european_count} European cities so far...")
    
    # Create the GeoJSON structure
    geojson = {
        'type': 'FeatureCollection',
        'features': european_features
    }
    
    # Save the GeoJSON file
    print(f"Saving {european_count} European cities to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    
    print(f"Done! Processed {row_count} rows and saved {european_count} European cities to {output_file}")

if __name__ == "__main__":
    main() 