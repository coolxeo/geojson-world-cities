#!/usr/bin/env python3
import json
import sys
import os
import re

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

def main():
    input_file = 'geonames-all-cities-with-a-population-1000@public (1).geojson'
    output_file = 'european_cities_geonames.geojson'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    print(f"Processing {input_file}...")
    
    # Process the file in chunks to handle large files
    european_features = []
    
    # Open the file and read line by line
    with open(input_file, 'r') as f:
        line_count = 0
        feature_count = 0
        
        # Read the file line by line
        buffer = ""
        in_feature = False
        
        for line in f:
            line_count += 1
            
            # Add the line to our buffer
            buffer += line
            
            # Check if we have a complete feature
            if '"type":"Feature"' in buffer and ('},' in buffer or '}}' in buffer):
                # Try to extract a complete feature
                try:
                    # Find the start of the feature
                    start_idx = buffer.find('"type":"Feature"')
                    if start_idx > 0:
                        # Move back to find the opening brace
                        while start_idx > 0 and buffer[start_idx] != '{':
                            start_idx -= 1
                    
                    # Find the end of the feature
                    end_idx = buffer.find('},', start_idx)
                    if end_idx == -1:
                        end_idx = buffer.find('}}', start_idx)
                        if end_idx != -1:
                            end_idx += 2  # Include the closing braces
                    else:
                        end_idx += 1  # Include the closing brace
                    
                    if start_idx >= 0 and end_idx > start_idx:
                        # Extract the feature
                        feature_str = buffer[start_idx:end_idx]
                        
                        # Parse the feature
                        try:
                            feature = json.loads(feature_str)
                            
                            # Check if the city is in Europe
                            is_european = False
                            
                            # Check by country name
                            if 'properties' in feature and feature['properties']:
                                country_name = feature['properties'].get('cou_name_en')
                                if country_name and is_european_country(country_name):
                                    is_european = True
                            
                            # Check by coordinates if not already determined to be European
                            if not is_european and 'geometry' in feature and feature['geometry']:
                                geom_type = feature['geometry'].get('type', '').lower()
                                coords = feature['geometry'].get('coordinates', [])
                                
                                # For Point geometries (city centers)
                                if geom_type == 'point' and coords and len(coords) == 2:
                                    lon, lat = coords
                                    if is_in_europe(lon, lat):
                                        is_european = True
                            
                            # If the city is in Europe, add it to our list
                            if is_european:
                                european_features.append(feature)
                                feature_count += 1
                                
                                # Print progress every 1000 features
                                if feature_count % 1000 == 0:
                                    print(f"Processed {line_count} lines, found {feature_count} European cities so far...")
                        
                        except json.JSONDecodeError as e:
                            print(f"Error parsing feature at line {line_count}: {e}")
                        
                        # Remove the processed feature from the buffer
                        buffer = buffer[end_idx:]
                
                except Exception as e:
                    print(f"Error processing buffer at line {line_count}: {e}")
                    buffer = ""  # Reset buffer on error
            
            # Limit processing to first 100,000 lines for testing
            if line_count >= 100000:
                print(f"Reached line limit of 100,000. Stopping processing.")
                break
    
    # Create new GeoJSON with only European cities
    european_data = {
        'type': 'FeatureCollection',
        'features': european_features
    }
    
    # Save the filtered data
    print(f"Saving {len(european_features)} European cities to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(european_data, f)
    
    print(f"Done! European cities have been saved to {output_file}")

if __name__ == "__main__":
    main() 