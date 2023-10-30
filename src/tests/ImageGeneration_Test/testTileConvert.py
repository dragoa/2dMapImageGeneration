import unittest
from src.main.ImageGeneration.tileConvert import latlon_to_xyz, bbox_to_xyz, mercatorToLat, y_to_lat_edges, x_to_lon_edges, tile_edges


class testTileConvert(unittest.TestCase):

    def test_latlon_to_xyz(self):
        # Test the latlon_to_xyz function
        lat = 23.750083333333336
        lon = 63.99988321407197
        z = 8
        x, y = latlon_to_xyz(lat, lon, z)
        self.assertEqual(x, 173.5110280633401)
        self.assertEqual(y, 110.60552358383444)

    def test_bbox_to_xyz(self):
        # Test the bbox_to_xyz function
        lon_min = 63.99988321407197
        lon_max = 73.99983333333333
        lat_min = 23.750083333333336
        lat_max = 37.750166666666665
        z = 8
        x_min, x_max, y_min, y_max = bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z)
        self.assertEqual(x_min, 173)
        self.assertEqual(x_max, 180)
        self.assertEqual(y_min, 98)
        self.assertEqual(y_max, 110)

    def test_mercatorToLat(self):
        # Test the mercatorToLat function
        mercatorY = 0
        lat = mercatorToLat(mercatorY)
        self.assertEqual(lat, 0)

    def test_y_to_lat_edges(self):
        # Test the y_to_lat_edges function
        y = 98
        z = 8
        lat1, lat2 = y_to_lat_edges(y, z)
        self.assertEqual(lat1, 38.8225909761771)
        self.assertEqual(lat2, 37.718590325588146)

    def test_x_to_lon_edges(self):
        # Test the x_to_lon_edges function
        x = 0
        z = 0
        lon1, lon2 = x_to_lon_edges(x, z)
        self.assertEqual(lon1, -180.0)
        self.assertEqual(lon2, 180.0)

    def test_tile_edges(self):
        # Test the tile_edges function
        x = 173
        y = 98
        z = 8
        edges = tile_edges(x, y, z)
        self.assertEqual(edges, [63.28125, 38.8225909761771, 64.6875, 37.718590325588146])


if __name__ == '__main__':
    unittest.main()
