#!/usr/bin/env python3
import json
import os
import sys
from collections import defaultdict

# Define European regions with their major cities/capitals
REGIONS = {
    "Western Europe": {
        "countries": ["France", "Belgium", "Netherlands", "Luxembourg", "Germany", "Switzerland", "Austria", "Liechtenstein", "Monaco"],
        "polygon": [
            [-5.5, 42.0],  # Southwest corner (Spain/France border)
            [7.5, 47.0],   # Southern border (Swiss/Italian Alps)
            [13.0, 47.0],  # Southeast (Austria/Slovenia)
            [15.0, 51.0],  # East (Germany/Poland)
            [8.0, 55.0],   # Northeast (Denmark)
            [3.5, 51.5],   # Northwest (English Channel)
            [-5.5, 48.5],  # Western coast (France)
            [-5.5, 42.0]   # Back to start
        ],
        "capitals": [
            {"name": "Paris", "coordinates": [2.3522, 48.8566]},
            {"name": "Berlin", "coordinates": [13.4050, 52.5200]},
            {"name": "Vienna", "coordinates": [16.3738, 48.2082]},
            {"name": "Brussels", "coordinates": [4.3517, 50.8503]},
            {"name": "Amsterdam", "coordinates": [4.9041, 52.3676]},
            {"name": "Bern", "coordinates": [7.4474, 46.9480]},
            {"name": "Luxembourg City", "coordinates": [6.1319, 49.6116]},
            {"name": "Monaco", "coordinates": [7.4246, 43.7384]},
            {"name": "Vaduz", "coordinates": [9.5209, 47.1410]}
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
        ],
        "capitals": [
            {"name": "London", "coordinates": [-0.1278, 51.5074]},
            {"name": "Dublin", "coordinates": [-6.2603, 53.3498]},
            {"name": "Reykjavik", "coordinates": [-21.9426, 64.1466]},
            {"name": "Oslo", "coordinates": [10.7522, 59.9139]},
            {"name": "Stockholm", "coordinates": [18.0686, 59.3293]},
            {"name": "Helsinki", "coordinates": [24.9384, 60.1699]},
            {"name": "Copenhagen", "coordinates": [12.5683, 55.6761]},
            {"name": "Tallinn", "coordinates": [24.7536, 59.4370]},
            {"name": "Riga", "coordinates": [24.1052, 56.9496]},
            {"name": "Vilnius", "coordinates": [25.2797, 54.6872]}
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
        ],
        "capitals": [
            {"name": "Madrid", "coordinates": [-3.7038, 40.4168]},
            {"name": "Lisbon", "coordinates": [-9.1393, 38.7223]},
            {"name": "Rome", "coordinates": [12.4964, 41.9028]},
            {"name": "Vatican City", "coordinates": [12.4534, 41.9029]},
            {"name": "San Marino", "coordinates": [12.4578, 43.9424]},
            {"name": "Valletta", "coordinates": [14.5074, 35.8997]},
            {"name": "Athens", "coordinates": [23.7275, 37.9838]},
            {"name": "Nicosia", "coordinates": [33.3823, 35.1856]}
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
        ],
        "capitals": [
            {"name": "Warsaw", "coordinates": [21.0122, 52.2297]},
            {"name": "Prague", "coordinates": [14.4378, 50.0755]},
            {"name": "Bratislava", "coordinates": [17.1077, 48.1486]},
            {"name": "Budapest", "coordinates": [19.0402, 47.4979]},
            {"name": "Bucharest", "coordinates": [26.1025, 44.4268]},
            {"name": "Sofia", "coordinates": [23.3219, 42.6977]}
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
        ],
        "capitals": [
            {"name": "Ljubljana", "coordinates": [14.5058, 46.0569]},
            {"name": "Zagreb", "coordinates": [15.9819, 45.8150]},
            {"name": "Sarajevo", "coordinates": [18.4131, 43.8563]},
            {"name": "Belgrade", "coordinates": [20.4612, 44.8125]},
            {"name": "Podgorica", "coordinates": [19.2636, 42.4304]},
            {"name": "Skopje", "coordinates": [21.4254, 42.0024]},
            {"name": "Tirana", "coordinates": [19.8187, 41.3275]},
            {"name": "Pristina", "coordinates": [21.1622, 42.6629]}
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
        ],
        "capitals": [
            {"name": "Minsk", "coordinates": [27.5615, 53.9045]},
            {"name": "Kiev", "coordinates": [30.5234, 50.4501]},
            {"name": "Chisinau", "coordinates": [28.8575, 47.0105]},
            {"name": "Moscow", "coordinates": [37.6173, 55.7558]},
            {"name": "St. Petersburg", "coordinates": [30.3351, 59.9343]}
        ]
    }
}

def create_geojson():
    """Create GeoJSON with regions and capital cities"""
    features = []
    
    # Add region polygons
    for region_name, region_data in REGIONS.items():
        # Create polygon feature for region
        region_feature = {
            "type": "Feature",
            "properties": {
                "name": region_name,
                "feature_type": "region"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [region_data["polygon"]]
            }
        }
        features.append(region_feature)
        
        # Add capital cities as point features
        for capital in region_data["capitals"]:
            capital_feature = {
                "type": "Feature",
                "properties": {
                    "name": capital["name"],
                    "feature_type": "capital",
                    "region": region_name
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": capital["coordinates"]
                }
            }
            features.append(capital_feature)
    
    # Create the final GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson

def main():
    output_file = 'europe_cities.json'
    
    # Create GeoJSON
    europe_geojson = create_geojson()
    
    # Save to file
    with open(output_file, 'w') as f:
        json.dump(europe_geojson, f, indent=2)
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"Saved output to {output_file} ({file_size:.2f} MB)")
    print(f"Created {len(europe_geojson['features'])} features ({len(REGIONS)} regions with capitals)")

if __name__ == "__main__":
    main()