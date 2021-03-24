import argparse, sys, contextlib, os, json, hashlib
import roxar
import roxar.coordinate_systems

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create GeoJson well geometry.')

    parser.add_argument('project', type=str, nargs='+', help='RMS project path')

    args = parser.parse_args()

    geometry = []

    # Roxar API quirk
    sys.stdout = os.fdopen(os.dup(1), 'w')
    os.close(1)

    for path in args.project:
        with roxar.Project.open(path, readonly=True) as project:
            for well in project.wells:
                color = generate_color(well.name)

                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": well.wellhead,
                    },
                    "properties": {
                        "name": well.name,
                        "color": color,
                    }
                }

                geometry.append(feature)

                for trajectory in well.wellbore.trajectories:
                    coordinates = trajectory.survey_point_series.get_points()
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": coordinates[:,:2].tolist(),  # to [[x, y], ...]
                        },
                        "properties": {
                            "name": well.name,
                            "color": color,
                        }
                    }
                    geometry.append(feature)


    print(json.dumps(geometry))
