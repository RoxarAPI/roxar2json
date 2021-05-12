import numpy as np

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
    curves.append(create_curve("MD", "continuous", "m", 1))
    for log_curve in log_run.log_curves:
        curves.append(create_curve(log_curve.name,
                                   log_curve.kind,
                                   log_curve.unit,
                                   log_curve.shape[1]))
    return curves

def create_data(log_run):
    "Create JSON Well Log data"
    '''
    data = []
    data.append(log_run.get_measured_depths().tolist())
    for log_curve in log_run.log_curves:
      data.append(log_curve.get_values().tolist())

    return np.array(data).T.tolist()
    '''
    data = log_run.get_measured_depths()
    for log_curve in log_run.log_curves:
      try:
        data = np.vstack([data, log_curve.get_values()])
      except:
        continue
    return data.T.tolist()

