import json
import os

import owslib.util
import requests
import requests.exceptions
import wasdi
# Import the WebMapService class from owslib.wms
from owslib.wms import WebMapService


class Layer:
    """
    Custom representation of a Layer

    Attributes
    ----------
    product : str
        Identifier for a product inside the WASDI workspace
    band : str
        Identifier for the band of the product
    bbox : str
        Bbox options used for selecting an area in the world
    crs : str
        Coordinate Reference System used
    width : int
        Width of the image
    height : int
        Height of the image
    style : str
        Name of a sld style file present on a WASDI workspace
    sFileName : str
        Name of the output image
    geoserver_url : str
        Link for a custom geoserver url
    layer_id : str
        Identifier of a layer in a Geoserver workspace
    iStackOrder : int
        Order on which we want to stack layers
    """

    def __init__(self, product, band, bbox, crs, width, height, style, sFileName,
                 geoserver_url, layer_id, iStackOrder):
        self.wms = None
        self.product = product
        self.band = band
        self.bbox = bbox
        self.crs = crs
        self.width = width
        self.height = height
        self.format = "geotiff"
        self.style = style
        self.geoserver_url = geoserver_url
        self.layer_id = layer_id
        self.filename = sFileName
        self.stack = iStackOrder

    def validate_params(self):
        """
        Validate arguments for a Layer
        """
        # If the crs is not correct set a default one
        if self.crs not in self.wms[self.layer_id].crsOptions:
            wasdi.wasdiLog("The crs value is not correct. Setting EPSG:4326 as default")
            self.crs = "EPSG:4326"

        # Check for the bbox
        if self.bbox is not None:
            # Split the BBox: it is in the format: WEST, NORTH, EAST, SOUTH
            if isinstance(self.bbox, dict):
                # Extract latitude and longitude values
                west = self.bbox.get("northEast", {}).get("lng", "")
                north = self.bbox.get("northEast", {}).get("lat", "")
                east = self.bbox.get("southWest", {}).get("lng", "")
                south = self.bbox.get("southWest", {}).get("lat", "")

                # Format the values into the desired format
                self.bbox = f"{west}, {north}, {east}, {south}"
            else:
                try:
                    asBBox = [float(x) for x in self.bbox.split(",")]
                    if len(asBBox) != 4:
                        wasdi.wasdiLog("BBOX Not valid. Please use LATN,LONW,LATS,LONE")
                        wasdi.wasdiLog("BBOX received:" + self.bbox)
                        self.bbox = ""
                    else:
                        self.bbox = asBBox
                except ValueError as oEx:
                    wasdi.wasdiLog(f"BBox not valid. {repr(oEx)}. Computing one")
                    self.bbox = ""

        if self.width == "":
            self.set_size()
            wasdi.wasdiLog(f"Width is not present. Computing default one... {self.width}")

        if self.height == "":
            wasdi.wasdiLog(f"Height is not present. Computing default one... {self.height}")
            self.set_size()

    def create_web_map_service(self):
        """
        Create a WebMapService object
        :return: None or a WebMapService object
        """
        try:
            self.wms = WebMapService(self.geoserver_url, version='1.3.0')

        except Exception as oEx:
            wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
            wasdi.updateStatus("ERROR", 0)
            return None

    def get_bounding_box_list(self):
        """
        Calculate the best bbox if it is not present
        :return: list of coordinates and in the last element the crs option
        """

        try:
            if self.bbox == "":
                # Get the bounding box and the correspondent coordinate system
                to_bounding_box_list = self.wms[self.layer_id].boundingBox
                wasdi.wasdiLog(f"Finding the correct BBox... used {to_bounding_box_list} for {self.product}")
            else:
                # Using bbox provided by the user
                to_bounding_box_list = self.bbox
                to_bounding_box_list.append(self.crs)
            return to_bounding_box_list

        except Exception as ex:
            wasdi.wasdiLog(f'An error occurred: {repr(ex)}')
            wasdi.updateStatus("ERROR", 0)
            return None

    def set_size(self):
        """
        Set the sizes for the output image if the user didn't provide them
        :return: int size of the output image
        """

        bbox = self.get_bounding_box_list()
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        self.width = int(width * 100)
        self.height = int(height * 100)

    def create_query_wms(self, layers, styles, to_bounding_box_list):
        """
        Creates the query for retrieving a map from geoserver
        :param layers: list of layers
        :param styles: str name of the style file on WASDI
        :param to_bounding_box_list: list of bboxes
        :return:
        """

        # Create a query to the WMS
        parameters = {
            'service': 'WMS',
            'version': '1.3.0',
            'request': 'GetMap',
            'layers': layers,
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

        return parameters

    def get_map_request(self, params):
        """
        Compute a get map request
        :param params: query params
        :return: True if the request is successful, False otherwise
        """

        try:
            # Make the request and save the response as a file
            response = self.wms.getmap(**params)
            # Get the local base save path for a product
            folder_path = wasdi.getSavePath()

            # Construct the file path
            file_path = os.path.join(folder_path, f"{self.filename}.{self.format}")

            with open(file_path, "wb") as o:
                o.write(response.read())
                wasdi.wasdiLog('Map image saved successfully.')
                return True  # Return True to indicate success

        except requests.exceptions.ConnectionError:
            # Handle network errors
            wasdi.wasdiLog('Could not connect to the WMS server.')
            return False  # Return False to indicate failure
        except owslib.util.ServiceException as oEx:
            # Handle server errors
            wasdi.wasdiLog(f'The WMS server returned an error: {repr(oEx)}')
            return False  # Return False to indicate failure
        except Exception as oEx:
            # Handle any other error
            wasdi.wasdiLog(f'An unknown error occurred: {repr(oEx)}')
            wasdi.updateStatus("ERROR", 0)
            return False  # Return False to indicate failure

    def process_layer(self, b_stack_layers):
        """
        Process each layer
        :param b_stack_layers: bool if we are stacking layers or not (True) by default
        :return: Either calls the process_layers() or the get_map_request()
        """

        if self.wms is None:

            try:
                # try to connect to the provided Geoserver url
                if self.geoserver_url == "":
                    # Check if the band is the correct band
                    bands = wasdi.getProductBand(self.product)
                    if self.band not in bands:
                        self.band = bands[0]

                    # Starts a publish band process and wait for the result to be available
                    s_json_result = wasdi.getlayerWMS(self.product, self.band)
                    # Convert the string to a Python object
                    data = json.loads(s_json_result)
                    wasdi.wasdiLog(data)

                    # Define the base URL of the WMS server
                    self.geoserver_url = data["server"]
                    self.layer_id = f"wasdi:{data['layerId']}"

                self.create_web_map_service()
                self.validate_params()

            except Exception as ex:
                wasdi.wasdiLog(f'An error occurred: {repr(ex)}')
                wasdi.updateStatus("ERROR", 0)
                return None

            # Getting the bbox for each layer
            to_bounding_box_list = self.get_bounding_box_list()

            layers_to_stack = []

            if b_stack_layers:
                layers_to_stack.append([self])
                pass

            # Create the query and then get the map
            parameters = self.create_query_wms([self.layer_id], [self.style], to_bounding_box_list)
            # Return the result of get_map_request
            return self.get_map_request(parameters)

        return True  # Return True to indicate success

    def process_layers(self, layers, iBBoxOptions):
        """
        Stacking layers
        :param layers: list of layers to stack
        :param iBBoxOptions: which bbox we want to choose when stacking
        :return: calls a get_map_request()
        """

        wasdi.wasdiLog("You are now stacking layers!")
        to_bounding_box_list = []

        # Using the intersection of BBoxes
        if iBBoxOptions == 0:
            wasdi.wasdiLog("You are now using the intersection of the BBoxes.")
            bboxes = []

            for layer in layers:
                bboxes.append(layer.get_bounding_box_list())

            for i in range(len(bboxes)):
                for j in range(i + 1, len(bboxes)):
                    box1 = bboxes[i]
                    box2 = bboxes[j]

                    intersection_area = calculate_bbox_intersection(box1, box2)
                    wasdi.wasdiLog(f"Intersection area between box {i + 1} and box {j + 1}: {intersection_area}")

                    to_bounding_box_list = intersection_area

        # Using the union of BBoxes
        elif iBBoxOptions == 1:
            wasdi.wasdiLog("You are now using the union of the BBoxes.")
            bboxes = []

            for layer in layers:
                bboxes.append(layer.get_bounding_box_list())

            for i in range(len(bboxes)):
                for j in range(i + 1, len(bboxes)):
                    box1 = bboxes[i]
                    box2 = bboxes[j]

                    union_area = calculate_bbox_union(box1, box2)
                    wasdi.wasdiLog(f"Union area between box {i + 1} and box {j + 1}: {union_area}")

                    to_bounding_box_list = union_area

        else:
            to_bounding_box_list = self.get_bounding_box_list()

        self.bbox = to_bounding_box_list

        layer_ids = []
        styles = []
        for layer in layers:
            layer_ids.append(layer.layer_id)
            styles.append(layer.style)

        # Create a query to the WMS
        parameters = self.create_query_wms(layer_ids, styles, to_bounding_box_list[:4])
        return self.get_map_request(parameters)


def calculate_bbox_intersection(bbox1, bbox2):
    """
    Calculate the intersection of bboxes
    :param bbox1: bbox of the first layer
    :param bbox2: bbox of the second layer
    :return: intersection of bboxes
    """
    x1_min, y1_min, x1_max, y1_max, _ = bbox1
    x2_min, y2_min, x2_max, y2_max, _ = bbox2

    intersection_x_min = max(x1_min, x2_min)
    intersection_y_min = max(y1_min, y2_min)
    intersection_x_max = min(x1_max, x2_max)
    intersection_y_max = min(y1_max, y2_max)

    if intersection_x_max < intersection_x_min or intersection_y_max < intersection_y_min:
        return None  # No overlap

    intersection_bbox = (intersection_x_min, intersection_y_min, intersection_x_max, intersection_y_max)
    return intersection_bbox


def calculate_bbox_union(bbox1, bbox2):
    """
        Calculate the union of bboxes
        :param bbox1: bbox of the first layer
        :param bbox2: bbox of the second layer
        :return: union of bboxes
        """
    x1_min, y1_min, x1_max, y1_max, _ = bbox1
    x2_min, y2_min, x2_max, y2_max, _ = bbox2

    union_x_min = min(x1_min, x2_min)
    union_y_min = min(y1_min, y2_min)
    union_x_max = max(x1_max, x2_max)
    union_y_max = max(y1_max, y2_max)

    union_bbox = (union_x_min, union_y_min, union_x_max, union_y_max)
    return union_bbox
