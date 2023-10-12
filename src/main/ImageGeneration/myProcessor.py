import uuid

import wasdi
from PIL import Image, ImageDraw, ImageFont
from osgeo import gdal

from Layer import Layer
from generateBackgroundTile import generateBackground


def run():
    wasdi.wasdiLog("WMS client tutorial v.1.3")
    # Define the constant save path
    SAVE_PATH = wasdi.getSavePath()

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
    sImageText = wasdi.getParameter("text", "")

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
        sGeoServerUrl = oProduct.get("GEOSERVER URL", "")
        sLayerId = oProduct.get("LAYER ID", "")
        iStackOrder = oProduct["stack_order"]
        sFileName = wasdi.getParameter("FILENAME", "")

        asGetProducts = wasdi.getProductsByActiveWorkspace()

        if asGetProducts is not None:
            wasdi.wasdiLog("Found " + str(len(aoProducts)) + " products")

        if sProduct not in asGetProducts:
            wasdi.wasdiLog("The selected product is not in the workspace")
            continue

        count = 0
        # If the filename is not set generate a random one
        if sFileName == "":
            sFileName = str(uuid.uuid4())
            wasdi.wasdiLog(f"FileName is not set! Generating a random UUID one... {sFileName}")
        else:
            sFileName = f"{sFileName}_{count}"

        # Check stacking order validity
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

        # Track all the layers
        layers.append(layer)

        # Process each layer alone if I'm not stacking (True by default)
        for layer in layers:
            layer.process_layer(bStackLayers)

        count += 1

    # if there is no product in the workspace, then stop the processor
    if len(layers) == 0:
        wasdi.wasdiLog("[ERROR] no selected product in the workspace")
        return None

    if sOutputImageFormat.lower() == "gif":
        for layer in layers:
            gdal.Translate(f"{SAVE_PATH}{layer.filename}.png",
                           f"{SAVE_PATH}{layer.filename}.geotiff",
                           options=["-of", "png"])

    # If stacking layers
    if bStackLayers and len(layers) > 1:

        if valid:
            # Sort layers based on stack_order
            layers = sorted(layers, key=lambda x: x.stack)

        layers[0].process_layers(layers, iBBoxOptions)

    # Check background tile service
    if sBackgroundTileService != "" or sBackgroundTileService is not None:
        generateBackground(sBackgroundTileService, layers[0])

    if sOutputImageFormat.lower() == "gif":
        gdal.Translate(f"{SAVE_PATH}/mosaic.png",
                       f"{SAVE_PATH}/mosaic.tif",
                       options=["-of", "png"])

        frames = []

        # Determine the common dimensions for all frames
        common_width, common_height = None, None

        for layer in layers:
            img_path = f"{SAVE_PATH}{layer.filename}.png"
            img = Image.open(img_path)

            # Check if common dimensions are initialized
            if common_width is None and common_height is None:
                common_width, common_height = img.size

            # Resize the image if it has different dimensions
            if img.size != (common_width, common_height):
                img = img.resize((common_width, common_height))

            # Convert the image to RGB format if it has a different number of bands
            if img.mode != "RGB":
                img = img.convert("RGB")

            frames.append(img)

        # Open the mosaic image
        mosaic_path = f"{SAVE_PATH}/mosaic.png"
        mosaic_img = Image.open(mosaic_path)

        # Resize the mosaic image if it has different dimensions
        if mosaic_img.size != (common_width, common_height):
            mosaic_img = mosaic_img.resize((common_width, common_height))

        frames.append(mosaic_img)

        filepath = f"{SAVE_PATH}/my_animation.gif"

        # Set the duration for each frame in milliseconds (500 milliseconds = 0.5 seconds)
        frame_duration = 500

        # Create a new image with the same dimensions as the frames
        gif = Image.new("RGB", frames[0].size)

        # Create a list of frames with the specified duration
        gif_frames = []

        for frame in frames:
            gif_frames.append(frame.copy())

        # Save the GIF
        gif.save(filepath, save_all=True, append_images=gif_frames, duration=frame_duration, loop=0)
        sFileName = "my_animation"

    else:
        gdal.Translate(SAVE_PATH + sFileName + f"1.{sOutputImageFormat}",
                       f"{SAVE_PATH}/mosaic.tif",
                       options=["-of", sOutputImageFormat])
        sFileName += "1"

        # Load the image
        image = Image.open(SAVE_PATH + sFileName + f".{sOutputImageFormat}")

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        # Specify text, font, color, and position
        # On linux
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        # On windows
        # font = ImageFont.truetype("arial.ttf", 36)
        text_color = (255, 255, 255)
        position = (20, 20)

        # Draw the text on the image
        draw.text(position, sImageText, fill=text_color, font=font)

        # Save the modified image
        image.save(SAVE_PATH + sFileName + f".{sOutputImageFormat}")

    wasdi.addFileToWASDI(sFileName + f'.{sOutputImageFormat}')

    # Create the payload object
    aoPayload = {
        "inputs": wasdi.getParametersDict(),
        "output": sFileName
    }
    # Save the payload
    wasdi.setPayload(aoPayload)

    # Close the process setting the status to DONE
    wasdi.updateStatus("DONE", 100)


if __name__ == "__main__":
    wasdi.init('./config.json')
    run()
