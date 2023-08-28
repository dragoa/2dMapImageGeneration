import uuid
import wasdi
from Layer import Layer


def run():
    wasdi.wasdiLog("WMS client tutorial v.1.3")

    # Reading the parameters
    aoProducts = wasdi.getParameter("products")
    iBBoxOptions = wasdi.getParameter("bboxOptions")
    bStackLayers = wasdi.getParameter("stackLayers")

    layers = []
    stack_orders = set()
    valid_range = range(1, len(aoProducts) + 1)
    valid = True

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
        sFileName = oProduct["FILENAME"]
        sGeoServerUrl = oProduct["GEOSERVER URL"]
        sLayerId = oProduct["LAYER ID"]
        iStackOrder = oProduct["stack_order"]

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
            sFormat,
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
