"Roxar 2 json unit tests."

import unittest
import sys
import json
import jsonschema
import numpy
import numpy.ma
import roxar_proxy
import roxar2json
from roxar2json import geojson


class TestGenerateColor(unittest.TestCase):
    def test_none(self):
        with self.assertRaises(AttributeError):
            roxar2json.generate_color(None)

    def test_empty(self):
        rgba = roxar2json.generate_color("")
        self.assertEqual(rgba, [255, 165, 172, 255])


class TestGeoJsonPoint(unittest.TestCase):
    def test_none(self):
        feature = geojson.create_point(None)
        self.assertEqual(feature, {"type": "Point", "coordinates": None})


class TestGeoJsonPolyline(unittest.TestCase):
    def test_none(self):
        feature = geojson.create_polyline(None)
        self.assertEqual(feature, {"type": "LineString", "coordinates": None})


class TestGeoJsonGeometryCollection(unittest.TestCase):
    def test_none(self):
        collection = geojson.create_collection(None)
        self.assertIsNone(collection["geometries"])


class TestGeoJsonFeature(unittest.TestCase):
    def test_none(self):
        geometry = geojson.create_point(None)
        name = None
        color = None
        feature = geojson.create_feature(geometry, name, color)
        self.assertEqual(
            feature,
            {
                "type": "Feature",
                "geometry": {"coordinates": None, "type": "Point"},
                "properties": {"color": None, "name": None},
            },
        )


class TestGeoJsonFeatureCollection(unittest.TestCase):
    def test_none(self):
        geometry = geojson.create_point([1, 2])
        name = None
        color = None
        feature = geojson.create_feature(geometry, name, color)
        self.assertEqual(
            feature,
            {
                "type": "Feature",
                "geometry": {"coordinates": [1, 2], "type": "Point"},
                "properties": {"color": None, "name": None},
            },
        )
        feature_collection = geojson.create_feature_collection([feature])
        schema = None
        with open("schema/FeatureCollection.json", encoding="utf-8") as schema_file:
            schema = json.load(schema_file)
        jsonschema.validate(instance=feature_collection, schema=schema)


class TestWellGeoJson(unittest.TestCase):
    def test_none(self):
        with self.assertRaises(AttributeError):
            roxar2json.get_well_geojson(None)

    def test_well_geojson(self):
        well = roxar_proxy.Well()

        well.name = ""

        well_head_geometry = {"type": "Point", "coordinates": None}

        collection = {
            "type": "GeometryCollection",
            "geometries": [well_head_geometry],
        }

        feature = {
            "type": "Feature",
            "geometry": collection,
            "properties": {"name": "", "color": [255, 165, 172, 255], "md": []},
        }

        geometry = roxar2json.get_well_geojson(well)
        self.assertEqual(geometry, feature)

    def test_well_trajectory(self):
        p0 = [0, 0, 0, 0]
        p1 = [1, 1, 1, 1]

        trajectory = roxar_proxy.Trajectory()
        trajectory.survey_point_series.set_measured_depths_and_points([p0, p1])

        data = trajectory.survey_point_series.get_measured_depths_and_points()

        self.assertEqual(data.tolist(), [p0, p1])

        geometry = roxar2json.get_trajectory_geojson(trajectory)
        self.assertEqual(
            geometry,
            {
                "type": "LineString",
                "coordinates": [
                    [0.0, 0.0, -0.0],
                    [1.0, 1.0, -1.0],
                ],
            },
        )

    def test_well_trajectory_collection(self):
        p0 = [0, 0, 0, 0]
        p1 = [1, 1, 1, 1]

        well = roxar_proxy.Well()
        well.name = ""

        trajectory = well.wellbore.trajectories.create("Trajectory")
        trajectory.survey_point_series.set_measured_depths_and_points([p0, p1])

        well_head_geometry = {"type": "Point", "coordinates": None}
        trajectory_geometry = {
            "type": "LineString",
            "coordinates": [
                [0, 0, 0],
                [1, 1, -1],
            ],
        }

        collection = {
            "type": "GeometryCollection",
            "geometries": [well_head_geometry, trajectory_geometry],
        }

        feature = {
            "type": "Feature",
            "geometry": collection,
            "properties": {"name": "", "color": [255, 165, 172, 255], "md": [[0, 1]]},
        }

        geometry = roxar2json.get_well_geojson(well)
        self.assertEqual(geometry, feature)


