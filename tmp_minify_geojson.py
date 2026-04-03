import json

filepath = 'Việt Nam (tỉnh thành).geojson'

def round_coords(coords, precision=5):
    if isinstance(coords, list):
        if len(coords) == 0: return coords
        if isinstance(coords[0], (int, float)):
            return [round(c, precision) for c in coords]
        return [round_coords(c, precision) for c in coords]
    return coords

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for feature in data.get('features', []):
        geom = feature.get('geometry', {})
        if geom and 'coordinates' in geom:
            geom['coordinates'] = round_coords(geom['coordinates'], 5)

    outpath = 'frontend/data/vietnam_merged.geojson'
    import os
    os.makedirs('frontend/data', exist_ok=True)
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(data, f) # No separators=(',', ':') to keep it simple, or yes to compress
        
    print(f"Saved optimized GeoJSON to {outpath}")
except Exception as e:
    print(f"Error: {e}")
