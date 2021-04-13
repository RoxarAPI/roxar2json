# Roxar2json
Serializes wells and stratigraphy info from RMS projects to Json encoding.

## Usage
Synopsis:
```sh
./wells2geojson -h
./stratigraphy2json -h
```

Extract wells geometry:
```sh
roxenv python wells2geojson <RMS project path>
```

Extract stratigraphy:
```sh
roxenv python stratigraphy2json <RMS project path>
```

```python
import roxar2json
with roxar.Project.open(project_path) as project:
    stratigraphy = roxar2json.get_stratigraphy_json(project)
    wells = roxar2json.get_wells_geojson(project)
```

## Testing
```python
roxenv python test.py
```
