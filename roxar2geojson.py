import argparse
import roxar

parser = argparse.ArgumentParser(description='Create GeoJson well geometry.')

parser.add_argument('project', type=str, nargs='+', help='RMS project path')

args = parser.parse_args()

for path in args.project:
    with roxar.Project.open(path) as project:
        for well in project.wells:
            print(well)

