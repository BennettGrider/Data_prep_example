import numpy as np
from osgeo import gdal
import rasterio
import fiona

from tkinter import *
from tkinter import filedialog

import pprint
import pytest


'''
STEPS:
Open survey area shapefile
Open basedata raster datasets
Open basedata vector datasets
Buffer survey area shapefile
Clip raster datasets to buffered survey area
Possibly reclassify a raster dataset, vectorize?
Clip vector datasets to buffered survey area (keep the entirety of a road feature 
 up to 1[or user input] miles away)
'''


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
    """Uses fiona to open a shapefile dataset, appending all vector features to the "features" list input"""

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





if __name__ == '__main__':



    # Opening the survey area dataset
    #survey_area = []
    #open_vector_dataset(survey_area, 'data/surveyarea.shp')


    # Opening the vector basedata
    roads = [] # List to contain all vector features from the survey area shapefile
    open_vector_dataset(roads, user_select_file("vector")) # 'data/tl_2015_27_prisecroads.shp'








