import glob
import os
import shutil
import urllib.request

import osgeo_utils.gdal_merge as gm
import wasdi
from osgeo import gdal

from tile_convert import bbox_to_xyz, tile_edges

import geotiler


def fetch_tile(x, y, z, tile_source, temp_dir):
    headers = {'User-Agent': 'Your-User-Agent-Name'}
    url = tile_source.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z)).replace(
        "{ext}", "png").replace(
        "{subdomain}", "a")

    req = urllib.request.Request(url, headers=headers)
    path = f'{temp_dir}/{x}_{y}_{z}.png'

    try:
        with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except urllib.error.URLError as e:
        print(f"Failed to retrieve tile at URL: {url}")
        print(f"Error: {e}")
        return None

    return path


def merge_tiles(input_pattern, output_path):
    params = ['', '-o', output_path]
    for name in glob.glob(input_pattern):
        params.append(name)
    gm.gdal_merge(params)


def georeference_raster_tile(x, y, z, path, provider):
    bounds = tile_edges(x, y, z)
    filename, extension = os.path.splitext(path)

    # Try with -r option
    if provider == "osm":
        gdal.Translate(filename + '.tif',
                       path,
                       outputSRS='EPSG:4326',
                       outputBounds=bounds,
                       options=["-ot", "Byte", "-expand", "rgb"])
    else:
        gdal.Translate(filename + '.tif',
                       path,
                       outputSRS='EPSG:4326',
                       outputBounds=bounds)


def run():
    wasdi.wasdiLog("Background tiles and overlapping of tifs v.1.1")

    provider = "stamen-toner-lite"
    tile_source = geotiler.find_provider(provider).url

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
                georeference_raster_tile(x, y, zoom, png_path, provider)
                # Add filename in a list
            except OSError:
                wasdi.wasdiLog(f"{x},{y} missing")
                pass

    wasdi.wasdiLog("Fetching of tiles complete")

    wasdi.wasdiLog("Merging tiles")
    merge_tiles(temp_dir + '/*.tif', output_dir + '/merged.tif')
    wasdi.wasdiLog("Merge complete")

    shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)


if __name__ == "__main__":
    wasdi.init('./config.json')
    run()
