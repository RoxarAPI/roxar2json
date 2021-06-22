[![Pylint](https://github.com/RoxarAPI/roxar2json/workflows/Pylint/badge.svg)](https://github.com/RoxarAPI/roxar2json/actions/workflows/pylint.yml)
[![Unit tests](https://github.com/RoxarAPI/roxar2json/workflows/Python%20unit%20tests/badge.svg)](https://github.com/RoxarAPI/roxar2json/actions/workflows/python-app.yml)

# Roxar2json
Serializes wells and stratigraphy info from RMS projects to Json encoding.

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
```

Extract wells geometry:
```sh
roxenv python wells2geojson <RMS project path>
```

Extract well logs:
```sh
roxenv python logs2jsonwelllog <RMS project path>
```

Extract stratigraphy:
```sh
roxenv python stratigraphy2json <RMS project path>
```

## Testing
```python
roxenv python test.py
```