class TestJsonWellLog(unittest.TestCase):
    def setUp(self):
        self.log_run = roxar_proxy.LogRun()

    def test_none(self):
        with self.assertRaises(AttributeError):
            roxar2json.get_log_jsonwelllog(None, None)

    def test_empty_log_json_well_log(self):
        log = roxar2json.get_log_jsonwelllog(self.log_run, 20)

        self.assertEqual(
            log,
            {
                "header": {
                    "name": "LogRun",
                    "well": "Well",
                    "startIndex": None,
                    "endIndex": None,
                    "step": None,
                },
                "curves": [
                    {
                        "name": "MD",
                        "description": "continuous",
                        "quantity": "m",
                        "unit": "m",
                        "valueType": "float",
                        "dimensions": 1,
                        "interpolationType": "continuous",
                    },
                ],
                "data": [],
                "metadata_discrete": {},
            },
        )

    def test_empty_md(self):
        with self.assertRaises(ValueError):
            self.log_run.set_measured_depths([])

    def test_log_curve(self):
        self.log_run.set_measured_depths([1.0, 100.0])

        curve = self.log_run.log_curves.create_discrete("DiscreteLog")

        curve.set_values([1, 2])
        curve.set_code_names({1: "One"})
        curve.interpolation_type = roxar_proxy.LogCurveInterpolationType.interval

        log = roxar2json.get_log_jsonwelllog(self.log_run)

        self.assertEqual(
            log,
            {
                "header": {
                    "name": "LogRun",
                    "well": "Well",
                    "startIndex": 1.0,
                    "endIndex": 100.0,
                    "step": None,
                },
                "curves": [
                    {
                        "name": "MD",
                        "description": "continuous",
                        "quantity": "m",
                        "unit": "m",
                        "valueType": "float",
                        "dimensions": 1,
                        "interpolationType": "continuous",
                    },
                    {
                        "name": "DiscreteLog",
                        "description": "discrete",
                        "quantity": "DISC",
                        "unit": "DISC",
                        "valueType": "integer",
                        "dimensions": 1,
                        "interpolationType": "interval",
                    },
                ],
                "data": [(1.0, 1), (100.0, 2)],
                "metadata_discrete": {
                    "DiscreteLog": {
                        "attributes": ["color", "code"],
                        "objects": {"One": [[23, 36, 255, 255], 1]},
                    },
                },
            },
        )

    def test_interval_log(self):
        self.log_run.set_measured_depths([1, 2, 3, 4, 5, 6, 7, 8])

        curve = self.log_run.log_curves.create_discrete("DiscreteLog")

        curve.set_values([1, 2, 2, 2, 1, -999, -999, 1])
        curve.set_code_names({1: "One", 2: "Two"})
        curve.interpolation_type = roxar_proxy.LogCurveInterpolationType.interval

        logs = roxar2json.get_interval_logs(self.log_run)

        curve_data = logs[0]["data"]
        md = curve_data[0]
        values = curve_data[1]

        self.assertListEqual(md.tolist(), [1, 2, 5, 6, 8])
        self.assertListEqual(values.tolist(), [1, 2, 1, None, 1])

    def test_interval_log_end(self):
        self.log_run.set_measured_depths([1, 2, 3, 4])

        curve = self.log_run.log_curves.create_discrete("DiscreteLog")

        curve.set_values([1, 2, 2, 2])
        curve.set_code_names({1: "One", 2: "Two"})
        curve.interpolation_type = roxar_proxy.LogCurveInterpolationType.interval

        logs = roxar2json.get_interval_logs(self.log_run)

        curve_data = logs[0]["data"]
        md = curve_data[0]
        values = curve_data[1]

        self.assertListEqual(md.tolist(), [1, 2, 4])
        self.assertListEqual(values.tolist(), [1, 2, 2])

    def test_flat_interval(self):
        self.log_run.set_measured_depths([1, 2, 3, 4])

        curve = self.log_run.log_curves.create_discrete("DiscreteLog")

        curve.set_values([0, 0, 0, 0])
        curve.set_code_names({1: "One"})
        curve.interpolation_type = roxar_proxy.LogCurveInterpolationType.interval

        logs = roxar2json.get_interval_logs(self.log_run)

        curve_data = logs[0]["data"]
        md = curve_data[0]
        values = curve_data[1]

        self.assertListEqual(md.tolist(), [1, 4])
        self.assertListEqual(values.tolist(), [0, 0])

    def test_undefined_interval(self):
        self.log_run.set_measured_depths([1, 2, 3, 4])

        curve = self.log_run.log_curves.create_discrete("DiscreteLog")

        curve.set_values([-999, -999, -999, -999])
        curve.set_code_names({1: "One"})
        curve.interpolation_type = roxar_proxy.LogCurveInterpolationType.interval

        logs = roxar2json.get_interval_logs(self.log_run)

        curve_data = logs[0]["data"]
        md = curve_data[0]
        values = curve_data[1]

        self.assertListEqual(md.tolist(), [1, 4])
        self.assertListEqual(values.tolist(), [None, None])

    def test_interval_mask(self):
        curve = numpy.ma.masked_array(
            [1, 2, 2, 2, -999, -999, 1], [False, False, False, False, True, True, False]
        )
        mask = roxar2json.get_interval_mask(curve)
        self.assertEqual(mask.tolist(), [False, False, True, True, False, True, False])

    def test_interval_mask_zero(self):
        curve = numpy.ma.masked_array(
            [0, 0, 0, 0], [False, False, False, False]
        )
        mask = roxar2json.get_interval_mask(curve)
        self.assertEqual(mask.tolist(), [False, True, True, True])


class TestStratigraphyJson(unittest.TestCase):
    def test_none(self):
        with self.assertRaises(AttributeError):
            roxar2json.get_stratigraphy_json(None)

    def test_stratigraphy(self):
        project = roxar_proxy.Project()
        zones = project.zones
        horizons = project.horizons
        top = horizons.create("TopHorizon", roxar_proxy.HorizonType.calculated)
        bottom = horizons.create("BottomHorizon", roxar_proxy.HorizonType.calculated)
        zones.create("TestZone", top, bottom)
        stratigraphy = roxar2json.get_stratigraphy_json(project)
        self.assertEqual(
            stratigraphy,
            {
                "horizons": ["TopHorizon", "BottomHorizon"],
                "zones": [
                    {
                        "name": "TestZone",
                        "horizon_above": "TopHorizon",
                        "horizon_below": "BottomHorizon",
                    }
                ],
            },
        )


if __name__ == "__main__":
    result = unittest.main(exit=False, verbosity=1)
    sys.exit(not result.result.wasSuccessful())
