import json

import owslib.util
import requests
import requests.exceptions
import wasdi
# Import the WebMapService class from owslib.wms
from owslib.wms import WebMapService


def run():
    wasdi.wasdiLog("WMS client tutorial v.1.0")
    # WMS Client
    global wms
    wms = ""
    # Read from the parameters each product that we want to extract
    aoProducts = wasdi.getParameter("products")

    try:
        for oProduct in aoProducts:
            # Read from params the bands we want to extract and the product
            sProduct = oProduct["PRODUCT"]
            sBand = oProduct["BAND"]
            sBBox = oProduct["BBOX"]
            sCRS = oProduct["CRS"]
            sWidthOfImage = oProduct["WIDTH"]
            sHeightOfImage = oProduct["HEIGHT"]
            sFormatOfImage = str.casefold(oProduct["FORMAT"])
            sStyleOfImage = oProduct["STYLE"]
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
                    return

            # Check the CRS: is needed
            if sCRS == "":
                wasdi.wasdiLog("CRS Parameter not set.")

            # If I already have a GeoServer URL
            if sGeoServerUrl != "":
                wms = createWebMapService(sGeoServerUrl)
                layer_names = ['ne:countries', 'ne:populated_places']
                parameters = {
                    'service': 'WMS',
                    'version': '1.3.0',
                    'request': 'GetMap',
                    'layers': [','.join(layer_names)],  # Combine layer names with commas
                    'styles': '',
                    'bbox': (-180, -90, 180, 90),
                    'size': (800, 600),
                    'srs': 'EPSG:4326',
                    'format': 'image/png'
                }

                getMapRequest(wms, parameters, "png", sGeoServerUrl)

            # Get all the products in the WASDI workspace
            asGetProducts = wasdi.getProductsByActiveWorkspace()
            if sProduct not in asGetProducts:
                wasdi.wasdiLog("An error occurred: The selected product is not in the workspace.")
                wasdi.updateStatus("ERROR", 0)
                return

            try:
                sJsonResult = wasdi.getlayerWMS(sProduct, sBand)
                # Convert the string to a Python object
                data = json.loads(sJsonResult)
                print(data)

                # Define the base URL of the WMS server
                sGeoServerUrl = data["server"]
                sLayerId = f"wasdi:{data['layerId']}"

                wms = createWebMapService(sGeoServerUrl)
            except Exception as oEx:
                # handle any error
                wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
                wasdi.updateStatus("ERROR", 0)
                return

            if sBBox == "":
                # get the bounding box and the correspondent coordinate system
                toBoundingBoxList = wms[sLayerId].boundingBox
                wasdi.wasdiLog(f"The Bounding Box used is {toBoundingBoxList}")
            else:
                toBoundingBoxList = [float(x) for x in sBBox.split(",")]
                toBoundingBoxList.append(sCRS)

            # layer_names = ['wasdi:a6c50075-7723-4a6c-9994-1cbff25cea08', sLayerId]
            layer_names = [sLayerId]

            parameters = {
                'service': 'WMS',
                'version': '1.3.0',
                'request': 'GetMap',
                "layers": [','.join(layer_names)],
                "styles": [sStyleOfImage],
                'srs': 'EPSG:4326',
                'bbox': (toBoundingBoxList[:4]),
                'size': (sWidthOfImage, sHeightOfImage),
                'format': f'image/{sFormatOfImage}',
                'transparent': True,
                'product': sProduct
            }
            # createLayerGroup()
            getMapRequest(wms, parameters, sFormatOfImage, sGeoServerUrl)
    except Exception as oEx:
        wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
        wasdi.updateStatus("ERROR", 0)
        return


def createWebMapService(sGeoserverUrl):
    try:
        wms = WebMapService(sGeoserverUrl, version='1.3.0')
        return wms
    except Exception as oEx:
        wasdi.wasdiLog(f'An error occurred: {repr(oEx)}')
        wasdi.updateStatus("ERROR", 0)
        return


def getMapRequest(wms, params, sFormatOfImage, sGeoserverUrl):
    # response = requests.get(f'{sGeoserverUrl}wms', params=params)
    #
    # if response.status_code == 200:
    #     with open('map.png', 'wb') as f:
    #         f.write(response.content)
    #     print('Map image saved successfully.')
    # else:
    #     print(f'Failed to retrieve map. Status code: {response.status_code}')

    # try to get the map image
    try:
        # make the request and save the response as a file
        response = wms.getmap(**params)
        with open(f"""{params['product']}.{sFormatOfImage}""", "wb") as o:
            o.write(response.read())
            wasdi.wasdiLog('Map image saved successfully.')
            # wasdi.addFileToWASDI("map.tiff", "")
    except requests.exceptions.ConnectionError:
        # handle network errors
        wasdi.wasdiLog('Could not connect to the WMS server.')
    except owslib.util.ServiceException as oEx:
        # handle server errors
        wasdi.wasdiLog(f'The WMS server returned an error: {repr(oEx)}')
    except Exception as oEx:
        # handle any other error
        wasdi.wasdiLog(f'An unknown error occurred: {repr(oEx)}')
        wasdi.updateStatus("ERROR", 0)
        return


def createLayerGroup():
    base_url = 'http://localhost:8080/geoserver/'
    username = 'admin'
    password = 'geoserver'

    layer_group_name = 'my_layer_group1'
    layer_names = ['ne:countries', 'ne:populated_places']  # Replace with actual layer names
    workspace = 'ne'  # Replace with the actual workspace name

    layer_group = {
        'name': layer_group_name,
        'workspace': workspace,
        'layers': {
            'layer': layer_names
        }
    }
    payload = json.dumps({'layerGroup': layer_group})

    url = f'{base_url}rest/workspaces/{workspace}/layergroups'

    response = requests.post(url, data=payload, auth=(username, password), headers={'Content-Type': 'application/json'})

    if response.status_code == 201:
        print('Layer group created successfully.')
    else:
        print(f'Failed to create layer group. Status code: {response.status_code}')
        print(response.text)


if __name__ == '__main__':
    wasdi.init('./config.json')
    run()
