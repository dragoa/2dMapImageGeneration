import json
import os

import owslib.util
import requests
import requests.exceptions
import wasdi
# Import the WebMapService class from owslib.wms
from owslib.wms import WebMapService


class Layer:
    def __init__(self, product, band, bbox, crs, width, height, img_format, style, geoserver_url, layer_id):
        self.wms = None
        self.product = product
        self.band = band
        self.bbox = bbox
        self.crs = crs
        self.width = width
        self.height = height
        self.format = img_format
        self.style = style
        self.geoserver_url = geoserver_url
        self.layer_id = layer_id

    def create_web_map_service(self):

        try:
            self.wms = WebMapService(self.geoserver_url, version='1.3.0')

        except Exception as oEx:
            wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
            wasdi.updateStatus("ERROR", 0)
            return None

    def create_query_wms(self, to_bounding_box_list):

        # Create a query to the WMS
        parameters = {
            'service': 'WMS',
            'version': '1.3.0',
            'request': 'GetMap',
            'layers': [self.layer_id],
            'styles': [self.style],
            'srs': self.crs,
            'bbox': (to_bounding_box_list[:4]),
            'size': (self.width, self.height),
            'format': f'image/{self.format}',
            'dpi': 120,
            'map_resolution': 120,
            'format_options': 'dpi:120',
            'transparent': True,
            'product': self.product
        }

        return parameters

    def get_map_request(self, params):

        try:
            # Make the request and save the response as a file
            response = self.wms.getmap(**params)
            # Specify the folder path
            folder_path = "img/"

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Construct the file path
            file_path = os.path.join(folder_path, f"{params['product']}.{self.format}")

            with open(file_path, "wb") as o:
                o.write(response.read())
                wasdi.wasdiLog('Map image saved successfully.')
                # wasdi.addFileToWASDI("map.tiff", "")  # You can add this line if needed

        except requests.exceptions.ConnectionError:
            # Handle network errors
            wasdi.wasdiLog('Could not connect to the WMS server.')
        except owslib.util.ServiceException as oEx:
            # Handle server errors
            wasdi.wasdiLog(f'The WMS server returned an error: {repr(oEx)}')
        except Exception as oEx:
            # Handle any other error
            wasdi.wasdiLog(f'An unknown error occurred: {repr(oEx)}')
            wasdi.updateStatus("ERROR", 0)
            return None

    def process_layer(self, b_stack_layers):

        if self.wms is None:

            # Get all the products in the WASDI workspace
            as_get_products = wasdi.getProductsByActiveWorkspace()
            if self.product not in as_get_products:
                wasdi.wasdiLog("An error occurred: The selected product is not in the workspace.")
                wasdi.updateStatus("ERROR", 0)
                return None

            try:
                # try to connect to the provided Geoserver url
                if self.geoserver_url == "":
                    # Starts a publish band process and wait for the result to be available
                    s_json_result = wasdi.getlayerWMS(self.product, self.band)
                    # Convert the string to a Python object
                    data = json.loads(s_json_result)
                    print(data)

                    # Define the base URL of the WMS server
                    self.geoserver_url = data["server"]
                    self.layer_id = f"wasdi:{data['layerId']}"

                self.create_web_map_service()

            except Exception as ex:
                wasdi.wasdiLog(f'An error occurred: {repr(ex)}')
                wasdi.updateStatus("ERROR", 0)
                return None

            to_bounding_box_list = self.get_bounding_box_list()

            layers_to_stack = []

            if b_stack_layers:
                layers_to_stack.append([self])
                pass
            else:
                # Create the query and then get the map
                parameters = self.create_query_wms(to_bounding_box_list)
                self.get_map_request(parameters)

    def get_bounding_box_list(self):
        try:
            if self.bbox == "":
                # Get the bounding box and the correspondent coordinate system
                to_bounding_box_list = self.wms[self.layer_id].boundingBox
                wasdi.wasdiLog(f"The Bounding Box used is {to_bounding_box_list}")
            else:
                to_bounding_box_list = [float(x) for x in self.bbox.split(",")]
                to_bounding_box_list.append(self.crs)
            return to_bounding_box_list

        except Exception as ex:
            wasdi.wasdiLog(f'An error occurred: {repr(ex)}')
            wasdi.updateStatus("ERROR", 0)
            return None

    def process_layers(self, layers):
        wasdi.wasdiLog("You are now stacking layers!")
        to_bounding_box_list = self.get_bounding_box_list()

        layer_ids = []
        styles = []
        for layer in layers:
            layer_ids.append(layer.layer_id)
            styles.append(layer.style)

        # Create a query to the WMS
        parameters = {
            'service': 'WMS',
            'version': '1.3.0',
            'request': 'GetMap',
            'layers': layer_ids,
            'styles': styles,
            'srs': self.crs,
            'bbox': (to_bounding_box_list[:4]),
            'size': (self.width, self.height),
            'format': f'image/{self.format}',
            'dpi': 120,
            'map_resolution': 120,
            'format_options': 'dpi:120',
            'transparent': True,
            'product': self.product
        }
        self.get_map_request(parameters)


def run():
    wasdi.wasdiLog("WMS client tutorial v.1.1")

    aoProducts = wasdi.getParameter("products")
    bStackLayers = wasdi.getParameter("stackLayers")

    layers = []

    for oProduct in aoProducts:
        # Read from params the bands we want to extract and the product
        sProduct = oProduct["PRODUCT"]
        sBand = oProduct["BAND"]
        sBBox = oProduct["BBOX"]
        sCRS = oProduct["CRS"]
        sWidth = oProduct["WIDTH"]
        sHeight = oProduct["HEIGHT"]
        sFormat = str.casefold(oProduct["FORMAT"])
        sStyle = oProduct["STYLE"]
        sGeoServerUrl = oProduct["GEOSERVER URL"]
        sLayerId = oProduct["LAYER ID"]

        # Check the Bounding Box: is needed
        if sBBox != "":
            # Split the BBox: it is in the format: NORTH, WEST, SOUTH, EAST
            asBBox = sBBox.split(",")
            if len(asBBox) != 4:
                wasdi.wasdiLog("BBOX Not valid. Please use LATN,LONW,LATS,LONE")
                wasdi.wasdiLog("BBOX received:" + sBBox)
                wasdi.wasdiLog("exit")
                wasdi.updateStatus("ERROR", 0)
                return None

        # Check the CRS: is needed
        if sCRS == "":
            wasdi.wasdiLog("CRS Parameter not set.")

        layer = Layer(
            sProduct,
            sBand,
            sBBox,
            sCRS,
            sWidth,
            sHeight,
            sFormat,
            sStyle,
            sGeoServerUrl,
            sLayerId
        )

        # check for GeoServer url
        if sGeoServerUrl != "" and sLayerId != "":
            layer.geoserver_url = sGeoServerUrl
            layer.layer_id = sLayerId

        layers.append(layer)

        for layer in layers:
            layer.process_layer(bStackLayers)

    if bStackLayers:
        process_layers(layers)


def process_layers(layers):
    layers[0].process_layers(layers)


if __name__ == "__main__":
    wasdi.init('./config.json')
    run()
