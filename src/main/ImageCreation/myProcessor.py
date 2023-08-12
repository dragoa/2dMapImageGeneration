import uuid
import wasdi
from Layer import Layer


def run():
    wasdi.wasdiLog("WMS client tutorial v.1.3")

    # Reading the parameters
    aoProducts = wasdi.getParameter("products")
    bStackLayers = wasdi.getParameter("stackLayers")
    iBBoxOptions = wasdi.getParameter("bboxOptions")

    layers = []
    background_layer = None

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
        sFileName = oProduct["FILENAME"]
        bIsBackground = oProduct["isBackground"]

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

        # If the filename is not set generate a random one
        if sFileName == "":
            wasdi.wasdiLog("FileName is not set! Generating a random UUID one...")
            sFileName = uuid.uuid4()

        # Create the layer
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
            sLayerId,
            sFileName
        )

        if bIsBackground:
            background_layer = layer
            wasdi.wasdiLog(f"Background Layer: {background_layer.product}")
        else:
            layers.append(layer)

        # check for GeoServer url
        if sGeoServerUrl != "" and sLayerId != "":
            layer.geoserver_url = sGeoServerUrl
            layer.layer_id = sLayerId

        layers.append(layer)

        for layer in layers:
            layer.process_layer(bStackLayers)

    if bStackLayers:

        # If the background was not specified
        if background_layer is None:
            wasdi.wasdiLog("No background layer specified.")
            wasdi.wasdiLog("exit")
            wasdi.updateStatus("ERROR", 0)
            return None

        process_layers(background_layer, layers, iBBoxOptions)


def process_layers(background_layer, layers, iBBoxOptions):
    background_layer.process_layers(layers, iBBoxOptions)


if __name__ == "__main__":
    wasdi.init('./config.json')
    run()
