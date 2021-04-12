def create_point(coordinates, name, color):
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coordinates,
        },
        "properties": {
            "name": name,
            "color": color,
        }
    }
    return feature

def create_polyline(coordinates, name, color):
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates,
        },
        "properties": {
            "name": name,
            "color": color,
        }
    }
    return feature

