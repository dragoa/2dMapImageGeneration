import wasdi
import urllib.request
import os
import glob
import subprocess
import shutil
from tile_convert import bbox_to_xyz, tile_edges
from osgeo import gdal


def fetch_tile(x, y, z, tile_source, temp_dir):
    url = tile_source.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z))
    path = f'{temp_dir}/{x}_{y}_{z}.png'
    urllib.request.urlretrieve(url, path)
    return path


def merge_tiles(input_pattern, output_path):
    merge_command = ["python", 'gdal_merge.py', '-o', output_path]

    for name in glob.glob(input_pattern):
        merge_command.append(name)

    subprocess.call(merge_command)


def georeference_raster_tile(x, y, z, path):
    bounds = tile_edges(x, y, z)
    filename, extension = os.path.splitext(path)
    gdal.Translate(filename + '.tif',
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)


def run():
    wasdi.wasdiLog("Background tiles and overlapping of tifs v.1.1")

    # Define a tile source. For now, we use mapbox
    mapBoxToken = "pk.eyJ1Ijoicm9iZXJ0OTAyMCIsImEiOiJjbGx0cGJ2bzMwc2dsM2dueml3NmNyazdwIn0.fGV_gn9SWcLf3bghozVfEw"
    tile_source = ("https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=" + mapBoxToken)

    # TODO Read from params BBOX and zoom and CRS
    lon_min = 22.673583850264553
    lon_max = 24.848876819014553
    lat_min = 37.71359330111474
    lat_max = 39.278404231638525
    zoom = 8

    # Local path of wasdi
    sWASDIsavePath = wasdi.getSavePath()
    # Create two directories
    temp_dir = os.path.join(sWASDIsavePath, "temp")
    output_dir = os.path.join(sWASDIsavePath, "output")

    # Check if the directory already exists
    if not os.path.exists(temp_dir):
        # Create the new directory and any missing intermediate directories
        os.makedirs(temp_dir)
    else:
        print(f"Directory '{temp_dir}' already exists.")
    if not os.path.exists(output_dir):
        # Create the new directory and any missing intermediate directories
        os.makedirs(output_dir)
    else:
        print(f"Directory '{output_dir}' already exists.")

    x_min, x_max, y_min, y_max = bbox_to_xyz(
        lon_min, lon_max, lat_min, lat_max, zoom)

    wasdi.wasdiLog(f"Fetching {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            try:
                png_path = fetch_tile(x, y, zoom, tile_source, temp_dir)
                wasdi.wasdiLog(f"{x},{y} fetched")
                georeference_raster_tile(x, y, zoom, png_path)
            except OSError:
                wasdi.wasdiLog(f"{x},{y} missing")
                pass

    wasdi.wasdiLog("Fetching of tiles complete")

    wasdi.wasdiLog("Merging tiles")
    merge_tiles(temp_dir + '/*.tif', output_dir + '/merged.tif')
    wasdi.wasdiLog("Merge complete")

    # shutil.rmtree(temp_dir)
    # os.makedirs(temp_dir)


if __name__ == "__main__":
    wasdi.init('./config.json')
    run()
