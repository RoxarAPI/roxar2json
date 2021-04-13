import unittest, sys
import roxar2json, geojson, roxar_proxy

class TestGenerateColor(unittest.TestCase):
    def test_none(self):
        with self.assertRaises(AttributeError):
            rgba = roxar2json.generate_color(None)

    def test_empty(self):
        rgba = roxar2json.generate_color("")
        self.assertEqual(rgba, [255, 165, 172, 255])

class TestGeoJsonPoint(unittest.TestCase):
    def test_none(self):
        feature = geojson.create_point(None, None, None)
        self.assertEqual(
                feature,
                {
                    'type': 'Feature',
                    'geometry': {'type': 'Point', 'coordinates': None},
                    'properties': {'name': None, 'color': None}
                }
        )

class TestGeoJsonPolyline(unittest.TestCase):
    def test_none(self):
        feature = geojson.create_polyline(None, None, None)
        self.assertEqual(
                feature,
                {
                    'type': 'Feature',
                    'geometry': {'type': 'LineString', 'coordinates': None},
                    'properties': {'name': None, 'color': None}
                }
        )


class TestWellGeoJson(unittest.TestCase):
    def test_none(self):
        with self.assertRaises(AttributeError):
            roxar2json.get_well_geojson(None)

    def test_well_geojson(self):
        well = roxar_proxy.Well()
        with self.assertRaises(AttributeError):
            roxar2json.get_well_geojson(well)

        well.name = ""
        geometry = roxar2json.get_well_geojson(well)
        self.assertEqual(
            geometry,
            [
                {
                    'type': 'Feature',
                    'geometry': {'type': 'Point', 'coordinates': None},
                    'properties': {'name': '', 'color': [255, 165, 172, 255]}
                }
            ]
        )

class TestStratigraphyJson(unittest.TestCase):
    def test_none(self):
        with self.assertRaises(AttributeError):
            roxar2json.get_stratigraphy_json(None)

    def test_stratigraphy(self):
        project = roxar_proxy.Project()
        zones = project.zones
        horizons = project.horizons
        top = horizons.create("TopHorizon", roxar_proxy.HorizonType.calculated)
        bottom = horizons.create(
                "BottomHorizon", roxar_proxy.HorizonType.calculated)
        zone = zones.create("TestZone", top, bottom)
        stratigraphy = roxar2json.get_stratigraphy_json(project)
        self.assertEqual(
                stratigraphy,
                {
                    'horizons': ['TopHorizon', 'BottomHorizon'],
                    'zones': [{
                        'name': 'TestZone',
                        'horizon_above': 'TopHorizon',
                        'horizon_below': 'BottomHorizon',
                    }],
                }
        )

if __name__ == '__main__':
    result = unittest.main(exit=False, verbosity=1)
    sys.exit(not result.result.wasSuccessful())
