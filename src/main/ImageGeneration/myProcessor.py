import uuid
import wasdi
from osgeo import gdal

from Layer import Layer
from generateBackgroundTile import generateBackground


def run():
    wasdi.wasdiLog("WMS client tutorial v.1.3")

    # Reading the parameters
    aoProducts = wasdi.getParameter("products")
    iBBoxOptions = wasdi.getParameter("bboxOptions", 1)
    bStackLayers = wasdi.getParameter("stackLayers", True)
    sBackgroundTileService = wasdi.getParameter("backgroundService", "osm")
    sOutputImageFormat = wasdi.getParameter("outputFormat", "png")

    layers = []
    stack_orders = set()
    valid_range = range(1, len(aoProducts) + 1)
    valid = True

    for oProduct in aoProducts:
        # Read from params the bands we want to extract and the product
        sProduct = oProduct["PRODUCT"]
        sBand = oProduct.get("BAND", "band_1")
        sBBox = oProduct.get("BBOX")
        sCRS = oProduct.get("CRS")
        sWidth = oProduct.get("WIDTH")
        sHeight = oProduct.get("HEIGHT")
        sStyle = oProduct.get("STYLE", "")
        sFileName = oProduct.get("FILENAME", "")
        sGeoServerUrl = oProduct.get("GEOSERVER URL", "")
        sLayerId = oProduct.get("LAYER ID", "")
        iStackOrder = oProduct["stack_order"]

        # Check the Bounding Box: is needed
        if sBBox is not None:
            # Split the BBox: it is in the format: WEST, NORTH, EAST, SOUTH
            if isinstance(sBBox, dict):
                # Extract latitude and longitude values
                north = sBBox.get("northEast", {}).get("lat", "")
                west = sBBox.get("northEast", {}).get("lng", "")
                south = sBBox.get("southWest", {}).get("lat", "")
                east = sBBox.get("southWest", {}).get("lng", "")

                # Format the values into the desired format
                sBBox = f"{west}, {north}, {east}, {south}"
            else:
                asBBox = sBBox.split(",")
                if len(asBBox) != 4:
                    wasdi.wasdiLog("BBOX Not valid. Please use LATN,LONW,LATS,LONE")
                    wasdi.wasdiLog("BBOX received:" + sBBox)
                    sBBox = ""

        wasdi.wasdiLog(wasdi.getProductBBOX(sProduct))

        # Check the CRS: is needed
        if sCRS is None:
            wasdi.wasdiLog("CRS Parameter not set.")
            sCRS = "EPSG:4326"

        if sWidth is None:
            sWidth = 2900

        if sHeight is None:
            sHeight = 700

        # If the filename is not set generate a random one
        if sFileName == "":
            sFileName = uuid.uuid4()
            wasdi.wasdiLog(f"FileName is not set! Generating a random UUID one... {sFileName}")

        # Check on the stacking order
        if iStackOrder not in valid_range:
            valid = False
            wasdi.wasdiLog(f"Invalid stack order for the product: {sProduct}")
        elif iStackOrder in stack_orders:
            valid = False
            wasdi.wasdiLog(f"Duplicate stack order for : {sProduct}! Trying anyway...")
        else:
            stack_orders.add(iStackOrder)

        # Create the layer
        layer = Layer(
            sProduct,
            sBand,
            sBBox,
            sCRS,
            sWidth,
            sHeight,
            sStyle,
            sFileName,
            sGeoServerUrl,
            sLayerId,
            iStackOrder
        )

        # Tracking all the layers
        layers.append(layer)

        # Process each layer alone if I'm not stacking (True by default)
        for layer in layers:
            layer.process_layer(bStackLayers)

    if bStackLayers:

        if valid:
            # Sort layers based on stack_order
            layers = sorted(layers, key=lambda x: x.stack)

        layers[0].process_layers(layers, iBBoxOptions)

    # Check background tile service
    if sBackgroundTileService != "" or sBackgroundTileService is not None:
        generateBackground(sBackgroundTileService, layers[0])

    gdal.Translate(str(sFileName) + f'.{sOutputImageFormat}',
                   "mosaic.tif",
                   options=["-of", sOutputImageFormat])

    # Create the payload object
    aoPayload = {}
    # Save the inputs that we received
    aoPayload["inputs"] = wasdi.getParametersDict()
    # Save the output we created
    aoPayload["output"] = sFileName
    # Save the payload
    wasdi.setPayload(aoPayload)

    # Close the process setting the status to DONE
    wasdi.updateStatus("DONE", 100)


if __name__ == "__main__":
    wasdi.init('./config.json')
    run()
