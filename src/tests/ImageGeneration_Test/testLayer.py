import unittest

import wasdi

# Import the Layer class from your module
from src.main.ImageGeneration import Layer


class TestLayer(unittest.TestCase):

    def setUp(self):
        # Initialize any common setup you need for your tests here
        wasdi.init('./config.json')
        self.layer = Layer.Layer("lulc_map.tif",
                                 "band_1",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "",
                                 1
                                 )

    def tearDown(self):
        # Clean up any resources after each test case here
        pass

    def test_process_layer(self):
        result = self.layer.process_layer(b_stack_layers=True)

        # Access the to_bounding_box_list attribute
        to_bounding_box_list = self.layer.get_bounding_box_list()

        self.assertEqual(self.layer.band, "band_1")
        self.assertEqual(self.layer.bbox, "")
        self.assertEqual(self.layer.crs, "EPSG:4326")
        self.assertEqual(self.layer.filename, "")
        self.assertEqual(self.layer.format, "geotiff")
        self.assertNotEqual(self.layer.geoserver_url, "")
        self.assertNotEqual(self.layer.height, "")
        self.assertNotEqual(self.layer.layer_id, "")
        self.assertEqual(self.layer.product, "lulc_map.tif")
        self.assertEqual(self.layer.stack, 1)
        self.assertEqual(self.layer.style, "")
        self.assertNotEqual(self.layer.width, "")
        self.assertEqual(self.layer.wms.url, self.layer.geoserver_url)

        self.assertNotEqual(to_bounding_box_list, "")
        self.assertTrue(result, "Processing was successful")

    def test_process_layers1(self):
        layer1 = Layer.Layer("PAK_2022-12-04_flood (1).tif",
                             "band_1",
                             "",
                             "",
                             "",
                             "",
                             "",
                             "",
                             "",
                             "",
                             1)
        self.layer.process_layer(b_stack_layers=True)
        layer1.process_layer(b_stack_layers=True)

        layers = [self.layer, layer1]
        # computing the union of bboxes
        result = layers[0].process_layers(layers, 0)

        self.assertTrue(result, "Stacking of layers was successful")

    def test_process_layers2(self):
        layer1 = Layer.Layer("PAK_2022-12-04_flood (1).tif",
                             "band_1",
                             "",
                             "",
                             "",
                             "",
                             "",
                             "",
                             "",
                             "",
                             1)
        self.layer.process_layer(b_stack_layers=True)
        layer1.process_layer(b_stack_layers=True)

        layers = [self.layer, layer1]
        # computing the union of bboxes
        result = layers[0].process_layers(layers, 1)

        self.assertTrue(result, "Stacking of layers was successful")

    def test_process_layers3(self):
        # band = "" so default one is assigned
        # using bbox provided by user
        layer1 = Layer.Layer("PAK_2022-12-04_flood (1).tif",
                             "",
                             "65.99983333333333, 23.750083333333336, 73.99983333333333, 37.750166666666665",
                             "",
                             "",
                             "",
                             "",
                             "",
                             "",
                             "",
                             1)
        self.layer.process_layer(b_stack_layers=True)
        layer1.process_layer(b_stack_layers=True)

        layers = [self.layer, layer1]
        # computing the union of bboxes
        result = layers[0].process_layers(layers, 2)

        self.assertTrue(result, "Stacking of layers was successful")

    def test_create_query_wms(self):
        # Test case 1: Verify the construction of the query dictionary
        layers = ['layer1', 'layer2']
        styles = 'style1'
        bounding_box = [10, 20, 30, 40]
        expected_parameters = {
            'service': 'WMS',
            'version': '1.3.0',
            'request': 'GetMap',
            'layers': layers,
            'styles': styles,
            'srs': self.layer.crs,
            'bbox': bounding_box,
            'size': (self.layer.width, self.layer.height),
            'format': f'image/{self.layer.format}',
            'dpi': 120,
            'map_resolution': 120,
            'format_options': 'dpi:120',
            'transparent': True,
            'product': self.layer.product
        }

        result = self.layer.create_query_wms(layers, styles, bounding_box)
        self.assertEqual(result, expected_parameters)

    def test_validate_params_with_invalid_crs(self):
        # Create a Layer object with an invalid CRS
        layer = Layer.Layer("lulc_map.tif", "band_1", "", "", "InvalidCRS", "600", "600", "", "", "", 1)

        # Call the validate_params method
        layer.validate_params()

        # Assert that the CRS is set to the default value "EPSG:4326"
        self.assertEqual(layer.crs, "EPSG:4326")

    def test_validate_params_with_valid_bbox_dict(self):
        # Create a Layer object with a valid bbox in dictionary format
        bbox_dict = {
            "northEast": {"lat": 20, "lng": 10},
            "southWest": {"lat": 15, "lng": 5}
        }
        layer = Layer.Layer("lulc_map.tif", "band_1", bbox_dict, "EPSG:4326", "600", "600", "", "", "", "", 1)

        # Call the validate_params method
        layer.validate_params()

        # Assert that the bbox is correctly formatted
        self.assertEqual(layer.bbox, "10, 20, 5, 15")

    def test_validate_params_with_invalid_bbox_format(self):
        # Create a Layer object with an invalid bbox format
        invalid_bbox = "10,20,30"  # Missing one coordinate
        layer = Layer.Layer("lulc_map.tif", "band_1", invalid_bbox, "", "600", "600", "", "", "", "", 1)

        # Call the validate_params method
        layer.validate_params()

        # Assert that the bbox is set to an empty string
        self.assertEqual(layer.bbox, "")

    def test_set_size(self):
        # Create a Layer object with a known bounding box
        layer = Layer.Layer("lulc_map.tif", "band_1", "", "", "", "", "", "", "", "", 1)

        # Mock the get_bounding_box_list method to return a known bounding box
        layer.get_bounding_box_list = lambda: [0, 0, 10, 10]  # Replace with your actual bounding box values

        # Call the set_size method
        layer.set_size()

        # Check if width and height have been set correctly
        self.assertEqual(layer.width, 1000)  # Width should be 10 * 100
        self.assertEqual(layer.height, 1000)  # Height should be 10 * 100

    def test_calculate_bbox_intersection(self):
        # Create test data for bbox intersections
        bbox1 = (0, 0, 10, 10, "EPSG:4326")
        bbox2 = (5, 5, 15, 15, "EPSG:4326")

        # Calculate the intersection
        intersection = Layer.calculate_bbox_intersection(bbox1, bbox2)

        # Assert that the intersection is as expected
        self.assertEqual(intersection, (5, 5, 10, 10))

    def test_calculate_bbox_union(self):
        # Create test data for bbox unions
        bbox1 = (0, 0, 10, 10, "EPSG:4326")
        bbox2 = (5, 5, 15, 15, "EPSG:4326")

        # Calculate the union
        union = Layer.calculate_bbox_union(bbox1, bbox2)

        # Assert that the union is as expected
        self.assertEqual(union, (0, 0, 15, 15))


if __name__ == '__main__':
    unittest.main()
