import unittest
import os
import wasdi

from unittest.mock import patch
from src.main.ImageGeneration import Layer
from src.main.ImageGeneration.generateBackgroundTile import fetch_tile, merge_tiles, georeference_raster_tile, \
    generateBackground, overlapTiles


class testGenBack(unittest.TestCase):
    def setUp(self):
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
        self.layer.process_layer(True)

        self.provider = "osm"
        # Create a temporary directory for testing
        self.temp_dir = "temp_test_dir"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def tearDown(self):
        # Clean up the temporary directory after the tests
        pass

    def test_fetch_tile1(self):
        # Test the fetch_tile function
        x = 173
        y = 98
        z = 8
        tile_source = 'http://tile.openstreetmap.org/{z}/{x}/{y}.{ext}'
        path = fetch_tile(x, y, z, tile_source, self.temp_dir)

        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))
        self.assertEqual(path, self.temp_dir + "/173_98_8.png")

    def test_fetch_tile2(self):
        # Test the fetch_tile function
        x = 173
        y = 99
        z = 8
        tile_source = 'http://tile.openstreetmap.org/{z}/{x}/{y}.{ext}'
        path = fetch_tile(x, y, z, tile_source, self.temp_dir)

        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))
        self.assertEqual(path, self.temp_dir + "/173_99_8.png")

    def test_georeference_raster_tile1(self):
        # Test the georeference_raster_tile function (requires a valid input file)
        x = 173
        y = 98
        z = 8
        path = self.temp_dir + "/173_98_8.png"
        georeference_raster_tile(x, y, z, path)

        output_file_path = self.temp_dir + "/173_98_8.tif"
        # Check if the file exists
        assert os.path.exists(output_file_path)

    def test_georeference_raster_tile2(self):
        # Test the georeference_raster_tile function (requires a valid input file)
        x = 173
        y = 99
        z = 8
        path = self.temp_dir + "/173_99_8.png"
        georeference_raster_tile(x, y, z, path)

        output_file_path = self.temp_dir + "/173_99_8.tif"
        # Check if the file exists
        assert os.path.exists(output_file_path)

    def test_merge_tiles(self):
        # Test the merge_tiles function
        input_path = os.path.abspath(self.temp_dir + "/*.tif")
        output_path = os.path.abspath(self.temp_dir + "/merged.tif")

        merge_tiles(input_path, output_path)

    @patch('src.main.ImageGeneration.generateBackgroundTile.fetch_tile')
    @patch('src.main.ImageGeneration.generateBackgroundTile.georeference_raster_tile')
    @patch('src.main.ImageGeneration.generateBackgroundTile.merge_tiles')
    def test_generateBackground(self, mock_fetch_tile, mock_georeference, mock_merge):
        # Test the generateBackground function
        generateBackground(self.provider, self.layer)

        mock_fetch_tile.assert_called_with(wasdi.getSavePath()+"temp/*.tif", wasdi.getSavePath()+"output/merged.tif")
        mock_merge.assert_called_with(180, 110, 8, "http://tile.openstreetmap.org/{z}/{x}/{y}.{ext}",
                                      wasdi.getSavePath() + "temp")

        output_file_path = wasdi.getSavePath() + "/mosaic.tif"

        # Check if the file exists
        assert os.path.exists(output_file_path)


if __name__ == '__main__':
    unittest.main()