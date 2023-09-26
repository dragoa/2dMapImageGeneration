import uuid
import wasdi
from osgeo import gdal

from Layer import Layer
from generateBackgroundTile import generateBackground


def run():
    wasdi.wasdiLog("WMS client tutorial v.1.3")

    # Reading the parameters
    aoProducts = wasdi.getParameter("products")
    if len(aoProducts) == 0:
        wasdi.wasdiLog("No product selected in the workspace.")
        wasdi.wasdiLog("exit")
        wasdi.updateStatus("ERROR", 0)
        return None

    sCRS = wasdi.getParameter("CRS", "EPSG:4326")
    sWidth = wasdi.getParameter("WIDTH", "")
    sHeight = wasdi.getParameter("HEIGHT", "")

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
        sBand = oProduct.get("BAND")
        sBBox = oProduct.get("BBOX")
        sStyle = oProduct.get("STYLE", "")
        sFileName = oProduct.get("FILENAME", "")
        sGeoServerUrl = oProduct.get("GEOSERVER URL", "")
        sLayerId = oProduct.get("LAYER ID", "")
        iStackOrder = oProduct["stack_order"]

        asGetProducts = wasdi.getProductsByActiveWorkspace()

        if asGetProducts is not None:
            wasdi.wasdiLog("Found " + str(len(aoProducts)) + " products")

        # TODO check
        if oProduct not in asGetProducts:
            wasdi.wasdiLog("About to execute SNAP workflow")
            sWorkFlow = "snap_workflow_name"
            wasdi.executeWorkflow([aoProducts[len(aoProducts) - 1]], [oProduct], sWorkFlow)
        else:
            wasdi.wasdiLog("File exists, no need to run workflow")

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

    gdal.Translate(wasdi.getSavePath()+str(sFileName) + f'.{sOutputImageFormat}',
                   wasdi.getSavePath()+"/mosaic.tif",
                   options=["-of", sOutputImageFormat])

    wasdi.addFileToWASDI(str(sFileName) + f'.{sOutputImageFormat}')

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
