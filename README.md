# ImageGeneration

ImageGeneration is a tool for retreiving layers present in a WASDI workspace in various different formats.
With this tool you are able to stack one or more layer over the other and to set a background map layer from using different providers.
As it is a WASDI processor it uses the WASDI library that can be found at <https://github.com/fadeoutsoftware/WASDI>

#### REQUIREMENTS AND INSTALLATION
__ImageGeneration__ depends on several packages, which should be installed automatically. The packages required for the
correct execution are the following:

* _wasdi_
* _gdal_
* _owslib_
* _geotiler_
* _uuid_

All the above packages are available via pip or conda. To install any of them, run the command:

```bash
pip install <name of the package>
```

To run some examples, further packages may be required. If an example requires a specific package, it will be detailed in the example directory.

### Documentation
The documentation related to the wasdi package can be found at <https://wasdi.readthedocs.io/en/latest/index.html>.

### Supported Inputs
To utilize the Image Generation as a WASDI processor, it is essential to have a WASDI account, as the application requires authentication. To set up the application, you must complete the configuration in the "config.json" file by providing your corresponding account credentials and the name of the workspace you are working on.
```bash
{
  "USER": "YOUR USERNAME",
  "PASSWORD": "YOUR PASSWORD",
  "PARAMETERSFILEPATH": "./params.json",
  "WORKSPACE": "WORKSPACE NAME"
}
```

ImageGeneration as a WASDI processor requires a _params.json_ file that contains all the parameters.
There are many parameters supported:
* A list of _products_ which represent each layer present in a WASDI workspace.
- Each layer has different options:

```bash
{
  "PRODUCT": "lulc_map.tif",
  "BAND": "band_1",
  "BBOX": "",
  "STYLE": "",
  "FILENAME": "",
  "GEOSERVER URL": "",
  "LAYER ID": "",
  "stack_order": 1
}
```
- _product_: Identifier for a product inside the WASDI workspace
- _band_: Identifier for the band of the product
- _bbox_: Bbox options used for selecting an area in the world
- _style_: Name of a sld style file present on a WASDI workspace
- _fileName_: Name of the output image
- _geoserver url_: Link for a custom geoserver url
- _layer id_: Identifier of a layer in a Geoserver workspace
- _stack order_: Order on which we want to stack layers

* A series of options for retreiving images:

```bash
"CRS": "",
"WIDTH": "",
"HEIGHT": 700,
"outputFormat": "jpeg",
"backgroundService" : "osm",
"stackLayers": true,
"bboxOptions": 1
```
- _crs_: Coordinate Reference System used. The list of crs options are the one supported by GeoServer
- _width_: Width of the image
- _height_: Height of the image
- _output format_: Format for the output image
- _background service_: Option for the tile provider
- _stack layers_: Boolean for selecting if stacking layers (true by default)
- _bbox options_: Integer for selecting the bbox options 

### File Format Options
The formats for the output images are the ones supported by GeoServer.

| Format     | Syntax                                  | Notes                                                                                          |
|------------|-----------------------------------------|------------------------------------------------------------------------------------------------|
| PNG        | `format=image/png`                      | Default PNG format for images.                                                                 |
| PNG8       | `format=image/png8`                     | Same as PNG, but with an optimal 256-color (8-bit) palette for smaller image sizes.          |
| JPEG       | `format=image/jpeg`                     | JPEG image format.                                                                              |
| JPEG-PNG   | `format=image/vnd.jpeg-png`             | A custom format that dynamically decides between JPEG and PNG compression based on image contents. Requires `&transparent=TRUE` parameter for meaningful use. |
| JPEG-PNG8  | `format=image/vnd.jpeg-png8`            | Similar to JPEG-PNG but generates a paletted output if PNG format is chosen.                   |
| GIF        | `format=image/gif`                      | GIF image format.                                                                              |
| TIFF       | `format=image/tiff`                     | TIFF image format.                                                                             |
| TIFF8      | `format=image/tiff8`                    | Similar to TIFF, but with an optimal 256-color (8-bit) palette for smaller image sizes.       |
| GeoTIFF    | `format=image/geotiff`                  | Similar to TIFF, but includes extra GeoTIFF metadata.                                           |
| GeoTIFF8   | `format=image/geotiff8`                 | Similar to GeoTIFF but with an optimal 256-color (8-bit) palette for smaller image sizes and extra GeoTIFF metadata. |
| SVG        | `format=image/svg`                      | SVG image format.                                                                              |
| PDF        | `format=application/pdf`                | PDF document format.                                                                           |
| GeoRSS     | `format=rss`                            | GeoRSS format.                                                                                 |
| KML        | `format=kml`                            | KML format, often used for geographic data in applications like Google Earth.                   |
| KMZ        | `format=kmz`                            | KMZ format, a compressed version of KML.                                                       |
| OpenLayers | `format=application/openlayers`          | Generates an OpenLayers HTML application, likely for displaying geospatial data.                |
| UTFGrid    | `format=application/json;type=utfgrid`  | Generates an UTFGrid 1.3 JSON response, typically for vector data output.                         |

For the bbox options you can choose between intersection, union, and then one of the bboxes of a specific product. 
| bboxOptions | Notes                                    |
|-------------|------------------------------------------|
| 0           | Using the intersection of BBoxes.       |
| 1           | Using the union of BBoxes.             |
| else        | Using the bbox of the base layer.      |

The parameter backgroundService is used to choose between the different tile providers supported by GeoTiler.
| Provider                    | Provider Id              | API Key Reference          | License                                |
|-----------------------------|--------------------------|----------------------------|----------------------------------------|
| OpenStreetMap               | osm                      |                            | [Open Data Commons Open Database License](https://www.openstreetmap.org/copyright) |
| Stamen Toner                | stamen-toner             |                            | [Creative Commons Attribution (CC BY 3.0) license](http://maps.stamen.com/) |
| Stamen Toner Lite           | stamen-toner-lite        |                            | as above                               |
| Stamen Terrain              | stamen-terrain           |                            | as above                               |
| Stamen Terrain Background   | stamen-terrain-background|                            | as above                               |
| Stamen Terrain Lines        | stamen-terrain-lines     |                            | as above                               |
| Stamen Water Color          | stamen-watercolor        |                            | as above                               |
| Modest Maps Blue Marble     | bluemarble               |                            | [NASA guideline](http://www.nasa.gov/audience/formedia/features/MP_Photo_Guidelines.html)                          |
| OpenCycleMap                | thunderforest-cycle      | thunderforest              | [Thunderforest Terms and Conditions](https://www.thunderforest.com/terms/)     |

N.B. A map provider might require API key. To add an API key for a map provider, the $HOME/.config/geotiler/geotiler.ini file has to be created with API key reference pointing to an API key, for example:

```bash
[api-key]
thunderforest = <api-key>
```
where <api-key> is usually a fixed size, alphanumeric hash value provided by map provider service.

For the full documentation of GeoTiler check https://wrobell.dcmod.org/geotiler/usage.html.