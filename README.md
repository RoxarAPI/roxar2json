[![Pylint](https://github.com/RoxarAPI/roxar2json/workflows/Pylint/badge.svg)](https://github.com/RoxarAPI/roxar2json/actions/workflows/pylint.yml)
[![Unit tests](https://github.com/RoxarAPI/roxar2json/workflows/Python%20unit%20tests/badge.svg)](https://github.com/RoxarAPI/roxar2json/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/RoxarAPI/roxar2json/branch/master/graph/badge.svg)](https://codecov.io/gh/RoxarAPI/roxar2json)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

# Roxar2json
Serializes geological info from RMS projects to Json encoding.

Supported geological data serializations:
- Well trajectory -> [GeoJson](https://geojson.org/)
- Well logs -> [Json Well Log Format](https://jsonwelllogformat.org/)
- Stratigraphic column -> Custom Json format
- Grid k-layers -> Custom Json format
- Fault lines -> [GeoJson](https://geojson.org/)

## Installation
```sh
roxenv python -m pip install git+https://github.com/RoxarAPI/roxar2json#egg=roxar2json
```

## Usage

```python
import roxar2json
with roxar.Project.open(project_path) as project:
    stratigraphy = roxar2json.get_stratigraphy_json(project)
    wells = roxar2json.get_wells_geojson(project)
    logs = roxar2json.get_logs_jsonwelllog(project)
```

Synopsis:
```sh
./wells2geojson -h
./logs2jsonwelllog -h
./stratigraphy2json -h
./faultlines2geojson -h
./gridlayer2json -h
```

### Extract wells geometry:
```sh
roxenv python wells2geojson <RMS project path>
```

### Extract well logs:
Extract all wells and all log runs:
```sh
roxenv python logs2jsonwelllog <RMS project path>
```

Extract selected wells and selected log runs:
```sh
roxenv python logs2jsonwelllog --log_run BLOCKING --well '15/9-19 A' -- <RMS project path>
```

Spread log curves in order to maximise intervals:
```sh
roxenv python logs2jsonwelllog --spread -- <RMS project path>
```

Filter by curve name:
```sh
roxenv python logs2jsonwelllog --spread --curve ZONELOG --log_run BLOCKING  -- <RMS project path>
```



### Extract stratigraphy:
```sh
roxenv python stratigraphy2json <RMS project path>
```

## Testing

Test using RoxarAPI:
```python
roxenv python test.py
```

Test using mock API:
```python
python test.py
```

## Contributing
Commit messages should follow [Conventional commits format](https://www.conventionalcommits.org/en/v1.0.0/)

## Examples
See [WebViz Subsurface Compnents](https://github.com/equinor/webviz-subsurface-components).
