import numpy as np
from scipy.interpolate import interp1d

"JSON Well Log function"

def create_header(log_run):
    "Create JSON Well Log header"
    header = {}
    header['name'] = log_run.name
    header['well'] = log_run.trajectory.wellbore.name
    header['field'] = None
    header['date'] = None
    header['operator'] = None
    try:
        header['startIndex'] = log_run.get_measured_depths()[0]
        header['endIndex'] = log_run.get_measured_depths()[-1]
    except:
        header['startIndex'] = None
        header['endIndex'] = None

    header['step'] = None
    return header

def create_curve(name, kind, unit, dimension):
    curve = {}
    curve['name'] = name
    curve['description'] = kind
    curve['quantity'] = unit
    curve['unit'] = unit
    curve['valueType'] = "float" if kind == "continuous" else "integer"
    curve['dimensions'] = dimension
    return curve

def create_curves(log_run):
    "Create JSON Well Log curves"
    curves = []
    curves.append(create_curve("XY", "continuous", "m", 2))
    for log_curve in log_run.log_curves:
        curves.append(create_curve(log_curve.name,
                                   log_curve.kind,
                                   log_curve.unit,
                                   log_curve.shape[1]))
    return curves

def _interpolate_log_at_md(mds, logs, log_at_md):
    if (logs == [None, None]):
        return None
    if logs[0] is None:
        return logs[1]
    if logs[1] is None:
        return logs[0]

    log_interp = interp1d(mds, logs, kind='nearest')
    return log_interp(log_at_md).tolist()


def _get_closest_md(mds, sample_md):
    min_idx = np.nonzero(mds<=sample_md)[0][-1]
    if min_idx == len(mds)-1:
        return min_idx, None
    else:
        return min_idx, min_idx+1


def _resample_mds(mds, step):
    return np.arange(mds[0], mds[-1], step)


def _interpolate_log(log_run, log_values, sample_size):
    original_mds = _get_mds(log_run)
    sampled_mds = _get_mds(log_run, sample_size)
    resampled_logs = []
    for sample_md in sampled_mds:
        min_idx, max_idx = _get_closest_md(original_mds, sample_md)

        if max_idx is None:
            resampled_logs.append(log_values[min_idx])
        else:
            sampled_log = _interpolate_log_at_md(
                [original_mds[min_idx], original_mds[max_idx]],
                [log_values[min_idx], log_values[max_idx]],
                sample_md)
            resampled_logs.append(sampled_log)
    return resampled_logs


def _get_mds(log_run, sample_size=None):
    original_mds = log_run.get_measured_depths()
    if sample_size and sample_size > 0:
        return _resample_mds(original_mds, sample_size)
    else:
        return original_mds


def _get_xy_from_log(log_run, sample_size):
    xy = []
    log_mds = _get_mds(log_run, sample_size)
    sps = log_run.trajectory.survey_point_series
    for md in log_mds:
        try:
            xy.append(sps.interpolate_survey_point(md)[3:5].tolist())
        except:
            return []
    return xy

def _get_log_data(log_run, sample_size):
    log_data = []
    for lc in log_run.log_curves:
        log_values = lc.get_values().tolist()
        if sample_size and sample_size > 0:
            sampled_log_values = _interpolate_log(log_run, log_values, sample_size)
            log_data.append(sampled_log_values)
        else:
            log_data.append(log_values)
    return log_data

def create_data(log_run, sample_size):
    "Create JSON Well Log data"
    xy = _get_xy_from_log(log_run, sample_size)
    log_data = _get_log_data(log_run, sample_size)

    if xy and log_data:
        return [xy]+log_data
    else:
        return []
