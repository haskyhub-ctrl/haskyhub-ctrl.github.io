import json

filepath = 'Việt Nam (tỉnh thành).geojson'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Type: {data.get('type')}")
    features = data.get('features', [])
    print(f"Total features: {len(features)}")
    
    if features:
        print("--- Properties of first feature ---")
        for key, value in features[0].get('properties', {}).items():
            print(f"  {key}: {value}")
            
    print("--- Memory size estimation ---")
    print(f"Items are mostly: {type(features[0].get('geometry', {}).get('coordinates'))}")
    
except Exception as e:
    print(f"Error: {e}")
