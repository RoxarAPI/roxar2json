from .utilities import generate_color
from . import geojson, jsonwelllog
import numpy as np
import numpy.ma


def get_trajectory_geojson(trajectory):
    coordinates = trajectory.survey_point_series.get_measured_depths_and_points()
    if coordinates is None:
        return None

    # Change sign of z axis.
    coordinates[:, 3] = -coordinates[:, 3]

    # The first coordinate is MD, the rest is (x, y z).
    coordinates = coordinates[:, 1:4]

    return geojson.create_polyline(coordinates.tolist())


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

        # The first coordinate is MD, the rest is (x, y z).
        md.append(coordinates[:, 0].tolist())

        trajectory_polyline = get_trajectory_geojson(trajectory)

        geometry.append(trajectory_polyline)

    geometry_collection = geojson.create_collection(geometry)

    return geojson.create_well_feature(geometry_collection, well.name, color, md)


def get_wells_geojson(project):
    geometry = []
    for well in project.wells:
        geometry.append(get_well_geojson(well))
    return geojson.create_feature_collection(geometry)


def get_fault_polygons(project, horizon_name):
    item = project.horizons[horizon_name]["ExtractedFaultLines"]
    poly_data = item.get_values()

    features = []
    for line in poly_data:
        polygon = geojson.create_polygon(line[:, :3].tolist())
        feature = geojson.create_feature(polygon, horizon_name, [0, 0, 0, 255])
        features.append(feature)

    feature_collection = geojson.create_feature_collection(features)
    return feature_collection


def get_interval_mask(curve):
    "Collapse intervals."
    adjacent = np.append([0], curve.data[:-1])
    mask = (curve.data == adjacent)
    return mask

def collapse_interval(curve):
    "Collapse intervals."
    adjacent = np.append([0], curve.data[:-1])
    collapsed = numpy.ma.masked_where(curve.data == adjacent, curve)
    return collapsed


def get_log_jsonwelllog(log_run, sample_size=None):
    log = {}
    log["header"] = jsonwelllog.create_header(log_run)
    log["curves"] = jsonwelllog.create_curves(log_run)
    log["data"] = jsonwelllog.create_data(log_run, sample_size)
    log["metadata_discrete"] = jsonwelllog.create_discrete_metadata(log_run)
    return log

def get_interval_logs(log_run, sample_size=None):
    header = jsonwelllog.create_header(log_run)
    curve_headers = jsonwelllog.create_curves(log_run)
    curves = jsonwelllog._get_log_data(log_run, sample_size)
    md = jsonwelllog._get_mds(log_run, sample_size)

    logs = []

    for curve_header, curve in zip(curve_headers[1:], curves):
        log = {}
        log["header"] = header
        log["curves"] = [curve_headers[0], curve_header]
        interval_mask = get_interval_mask(curve)
        stripped_md = md[~interval_mask]
        curve = curve[~interval_mask]
        log["data"] = [stripped_md.tolist(), curve.tolist()]
        logs.append(log)

    return logs

def get_logs_jsonwelllog(project, selected_log_runs=None, sample_size=None, wells=None, encode_codenames=False, spread_logs=False):
    logs = []
    log_runs = selected_log_runs if selected_log_runs else []
    for well in project.wells:
        if wells and well.name not in wells:
            continue
        for trajectory in well.wellbore.trajectories:
            if not selected_log_runs:
                for log in trajectory.log_runs:
                    log_runs.append(log.name)
            for log_run_name in log_runs:
                try:
                    log_run = trajectory.log_runs[log_run_name]
                    logs += get_log_jsonwelllog(log_run, sample_size, spread_logs)
                except KeyError:
                    continue
            # Export logs of only first available trajectory as there is
            # JSONWellLog format expects only one trajectory associated to a well
            # and there is no mechanism in RoxAPI to identify default trajectory.
            break
    return logs


def get_stratigraphy_json(project):
    stratigraphy = {"horizons": [], "zones": []}
    zones = project.zones
    horizons = project.horizons
    for zone in zones:
        info = {
            "name": zone.name,
            "horizon_above": zone.horizon_above.name,
            "horizon_below": zone.horizon_below.name,
        }
        stratigraphy["zones"].append(info)
    for horizon in horizons:
        stratigraphy["horizons"].append(horizon.name)
    return stratigraphy

def get_grid_layer_data(project, grid_name, property_name):
    # note: property should be time dependent.

    grid_model = project.grid_models[grid_name]
    grid = grid_model.get_grid(realisation=0)
    geometry = grid.get_geometry()
    properties = grid_model.properties[property_name]
    # keep for debug.
    #print(properties.type)
    #print(properties.data_type)
    tags = properties.get_tags(realisation=0)
    timesteps = len(tags)

    ni, nj, nk = geometry.dimensions
    indexer = grid.grid_indexer
    cells = []
    k = 0
    for i in range(ni):
        for j in range(nj):
            corners_all = grid.get_cell_corners_by_index((i,j,k)).tolist()
            corners = [corners_all[0][0:3], corners_all[1][0:3], corners_all[3][0:3], corners_all[2][0:3] ]

            index = (i, j, k)
            if indexer.is_defined(index):
                cell_number = indexer.get_cell_numbers(index)

                property_values = []
                for t in range(timesteps):
                    property_values.append( float(properties.get_values(realisation=0, cell_numbers=cell_number, tag=t)) )

                cell = {"i": i, "j": j, "z": corners_all[0][2], "cs": corners, "vs": property_values}
                cells.append(cell)

    return cells
