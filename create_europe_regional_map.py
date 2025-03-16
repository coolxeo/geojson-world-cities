#!/usr/bin/env python3
import json
import os
import sys
from collections import defaultdict

# European regions grouping
REGIONS = {
    "Western Europe": ["France", "Belgium", "Netherlands", "Luxembourg", "Germany", "Switzerland", "Austria", "Liechtenstein", "Monaco"],
    "Northern Europe": ["United Kingdom", "Ireland", "Iceland", "Norway", "Sweden", "Finland", "Denmark", "Estonia", "Latvia", "Lithuania"],
    "Southern Europe": ["Spain", "Portugal", "Italy", "Vatican City", "San Marino", "Malta", "Greece", "Cyprus"],
    "Eastern Europe": ["Poland", "Czech Republic", "Slovakia", "Hungary", "Romania", "Bulgaria"],
    "Southeastern Europe": ["Slovenia", "Croatia", "Bosnia and Herzegovina", "Serbia", "Montenegro", "North Macedonia", "Albania", "Kosovo"],
    "Northeastern Europe": ["Belarus", "Ukraine", "Moldova", "Russia"]
}

# Flatten country to region mapping
COUNTRY_TO_REGION = {}
for region, countries in REGIONS.items():
    for country in countries:
        COUNTRY_TO_REGION[country] = region

def load_cities(filepath):
    """Load cities from GeoJSON file"""
    print(f"Loading data from {filepath}...")
    with open(filepath, 'r') as f:
        return json.load(f)

def group_by_region(cities_data):
    """Group cities by region"""
    city_points = defaultdict(list)
    
    for feature in cities_data["features"]:
        if feature["geometry"]["type"] != "Point":
            continue
            
        properties = feature["properties"]
        country = properties.get("country_name", "")
        
        # Skip cities with no country information
        if not country:
            continue
            
        # Get the region for this country
        region = COUNTRY_TO_REGION.get(country)
        if region:
            coords = feature["geometry"]["coordinates"]
            city_points[region].append(coords)
    
    return city_points

def create_region_polygons(city_points):
    """Create simplified polygons for each region"""
    region_features = []
    
    for region, points in city_points.items():
        if len(points) < 3:
            continue
            
        # Select a subset of points to create a simplified convex hull-like polygon
        # For simplicity, we'll just take points from different extremes 
        # This is a very simplified approach - in practice you'd use a proper convex hull algorithm
        points.sort(key=lambda p: p[0])  # Sort by longitude
        west_points = points[:min(5, len(points))]
        east_points = points[-min(5, len(points)):]
        
        all_selected = west_points + east_points
        all_selected.sort(key=lambda p: p[1])  # Sort by latitude
        south_points = all_selected[:min(5, len(all_selected))]
        north_points = all_selected[-min(5, len(all_selected)):]
        
        # Convert points to tuples of tuples for deduplication
        unique_points = {}
        for point in west_points + east_points + south_points + north_points:
            point_tuple = tuple(point)
            unique_points[point_tuple] = point
        
        boundary_points = list(unique_points.values())
        
        # Sort the points to form a rough polygon (this is simplified)
        # A proper implementation would use a convex hull algorithm
        central_point = [sum(p[0] for p in boundary_points)/len(boundary_points), 
                        sum(p[1] for p in boundary_points)/len(boundary_points)]
        
        # Sort points by angle to create a rough polygon
        def get_angle(point):
            return (point[0] - central_point[0], point[1] - central_point[1])
            
        boundary_points.sort(key=lambda p: (
            # Sort counterclockwise by quadrant and angle
            (1 if p[1] > central_point[1] else 0) * 2 + (1 if p[0] > central_point[0] else 0),
            (p[1] - central_point[1]) / (p[0] - central_point[0] + 0.0001)
        ))
        
        # Close the polygon
        polygon = boundary_points + [boundary_points[0]]
        
        feature = {
            "type": "Feature",
            "properties": {
                "name": region
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon]
            }
        }
        
        region_features.append(feature)
    
    return region_features

def main():
    # Use the european cities data file
    input_file = 'european_cities.geojson'
    output_file = 'europe_cities.json'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Load cities data
    cities_data = load_cities(input_file)
    print(f"Loaded {len(cities_data['features'])} features")
    
    # Group cities by region
    city_points = group_by_region(cities_data)
    print(f"Grouped cities into {len(city_points)} regions")
    
    # Create region polygons
    region_features = create_region_polygons(city_points)
    print(f"Created {len(region_features)} region polygons")
    
    # Create GeoJSON output
    output_data = {
        "type": "FeatureCollection",
        "features": region_features
    }
    
    # Save the output file
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"Saved output to {output_file} ({file_size:.2f} MB)")

if __name__ == "__main__":
    main()