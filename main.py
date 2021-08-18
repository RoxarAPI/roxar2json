#!python3

import argparse
import sys
import os
import json

import roxar2json
from roxar2json import roxar_proxy as roxar

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description='Create Json data from RMS project.')

    # Global arguments
    PARSER.add_argument('project', type=str, nargs='+', help='RMS project path')
    PARSER.add_argument(
        '-p',
        '--pretty',
        action="store_true",
        help='Encode with indentation')

    # Fault lines arguments
    if PARSER.prog == "faultlines2json":
        PARSER.add_argument('--horizon', type=str)

    # Log run arguments
    if PARSER.prog == "logs2jsonwelllog":
        PARSER.add_argument(
                '--log_run',
                type=str,
                nargs='+',
                help='List of log runs to export')
        PARSER.add_argument('--sample_size', type=float, help='Logs resampling rate')

    ARGS = PARSER.parse_args()

    DATA = {}

    # Suppress Roxar API warnings to stdout
    sys.stdout = os.fdopen(os.dup(1), 'w')
    os.close(1)

    for path in ARGS.project:
        try:
            with roxar.Project.open(path, readonly=True) as roxar_project:
                if PARSER.prog == "wells2geojson":
                    DATA = roxar2json.get_wells_geojson(roxar_project)
                elif PARSER.prog == "faultlines2json":
                    horizon_name = ARGS.horizon
                    DATA = roxar2json.get_fault_polygons(roxar_project, horizon_name)
                elif PARSER.prog == "logs2jsonwelllog":
                    log_runs = ARGS.log_run
                    sample_size = ARGS.sample_size
                    DATA = roxar2json.get_logs_jsonwelllog(
                        roxar_project, log_runs, sample_size)
                elif PARSER.prog == "stratigraphy2json":
                    DATA = roxar2json.get_stratigraphy_json(roxar_project)
        except NotImplementedError:
            print("Error: Roxar API needed.", file=sys.stderr)

    INDENT = None
    if ARGS.pretty:
        INDENT = 4


    print(json.dumps(DATA, indent=INDENT))
