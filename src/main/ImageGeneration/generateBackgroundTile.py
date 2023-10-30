import glob
import os
import shutil
import urllib.request

import geotiler
import wasdi
from osgeo import gdal

from src.main.ImageGeneration.tileConvert import bbox_to_xyz, tile_edges


def fetch_tile(x, y, z, tile_source, temp_dir):
    """
    Create a request to a map service provider
    :param x: int longitude
    :param y: int altitude
    :param z: int latitude
    :param tile_source: str preferred tile source for the map
    :param temp_dir: str temporary directory for saving tiles
    :return: str path for fetched tiles
    """
    headers = {'User-Agent': 'Your-User-Agent-Name'}
    # Creating the url
    url = tile_source.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z)).replace(
        "{ext}", "png").replace(
        "{subdomain}", "a")

    # Making the request
    req = urllib.request.Request(url, headers=headers)
    path = f'{temp_dir}/{x}_{y}_{z}.png'

    try:
        with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
            data = response.read()
            # Write the response
            out_file.write(data)
    except urllib.error.URLError as e:
        wasdi.wasdiLog(f"Failed to retrieve tile at URL: {url}")
        wasdi.wasdiLog(f"Error: {e}")
        return None

    return path


def merge_tiles(input_pattern, output_path):
    """
    Merge every tile to create only a single one
    :param input_pattern: str temporary directory of all the fetched tile
    :param output_path: output directory for saving final tile
    :return: a single tile from all the fetched ones
    """
    # create the param string for gdal merge
    params = ['/usr/bin/gdal_merge.py', '-o', output_path]
    for name in glob.glob(input_pattern):
        params.append(name)
    # gdal command to merge tiles
    os.system(' '.join(params))


def georeference_raster_tile(x, y, z, path):
    """
    Georeferenciate each tile
    :param x: longitude
    :param y: altitude
    :param z: latitude
    :param path: str path for fetched tiles
    :return:
    """
    bounds = tile_edges(x, y, z)
    filename, extension = os.path.splitext(path)

    # Try with -r option
    gdal.Translate(filename + '.tif',
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds,
                   options=["-ot", "Byte", "-expand", "rgb"])


def generateBackground(provider, layer):
    """
    Method for generating background tile
    :param provider: str map service provider
    :param layer: Layer base layer for creating a background
    :return:
    """
    wasdi.wasdiLog("Background tiles and overlapping of tifs v.1.1")

    provider = provider

    # check if the tile provider is correct
    try:
        tile_source = geotiler.find_provider(provider).url
    except FileNotFoundError as oEx:
        wasdi.wasdiLog("[ERROR] the selected tile provider is not supported. Using osm")
        wasdi.wasdiLog({repr(oEx)})
        tile_source = geotiler.find_provider("osm").url
    except Exception as oEx:
        wasdi.wasdiLog("[ERROR] occurred when contacting the server provider. Using osm")
        wasdi.wasdiLog({repr(oEx)})
        tile_source = geotiler.find_provider("osm").url

    # getting the bbox
    if layer.bbox != "":
        bbox = layer.bbox
    else:
        bbox = layer.get_bounding_box_list()

    # computing latitude and longitude and zoom level
    lon_min = bbox[0]
    lon_max = bbox[2]
    lat_min = bbox[1]
    lat_max = bbox[3]
    zoom = 8

    # local path of wasdi
    sWASDIsavePath = wasdi.getSavePath()
    # create two directories
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

    # get the range of tiles for a specified rectangular area/bounding box
    x_min, x_max, y_min, y_max = bbox_to_xyz(
        lon_min, lon_max, lat_min, lat_max, zoom)

    wasdi.wasdiLog(f"Fetching {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            try:
                png_path = fetch_tile(x, y, zoom, tile_source, temp_dir)
                wasdi.wasdiLog(f"{x},{y} fetched")
                georeference_raster_tile(x, y, zoom, png_path)
                # Add filename in a list
            except OSError:
                wasdi.wasdiLog(f"{x},{y} missing")
                pass
            except Exception as oEx:
                wasdi.wasdiLog(f"[ERROR] {repr(oEx)}")
                wasdi.wasdiLog("Check API key for provider or try to use osm")
                return None

    wasdi.wasdiLog("Fetching of tiles complete")

    wasdi.wasdiLog("Merging tiles")
    # merge tiles
    merge_tiles(temp_dir + '/*.tif', output_dir + '/merged.tif')
    wasdi.wasdiLog("Merge complete")

    # removing data in the temp directory
    shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # final overlapping
    overlapTiles(layer, output_dir + '/merged.tif')


def overlapTiles(layer, merged):
    """
    Method for overlapping the stacked layers on top of the background tile
    :param layer: Layer created layer
    :param merged: str directory for merged tiles
    :return:
    """

    filename_path = wasdi.getSavePath() + str(layer.filename) + "." + layer.format
    onTopLayer = filename_path

    # Define the input files
    files_to_mosaic = [merged, onTopLayer]

    # Define the output file
    output_file = wasdi.getSavePath() + "/mosaic.tif"

    # Merge the input files using gdal.Warp
    g = gdal.Warp(output_file, files_to_mosaic, format="GTiff", options=["COMPRESS=LZW", "TILED=YES"])

    # Close the output file and flush to disk
    g = None
