#!/usr/bin/env python3
import json
import sys

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

# Define European cities by name (based on the sample we've seen)
european_city_names = {
    'TORSHAVN', 'LERWICK', 'HONNINGSVAG', 'DYFJORD', 'HAMMERFEST', 'BATSFORD',
    'VADSO', 'TROMSO', 'ANDENES', 'HARSTAD', 'AVVIL', 'NARVIK', 'MUONIO',
    'KROKVIK', 'VITTANGI'
}

# Alternative approach: define Europe by bounding box
# This is a rough approximation of Europe's boundaries
def is_in_europe_bbox(lon, lat):
    # Make sure we're dealing with numbers
    try:
        lon_val = float(lon)
        lat_val = float(lat)
        return -25 <= lon_val <= 40 and 34 <= lat_val <= 72
    except (TypeError, ValueError):
        return False

def calculate_centroid(coordinates):
    """Calculate the centroid of a polygon."""
    if not coordinates or not coordinates[0]:
        return None, None
    
    # For simplicity, we'll use the first ring of coordinates
    ring = coordinates[0]
    
    # Calculate centroid
    sum_x = sum(point[0] for point in ring)
    sum_y = sum(point[1] for point in ring)
    
    count = len(ring)
    if count == 0:
        return None, None
    
    return sum_x / count, sum_y / count

def main():
    print("Loading cities.geojson file...")
    try:
        with open('cities.geojson', 'r') as f:
            data = json.load(f)
        
        print(f"Loaded GeoJSON with {len(data['features'])} cities.")
        
        european_features = []
        for i, feature in enumerate(data['features']):
            try:
                # Check if the city name is in our list of European cities
                city_name = None
                if 'properties' in feature and feature['properties']:
                    city_name = feature['properties'].get('NAME')
                
                # Check if the city is in Europe by name
                if city_name and city_name in european_city_names:
                    european_features.append(feature)
                    continue
                
                # Check if the city is in Europe by coordinates
                if 'geometry' in feature and feature['geometry']:
                    geom_type = feature['geometry'].get('type', '').lower()
                    coords = feature['geometry'].get('coordinates', [])
                    
                    if geom_type == 'polygon' and coords:
                        # Calculate the centroid of the polygon
                        centroid_lon, centroid_lat = calculate_centroid(coords)
                        
                        # Check if the centroid is in Europe
                        if centroid_lon is not None and centroid_lat is not None:
                            if is_in_europe_bbox(centroid_lon, centroid_lat):
                                european_features.append(feature)
            except Exception as e:
                print(f"Error processing feature {i}: {e}")
                continue
        
        # Create new GeoJSON with only European cities
        european_data = {
            'type': 'FeatureCollection',
            'features': european_features
        }
        
        # Save the filtered data
        print(f"Saving {len(european_features)} European cities to european_cities.geojson...")
        with open('european_cities.geojson', 'w') as f:
            json.dump(european_data, f)
        
        print("Done! European cities have been saved to european_cities.geojson")
        
    except Exception as e:
        print(f"Error processing the GeoJSON file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 