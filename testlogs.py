import roxar2json
import roxar

project_path = r"D:\BigLoopAnalytics\RMS project\Emerald trimmed wells"
with roxar.Project.open(project_path, readonly=True) as project:
    wells = roxar2json.get_wells_geojson(project)
    lcs = roxar2json.get_logs_jsonwelllog(project)
print(wells)