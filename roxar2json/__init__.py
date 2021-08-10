from .utilities import generate_color
from . import geojson, jsonwelllog


def get_well_geojson(well):
    geometry = []
    md = []
    color = generate_color(well.name)
    well_head_point = geojson.create_point(well.wellhead)
    geometry.append(well_head_point)

    for trajectory in well.wellbore.trajectories:
        coordinates = trajectory.survey_point_series.get_measured_depths_and_points()
        if coordinates is None:
            continue

        # Change sign of z axis.
        for p in coordinates:
            p[3] = -p[3]

        # The first coordinate is MD, the rest is (x, y z).
        md.append(coordinates[:, 0].tolist())
        coordinates = coordinates[:, 1:4]

        trajectory_polyline = geojson.create_polyline(coordinates.tolist())

        geometry.append(trajectory_polyline)

    geometry_collection = geojson.create_collection(geometry)

    return geojson.create_well_feature(geometry_collection, well.name, color, md)

def get_wells_geojson(project):
    geometry = []
    for well in project.wells:
        geometry.append(get_well_geojson(well))
    return geojson.create_feature_collection(geometry)

def get_fault_polygons(project, horizon_name):
    item = project.horizons[horizon_name]['ExtractedFaultLines']
    poly_data = item.get_values()

    features = []
    for line in poly_data:
        polygon = geojson.create_polygon(line[:,:3].tolist())
        feature = geojson.create_feature(polygon, horizon_name, [0, 0, 0, 255])
        features.append(feature)

    feature_collection = geojson.create_feature_collection(features)
    return feature_collection

def get_log_jsonwelllog(log_run, sample_size=None):
    log = {}
    log['header'] = jsonwelllog.create_header(log_run)
    log['curves'] = jsonwelllog.create_curves(log_run)
    log['data'] = jsonwelllog.create_data(log_run, sample_size)
    log['metadata_discrete'] = jsonwelllog.create_discrete_metadata(log_run)
    return log

def get_logs_jsonwelllog(project, selected_log_runs=None, sample_size=None):
    logs = []
    log_runs = selected_log_runs if selected_log_runs else []
    for well in project.wells:
        for trajectory in well.wellbore.trajectories:
            if not selected_log_runs:
                for log in trajectory.log_runs:
                    log_runs.append(log.name)
            try:
                for log_run_name in log_runs:
                    try:
                        log_run = trajectory.log_runs[log_run_name]
                        logs.append(get_log_jsonwelllog(log_run, sample_size))
                    except KeyError:
                        continue
                # Export logs of only first available trajectory as there is
                # JSONWellLog format expects only one trajectory associated to a well
                # and there is no mechanism in RoxAPI to identify default trajectory.
                break
            except ValueError:
                continue
    return logs

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
