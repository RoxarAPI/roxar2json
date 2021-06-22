import json
import roxar
import roxar2json

#project_path = r"D:\BigLoopAnalytics\RMS project\Emerald trimmed wells 2"
#project_path = r"D:\Projects\Volve3"
project_path = r"D:\BigLoopAnalytics\RMS project\volve_11.1.0_v1h.pro"
with roxar.Project.open(project_path, readonly=True) as project:
    #wells = roxar2json.get_wells_geojson(project)
    lcs = roxar2json.get_logs_jsonwelllog(project, ['BLOCKING', 'CORE_PLUG'], 0.154)
    lcs_json = json.dumps(lcs, indent=None)
    with open("D:\\BigLoopAnalytics\\data files\\154cm_continuous_new3.json", "w") as outfile:
        outfile.write(lcs_json)
print("Done")
