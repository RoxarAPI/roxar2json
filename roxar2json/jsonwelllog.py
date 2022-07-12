"JSON Well Log function"

import numpy as np
from .utilities import generate_color


def create_header(log_run):
    "Create JSON Well Log header"
    header = {}
    header["name"] = log_run.name
    header["well"] = log_run.trajectory.wellbore.name
    try:
        header["startIndex"] = log_run.get_measured_depths()[0]
        header["endIndex"] = log_run.get_measured_depths()[-1]
    except IndexError:
        header["startIndex"] = None
        header["endIndex"] = None

    header["step"] = None
    return header


def create_curve(name, kind, unit, dimension, interpolation_type):
    curve = {}
    curve["name"] = name
    curve["description"] = kind
    curve["quantity"] = unit
    curve["unit"] = unit
    curve["valueType"] = "float" if kind == "continuous" else "integer"
    curve["dimensions"] = dimension
    curve["interpolationType"] = interpolation_type
    return curve


def create_curves(log_run):
    "Create JSON Well Log curves"
    curves = []
    curves.append(create_curve("MD", "continuous", "m", 1, "continuous"))
    for log_curve in log_run.log_curves:
        curves.append(
            create_curve(
                log_curve.name,
                log_curve.kind,
                log_curve.unit,
                log_curve.shape[1],
                log_curve.interpolation_type.name,
            )
        )
    return curves


def _resample_mds(mds, step):
    if len(mds) == 0:
        return np.array([])
    return np.arange(mds[0], mds[-1], step).tolist()


def _interpolate_log(log_run, log_values, sample_size, is_discrete):
    try:
        from scipy.interpolate import interp1d

        original_mds = _get_mds(log_run)

        if not original_mds.size > 0:
            return []

        sampled_mds = _get_mds(log_run, sample_size)
        log_values = log_values.tolist()
        if is_discrete:
            log_interp = interp1d(original_mds, log_values, kind="nearest")
            sampled_values = log_interp(sampled_mds).astype(np.int32)
            int_nan = np.array([np.nan]).astype(np.int32)[0]
            sampled_values = np.where(sampled_values == int_nan, None, sampled_values)
        else:
            log_interp = interp1d(original_mds, log_values, kind="linear")
            sampled_values = log_interp(sampled_mds)
            sampled_values = np.where(np.isnan(sampled_values), None, sampled_values)

        return sampled_values.tolist()

    except ModuleNotFoundError:
        return []


def _get_mds(log_run, sample_size=None):
    original_mds = log_run.get_measured_depths()
    if sample_size and sample_size > 0:
        return _resample_mds(original_mds, sample_size)
    return original_mds


def _get_log_data(log_run, sample_size):
    log_data = []
    for lc in log_run.log_curves:
        if sample_size and sample_size > 0:
            sampled_log_values = _interpolate_log(
                log_run, lc.get_values(), sample_size, lc.is_discrete
            )
            log_data.append(sampled_log_values)
        else:
            log_data.append(lc.get_values())
    return log_data


def create_data(log_run, sample_size):
    "Create JSON Well Log data"
    md = _get_mds(log_run, sample_size)
    log_data = _get_log_data(log_run, sample_size)

    if md.any() and log_data:
        return list(zip(md, *log_data))
    return []


def _create_log_curve_metadata(discrete_log_curve):
    metadata = {}
    metadata["attributes"] = ["color", "code"]

    object_data = {}
    for code, label in discrete_log_curve.get_code_names().items():
        object_data[label] = [generate_color(label), code]

    metadata["objects"] = object_data
    return metadata


def create_discrete_metadata(log_run):
    metadata = {}
    for lc in log_run.log_curves:
        # Continuous logs don't have labels
        if not lc.is_discrete:
            continue
        metadata[lc.name] = _create_log_curve_metadata(lc)
    return metadata
