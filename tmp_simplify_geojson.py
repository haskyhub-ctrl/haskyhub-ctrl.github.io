import json
import traceback
from copy import deepcopy

try:
    from shapely.geometry import shape, mapping
except ImportError:
    print("Shapely not found, please install it first.")
    exit(1)

filepath = 'Việt Nam (tỉnh thành).geojson'
outpath = 'frontend/data/vietnam_merged_optimized.geojson'

# Tolerance in degrees. 
# 0.005 degrees is approximately 550 meters at the equator.
# This should drastically reduce vertex count while keeping province borders intact visually.
TOLERANCE = 0.005 

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    simplified_features = []
    
    for feature in data.get('features', []):
        geom_dict = feature.get('geometry')
        if not geom_dict:
            continue
            
        try:
            geom = shape(geom_dict)
            # Simplify geometry. preserve_topology=True keeps shared boundaries and prevents intersections
            simplified_geom = geom.simplify(tolerance=TOLERANCE, preserve_topology=True)
            
            new_feature = deepcopy(feature)
            new_feature['geometry'] = mapping(simplified_geom)
            
            # Additional cleanup: remove unnecessary precision in numbers
            def round_coords(coords, precision=4):
                if isinstance(coords, list):
                    if len(coords) == 0: return coords
                    if isinstance(coords[0], (int, float)):
                        return [round(c, precision) for c in coords]
                    return [round_coords(c, precision) for c in coords]
                elif isinstance(coords, tuple):
                    if isinstance(coords[0], (int, float)):
                        return tuple(round(c, precision) for c in coords)
                    return tuple(round_coords(c, precision) for c in coords)
                return coords
            
            new_feature['geometry']['coordinates'] = round_coords(new_feature['geometry']['coordinates'])
            
            simplified_features.append(new_feature)
        except Exception as e:
            print(f"Failed to simplify a feature: {e}")
            simplified_features.append(feature) # Fallback to original

    data['features'] = simplified_features

    import os
    os.makedirs('frontend/data', exist_ok=True)
    
    # Save with custom separator to minify the JSON file size further
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
        
    original_size = os.path.getsize(filepath)
    new_size = os.path.getsize(outpath)
    
    print(f"Optimization successful!")
    print(f"Original size: {original_size / 1024 / 1024:.2f} MB")
    print(f"Optimized size: {new_size / 1024 / 1024:.2f} MB")

except Exception as e:
    print(f"Error during execution:")
    traceback.print_exc()
