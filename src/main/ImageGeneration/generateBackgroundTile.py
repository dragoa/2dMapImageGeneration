import glob
import os
import shutil
import urllib.request

import osgeo_utils.gdal_merge as gm
import wasdi
from osgeo import gdal

from tileConvert import bbox_to_xyz, tile_edges

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
        wasdi.wasdiLog(f"Failed to retrieve tile at URL: {url}")
        wasdi.wasdiLog(f"Error: {e}")
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


def generateBackground(provider, layer):
    wasdi.wasdiLog("Background tiles and overlapping of tifs v.1.1")

    provider = provider
    tile_source = geotiler.find_provider(provider).url

    if layer.bbox != "":
        bbox = layer.bbox
        bbox = [float(x) for x in bbox.split(",")]
    else:
        bbox = layer.get_bounding_box_list()

    lon_min = bbox[0]
    lon_max = bbox[2]
    lat_min = bbox[1]
    lat_max = bbox[3]
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
        wasdi.wasdiLog(f"Directory '{temp_dir}' already exists.")
    if not os.path.exists(output_dir):
        # Create the new directory and any missing intermediate directories
        os.makedirs(output_dir)
    else:
        wasdi.wasdiLog(f"Directory '{output_dir}' already exists.")

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

    overlapTiles(layer, output_dir + '/merged.tif')


def overlapTiles(layer, merged):

    filename_path = wasdi.getSavePath() + str(layer.filename) + "." + layer.format
    onTopLayer = filename_path

    import subprocess

    src_ds = gdal.Open(filename_path)

    if src_ds.RasterCount == 1:
        onTopLayer = "layer_rgb.tif"
        # Define the gdal_translate command as a list of strings
        gdal_translate_command = [
            'gdal_translate',  # Command name
            '-expand', 'rgb',  # Arguments
            filename_path,
            onTopLayer
        ]

        # Execute the gdal_translate command
        try:
            subprocess.run(gdal_translate_command, check=True)
            wasdi.wasdiLog("gdal_translate completed successfully.")
        except subprocess.CalledProcessError as e:
            wasdi.wasdiLog(f"Error: gdal_translate command failed with exit code {e.returncode}")

        onTopTrLayer = "layer_tr.tif"
        # Use gdal.Warp with dstNodata option
        g = gdal.Warp(onTopTrLayer, onTopLayer, dstNodata="51, 51, 51")
        onTopLayer = onTopTrLayer

    # Define the input files
    files_to_mosaic = [merged, onTopLayer]

    # Define the output file
    output_file = "mosaic.tif"

    # Merge the input files using gdal.Warp
    g = gdal.Warp(output_file, files_to_mosaic, format="GTiff", options=["COMPRESS=LZW", "TILED=YES"])

    # Close the output file and flush to disk
    g = None