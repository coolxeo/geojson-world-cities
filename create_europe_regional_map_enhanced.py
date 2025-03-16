#!/usr/bin/env python3
import json
import os
import sys
import math
from collections import defaultdict

# Define European regions with more precise boundaries
REGIONS = {
    "Western Europe": {
        "countries": ["France", "Belgium", "Netherlands", "Luxembourg", "Germany", "Switzerland", "Austria", "Liechtenstein", "Monaco"],
        "polygon": [
            # Approximate region boundaries in [longitude, latitude] format
            [-5.5, 42.0],  # Southwest corner (Spain/France border)
            [7.5, 47.0],   # Southern border (Swiss/Italian Alps)
            [13.0, 47.0],  # Southeast (Austria/Slovenia)
            [15.0, 51.0],  # East (Germany/Poland)
            [8.0, 55.0],   # Northeast (Denmark)
            [3.5, 51.5],   # Northwest (English Channel)
            [-5.5, 48.5],  # Western coast (France)
            [-5.5, 42.0]   # Back to start
        ]
    },
    "Northern Europe": {
        "countries": ["United Kingdom", "Ireland", "Iceland", "Norway", "Sweden", "Finland", "Denmark", "Estonia", "Latvia", "Lithuania"],
        "polygon": [
            [-24.0, 63.0],  # Iceland
            [-10.0, 59.0],  # Atlantic
            [-5.0, 59.0],   # UK West coast
            [0.0, 52.0],    # UK South coast
            [4.0, 53.0],    # North Sea
            [30.0, 60.0],   # Eastern Baltic
            [32.0, 70.0],   # Northern Russia
            [25.0, 71.0],   # Northern Scandinavia
            [-20.0, 66.0],  # Back to Iceland
            [-24.0, 63.0]   # Close polygon
        ]
    },
    "Southern Europe": {
        "countries": ["Spain", "Portugal", "Italy", "Vatican City", "San Marino", "Malta", "Greece", "Cyprus"],
        "polygon": [
            [-10.0, 36.0],  # Southwest (Portugal/Spain)
            [3.0, 36.0],    # Southern Mediterranean
            [19.0, 35.0],   # Southern Greece
            [35.0, 35.0],   # Eastern Mediterranean (Cyprus)
            [29.0, 42.0],   # Turkey/Greece border
            [19.0, 45.5],   # Northeast (Balkan Peninsula)
            [13.0, 46.0],   # Northern Italy
            [8.0, 46.0],    # Alps
            [-3.0, 44.0],   # Pyrenees
            [-10.0, 44.0],  # Western Iberian Peninsula
            [-10.0, 36.0]   # Close polygon
        ]
    },
    "Eastern Europe": {
        "countries": ["Poland", "Czech Republic", "Slovakia", "Hungary", "Romania", "Bulgaria"],
        "polygon": [
            [12.0, 49.0],   # Western border (Germany/Czech Republic)
            [17.0, 48.0],   # Southwest (Austria/Slovakia)
            [22.0, 44.0],   # Southern border (Romania/Serbia)
            [29.0, 44.0],   # Southeast (Romania/Black Sea)
            [30.0, 49.0],   # Eastern border (Ukraine)
            [24.0, 54.0],   # Northeast (Baltic states)
            [14.0, 54.5],   # North (Poland/Baltic Sea)
            [12.0, 49.0]    # Close polygon
        ]
    },
    "Southeastern Europe": {
        "countries": ["Slovenia", "Croatia", "Bosnia and Herzegovina", "Serbia", "Montenegro", "North Macedonia", "Albania", "Kosovo"],
        "polygon": [
            [13.5, 46.0],   # Northwest (Slovenia/Italy border)
            [13.5, 45.0],   # Adriatic coast (Croatia)
            [19.0, 41.0],   # Southern tip (Albania)
            [23.0, 41.0],   # Southeast (Greece/North Macedonia)
            [23.0, 44.0],   # Northeast (Serbia/Romania)
            [19.0, 46.0],   # Northern border (Hungary)
            [16.0, 46.5],   # Northwest (Croatia/Hungary)
            [13.5, 46.0]    # Close polygon
        ]
    },
    "Northeastern Europe": {
        "countries": ["Belarus", "Ukraine", "Moldova", "Russia"],
        "polygon": [
            [23.0, 51.0],   # Western border (Poland/Belarus)
            [23.0, 45.0],   # Southwest (Romania/Moldova)
            [30.0, 44.0],   # Black Sea coast
            [45.0, 48.0],   # Southeast (Russia)
            [40.0, 60.0],   # Northeast (Russia)
            [30.0, 60.0],   # Northern border
            [23.0, 56.0],   # Northwest (Baltic states)
            [23.0, 51.0]    # Close polygon
        ]
    }
}

# Flatten country to region mapping
COUNTRY_TO_REGION = {}
for region, data in REGIONS.items():
    for country in data["countries"]:
        COUNTRY_TO_REGION[country] = region

def load_cities(filepath):
    """Load cities from GeoJSON file"""
    print(f"Loading data from {filepath}...")
    with open(filepath, 'r') as f:
        return json.load(f)

def create_region_features():
    """Create region features from predefined polygons"""
    region_features = []
    
    for region, data in REGIONS.items():
        feature = {
            "type": "Feature",
            "properties": {
                "name": region
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [data["polygon"]]
            }
        }
        region_features.append(feature)
    
    return region_features

def main():
    output_file = 'europe_cities.json'
    
    # Create region features
    region_features = create_region_features()
    print(f"Created {len(region_features)} region features")
    
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