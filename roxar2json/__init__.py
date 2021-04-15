#!python3

import argparse
import sys
import os
import json
import hashlib
from . import geojson
from . import roxar_proxy as roxar

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
    color = generate_color(well.name)
    feature = geojson.create_point(well.wellhead, well.name, color)
    geometry.append(feature)

    for trajectory in well.wellbore.trajectories:
        coordinates = trajectory.survey_point_series.get_points()
        feature = geojson.create_polyline(
            coordinates[:, :2].tolist(), well.name, color)
        geometry.append(feature)
    return geometry

def get_wells_geojson(project):
    geometry = []
    for well in project.wells:
        geometry += get_well_geojson(well)
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

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description='Create Json data from RMS project.')

    PARSER.add_argument('project', type=str, nargs='+', help='RMS project path')
    PARSER.add_argument(
        '-p',
        '--pretty',
        action="store_true",
        help='Encode with indentation')

    ARGS = PARSER.parse_args()

    DATA = []

    # Suppress Roxar API warnings to stdout
    sys.stdout = os.fdopen(os.dup(1), 'w')
    os.close(1)

    for path in ARGS.project:
        try:
            with roxar.Project.open(path, readonly=True) as roxar_project:
                if PARSER.prog == "wells2geojson":
                    DATA.extend(get_wells_geojson(roxar_project))
                elif PARSER.prog == "stratigraphy2json":
                    DATA.append(get_stratigraphy_json(roxar_project))
        except NotImplementedError:
            print("Error: Roxar API needed.", file=sys.stderr)

    INDENT = None
    if ARGS.pretty:
        INDENT = 4


    print(json.dumps(DATA, indent=INDENT))
