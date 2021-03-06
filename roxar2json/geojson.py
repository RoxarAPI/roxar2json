"GeoJson geometry functions."


def create_feature(geometry, name, color):
    "Create GeoJson feature."
    feature = {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "name": name,
            "color": color,
        },
    }
    return feature


def create_well_feature(geometry, name, color, md):
    "Create a well GeoJson feature with an MD property."

    feature = create_feature(geometry, name, color)
    feature["properties"]["md"] = md
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


def create_polygon(coordinates):
    "Create GeoJson Polygon."
    poly_coords = [coordinates]
    return {
        "type": "Polygon",
        "coordinates": poly_coords,
    }


def create_feature_collection(features):
    "Create GeoJson FeatureCollection from a set of features."
    return {"type": "FeatureCollection", "features": features}
