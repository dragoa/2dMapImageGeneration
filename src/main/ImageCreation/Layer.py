import json
import os

import owslib.util
import requests
import requests.exceptions
import wasdi
# Import the WebMapService class from owslib.wms
from owslib.wms import WebMapService


def calculate_bbox_intersection(bbox1, bbox2):
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


def calculate_bbox_union(box1, box2):
    x1_min, y1_min, x1_max, y1_max, _ = box1
    x2_min, y2_min, x2_max, y2_max, _ = box2

    union_x_min = min(x1_min, x2_min)
    union_y_min = min(y1_min, y2_min)
    union_x_max = max(x1_max, x2_max)
    union_y_max = max(y1_max, y2_max)

    union_bbox = (union_x_min, union_y_min, union_x_max, union_y_max)
    return union_bbox


class Layer:
    def __init__(self, product, band, bbox, crs, width, height, img_format, style, sFileName,
                 geoserver_url, layer_id, iStackOrder):
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
        self.filename = sFileName
        self.stack = iStackOrder

    def create_web_map_service(self):

        try:
            self.wms = WebMapService(self.geoserver_url, version='1.3.0')

        except Exception as oEx:
            wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
            wasdi.updateStatus("ERROR", 0)
            return None

    def get_bounding_box_list(self):

        try:
            if self.bbox == "":
                # Get the bounding box and the correspondent coordinate system
                to_bounding_box_list = self.wms[self.layer_id].boundingBox
                wasdi.wasdiLog(f"Finding the correct BBox... used {to_bounding_box_list} for {self.product}")
            else:
                # Using bbox provided by the user
                to_bounding_box_list = [float(x) for x in self.bbox.split(",")]
                to_bounding_box_list.append(self.crs)
            return to_bounding_box_list

        except Exception as ex:
            wasdi.wasdiLog(f'An error occurred: {repr(ex)}')
            wasdi.updateStatus("ERROR", 0)
            return None

    def create_query_wms(self, layers, styles, to_bounding_box_list):

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

        try:
            # Construct the GetMap request URL
            # url_params = "&".join([f"{key}={value}" for key, value in params.items()])
            # getmap_url = f"{self.geoserver_url}?{url_params}"
            # print(getmap_url)

            # Make the request and save the response as a file
            response = self.wms.getmap(**params)
            # Get the local base save path for a product
            folder_path = wasdi.getSavePath()

            # # Create the folder if it doesn't exist
            # if not os.path.exists(folder_path):
            #     os.makedirs(folder_path)

            # Construct the file path
            file_path = os.path.join(folder_path, f"{self.filename}.{self.format}")

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

            try:
                # try to connect to the provided Geoserver url
                if self.geoserver_url == "":
                    # Starts a publish band process and wait for the result to be available
                    s_json_result = wasdi.getlayerWMS(self.product, self.band)
                    # Convert the string to a Python object
                    data = json.loads(s_json_result)
                    wasdi.wasdiLog(data)

                    # Define the base URL of the WMS server
                    self.geoserver_url = data["server"]
                    self.layer_id = f"wasdi:{data['layerId']}"

                self.create_web_map_service()

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
            else:
                # Create the query and then get the map
                parameters = self.create_query_wms([self.layer_id], [self.style], to_bounding_box_list)
                self.get_map_request(parameters)

    def process_layers(self, layers, iBBoxOptions):

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

        layer_ids = []
        styles = []
        for layer in layers:
            layer_ids.append(layer.layer_id)
            styles.append(layer.oStyle)

        # Create a query to the WMS
        parameters = self.create_query_wms(layer_ids, styles, to_bounding_box_list[:4])
        self.get_map_request(parameters)
