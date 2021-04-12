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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create GeoJson well geometry.')

    parser.add_argument('project', type=str, nargs='+', help='RMS project path')

    args = parser.parse_args()

    geometry = []

    # Prevent Roxar API warnings to stdout
    sys.stdout = os.fdopen(os.dup(1), 'w')
    os.close(1)

    for path in args.project:
        with roxar.Project.open(path, readonly=True) as project:
            for well in project.wells:
                geometry += get_well_geojson(well)

    print(json.dumps(geometry))
