import argparse, sys, contextlib, os, json, hashlib
import roxar
import roxar.coordinate_systems

parser = argparse.ArgumentParser(description='Create GeoJson well geometry.')

parser.add_argument('project', type=str, nargs='+', help='RMS project path')

args = parser.parse_args()

geometry = []

# Roxar API quirk
sys.stdout = os.fdopen(os.dup(1), 'w')
os.close(1)

for path in args.project:
    with roxar.Project.open(path) as project:
        for well in project.wells:
            m = hashlib.sha256()
            m.update(well.name.encode('ascii'))
            digest = m.digest()
            segment_size = int(m.digest_size / 3)
            r = int.from_bytes(digest[:segment_size], 'big') % 205 + 50
            g = int.from_bytes(digest[segment_size:-segment_size], 'big') % 205 + 50
            b = int.from_bytes(digest[-segment_size:], 'big') % 205 + 50


            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": well.wellhead,
                },
                "properties": {
                    "name": well.name,
                    "color": [r, g, b, 200],
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
                        "color": [r, g, b, 200],
                    }
                }
                geometry.append(feature)


print(json.dumps(geometry))
