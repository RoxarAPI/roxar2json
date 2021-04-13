#!python3

import argparse, sys, contextlib, os, json, hashlib
import geojson
import roxar_proxy as roxar

def generate_color(text):
    m = hashlib.sha256()
    m.update(text.encode('ascii', errors='replace'))
    digest = m.digest()
    segment_size = int(m.digest_size / 3)
    r = int.from_bytes(digest[:segment_size], 'big') % 255
    g = int.from_bytes(digest[segment_size:-segment_size], 'big') % 255
    b = int.from_bytes(digest[-segment_size:], 'big') % 255

    max_intensity = max(r, g, b)

    f = 255 / max_intensity

    r *= f
    g *= f
    b *= f

    r = int(r)
    g = int(g)
    b = int(b)

    return [r, g, b, 255]

def get_well_geojson(well):
    geometry = []
    color = generate_color(well.name)
    feature = geojson.create_point(well.wellhead, well.name, color)
    geometry.append(feature)

    for trajectory in well.wellbore.trajectories:
        coordinates = trajectory.survey_point_series.get_points()
        feature = geojson.create_polyline(
                coordinates[:,:2].tolist(), well.name, color)
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
    parser = argparse.ArgumentParser(
            description='Create Json data from RMS project.')

    parser.add_argument('project', type=str, nargs='+', help='RMS project path')
    parser.add_argument(
            '-p',
            '--pretty',
            action="store_true",
            help='Encode with indentation')

    args = parser.parse_args()

    data = []

    # Suppress Roxar API warnings to stdout
    sys.stdout = os.fdopen(os.dup(1), 'w')
    os.close(1)

    for path in args.project:
        try:
            with roxar.Project.open(path, readonly=True) as project:
                if parser.prog == "wells2geojson":
                    data.extend(get_wells_geojson(project))
                elif parser.prog == "stratigraphy2json":
                    data.append(get_stratigraphy_json(project))
        except NotImplementedError:
            print("Error: Roxar API needed.", file=sys.stderr)

    indent = None
    if args.pretty:
        indent = 4

    print(json.dumps(data, indent=indent))
