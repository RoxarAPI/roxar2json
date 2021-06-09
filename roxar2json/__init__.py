import hashlib
from . import geojson

def generate_color(text):
    hash_object = hashlib.sha256()
    hash_object.update(text.encode('ascii', errors='replace'))
    digest = hash_object.digest()
    segment_size = int(hash_object.digest_size / 3)
    red = int.from_bytes(digest[:segment_size], 'big') % 255
    green = int.from_bytes(digest[segment_size:-segment_size], 'big') % 255
    blue = int.from_bytes(digest[-segment_size:], 'big') % 255

    max_intensity = max(red, green, blue)

    frac = 255 / max_intensity

    red *= frac
    green *= frac
    blue *= frac

    red = int(red)
    green = int(green)
    blue = int(blue)

    return [red, green, blue, 255]

def get_well_geojson(well):
    geometry = []
    md = []
    color = generate_color(well.name)
    well_head_point = geojson.create_point(well.wellhead)
    geometry.append(well_head_point)

    for trajectory in well.wellbore.trajectories:
        coordinates = trajectory.survey_point_series.get_measured_depths_and_points()

        # The first coordinate is MD, the rest is (x, y z).
        md.append(coordinates[:, 0].tolist())
        coordinates = coordinates[:, 1:3]

        trajectory_polyline = geojson.create_polyline(coordinates.tolist())

        geometry.append(trajectory_polyline)

    geometry_collection = geojson.create_collection(geometry)

    return geojson.create_well_feature(geometry_collection, well.name, color, md)

def get_wells_geojson(project):
    geometry = []
    for well in project.wells:
        geometry.append(get_well_geojson(well))
    return geometry

def get_stratigraphy_json(project):
    stratigraphy = {'horizons': [], 'zones': []}
    zones = project.zones
    horizons = project.horizons
    for zone in zones:
        info = {
            'name': zone.name,
            'horizon_above': zone.horizon_above.name,
            'horizon_below': zone.horizon_below.name
        }
        stratigraphy['zones'].append(info)
    for horizon in horizons:
        stratigraphy['horizons'].append(horizon.name)
    return stratigraphy
