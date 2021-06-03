"GeoJson geometry functions."

def create_feature(geometry, name, color):
    "Create GeoJson feature."
    feature = {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "name": name,
            "color": color,
        }
    }
    return feature


def create_collection(features):
    "Create GeoJson GeometryCollection from a set of features."
    collection = {"type": "GeometryCollection", "geometries": features}
    return collection

def create_point(coordinates):
    "Create GeoJson point. "
    return {
        "type": "Point",
        "coordinates": coordinates,
    }

def create_polyline(coordinates):
    "Create GeoJson LineString."
    return {
        "type": "LineString",
        "coordinates": coordinates,
    }
