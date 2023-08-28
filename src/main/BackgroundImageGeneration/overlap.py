from osgeo import gdal


def overlap_geotiffs(input_tiff1, input_tiff2, output_tiff):
    # Open the input GeoTIFFs
    dataset1 = gdal.Open(input_tiff1, gdal.GA_ReadOnly)
    dataset2 = gdal.Open(input_tiff2, gdal.GA_ReadOnly)

    # Get the geotransforms and resolutions of the datasets
    geotransform1 = dataset1.GetGeoTransform()
    geotransform2 = dataset2.GetGeoTransform()
    x_res1 = geotransform1[1]
    y_res1 = geotransform1[5]
    x_res2 = geotransform2[1]
    y_res2 = geotransform2[5]

    # Calculate the new geotransform for the output image
    new_geotransform = (
        min(geotransform1[0], geotransform2[0]), max(x_res1, x_res2), 0,
        max(geotransform1[3], geotransform2[3]), 0, min(y_res1, y_res2)
    )

    # Create the output GeoTIFF
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(
        output_tiff, dataset1.RasterXSize, dataset1.RasterYSize, 3, gdal.GDT_Byte
    )
    output_dataset.SetGeoTransform(new_geotransform)

    # Read and write the overlapping content
    for i in range(1, 4):  # Assuming 3 bands (RGB)
        band1 = dataset1.GetRasterBand(i)
        band2 = dataset2.GetRasterBand(i)
        output_band = output_dataset.GetRasterBand(i)
        data1 = band1.ReadAsArray()
        data2 = band2.ReadAsArray()
        overlapped_data = data1 + data2  # You might want to perform more advanced blending
        output_band.WriteArray(overlapped_data)

    # Close datasets
    dataset1 = None
    dataset2 = None
    output_dataset = None


input_tiff1 = "temp/output.tif"
input_tiff2 = "6f011deb-34c4-4865-8eca-80448517187a.geotiff"
output_tiff = "output11.tif"

overlap_geotiffs(input_tiff1, input_tiff2, output_tiff)
