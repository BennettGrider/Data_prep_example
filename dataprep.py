import numpy as np
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import rasterio
import fiona

from tkinter import *
from tkinter import filedialog

import pprint
import pytest


"""
STEPS:
Open survey area shapefile
Open basedata raster datasets
Open basedata vector datasets
Buffer survey area shapefile
Clip raster datasets to buffered survey area
Possibly reclassify a raster dataset, vectorize?
Clip vector datasets to buffered survey area (keep the entirety of a road feature 
 up to 1[or user input] miles away)
"""



def user_select_file(file_type):
    """Allows the user to select a file location. Provides vector and raster options."""
    if file_type == "vector":
        ft = ("Shapefile", "*.shp")
    elif file_type == "raster":
        ft = ("TIFF", "*.tif")
    root = Tk().withdraw() # .withdraw() used to keep the blank main window from displaying as well
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(ft, ("all files", "*.*")))
    return root.filename


def open_vector_dataset(feature_list, file):
    """Uses fiona to open a shapefile dataset, appending all vector features to the "features" list input.
    feature_list is a list that will store the shapefile information, and file is the file directory."""

    # Making sure the inputs are valid
    if type(feature_list) is not list:
        raise TypeError('The input variable storing features must be a list.')
    if type(file) is not str:
        raise TypeError('The path input must be a string of the dataset filepath.')
    if file[-4:] != '.shp':
        raise ValueError('The input vector dataset must be a shapefile.')

    # Opening the shapefile and appending each feature to the aggregate list
    with fiona.open(file, 'r') as fh:
        for feat in fh:
            feature_list.append(feat)

    return feature_list


def open_raster_dataset(file, band_number=1):
    """Uses rasterio to open a raster dataset, where file is the directory of the raster file and band_number is
    the desired band to be read (defaults to the first band)."""
    # TODO: finish writing this!
    with rasterio.open(file) as dataset:
        print(f'{dataset.name}, {dataset.mode}, {dataset.width}, {dataset.height}, {dataset.crs}')
        print(f'Opening raster file at {file}')
        extracted_crs = dataset.crs.to_dict()['init']
        print(f'Shape: {dataset.shape}, CRS: {extracted_crs}, Bands: {dataset.indexes}')

        array = dataset.read(band_number)

    return array


# Not strictly necessary for this example, but used to create the test survey dataset and for future use
def create_new_shapefile(fields, epsg_crs_code, filename = 'New_Shapefile', feature_type = 'point'):
    """Provided a file directory/name, a tuple of field attributes in the format (type, name), and optionally a list(?)
    of features to add to the shapefile, creates a brand new shapefile."""
    driver = ogr.GetDriverByName("ESRI Shapefile") # Set up driver
    data_source = driver.CreateDataSource(filename + '.shp') # Create data source
    srs = osr.SpatialReference() # Create spatial reference
    srs.ImportFromEPSG(epsg_crs_code) # The epsg code must be the number portion of the code only!
    if feature_type.lower() == 'point':
        feat_type = ogr.wkbPoint
    elif feature_type.lower() == 'line':
        feat_type = ogr.wkbLineString
    elif feature_type.lower() == 'polygon':
        feat_type = ogr.wkbPolygon
    layer = data_source.CreateLayer(filename, srs, feat_type) # Creating layer, defaults to point type

    # Adding fields
    for field in fields:
        if field[0] == 'field_int':
            layer.CreateField(ogr.FieldDefn(field[1], ogr.OFTInteger))
        elif field[0] == 'field_float':
            layer.CreateField(ogr.FieldDefn(field[1], ogr.OFTReal))
        elif field[0] == 'field_str':
            field_name = ogr.FieldDefn(field[1], ogr.OFTString)
            field_name.SetWidth(24)
            layer.CreateField(field_name)

    # For checking to make sure that the attributes actually got properly added to the layer
    schema = []
    # ldef = layer.GetLayerDefn()
    # for n in range(ldef.GetFieldCount()):
    #     fdef = ldef.GetFieldDefn(n)
    #     schema.append(fdef.name)
    # print(schema)

    data_source = None # Saving and closing the data source





def smart_clip_roads(clip_vector, roads, buffer = 0.5, max_road_extension = 1):
    """Takes two data inputs, a list of vector data (survey data or anything else) and a roads vector data list,
    and creates a smart buffer around the survey data. The roads vector data is clipped to a buffer of the survey
    data, but road features are preserved if they connect to a different road within a maximum extension distance."""
    # TODO: write all this as well!





if __name__ == '__main__':



    # Opening the survey area dataset
    #survey_area = []
    #open_vector_dataset(survey_area, 'data/surveyarea.shp')


    # Opening the vector basedata
    #roads = [] # List to contain all vector features from the survey area shapefile
    #open_vector_dataset(roads, user_select_file("vector")) # 'data/tl_2015_27_prisecroads.shp'

    testRast = open_raster_dataset('data/n44_w094_1arc_v3.tif')

    shapefile = "data/tl_2015_27_prisecroads.shp"
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shapefile, 0) # 0 specifies that data can't be written to, a 1 would mean it can be written to
    layer = dataSource.GetLayer()

    testFields = [('field_float', 'Latitude'), ('field_float', 'Longitude'),
                  ('field_int', 'Number'), ('field_str', 'Notes')]
    create_new_shapefile(testFields, 4326, filename='data/test_empty_shapefile', feature_type='line')










