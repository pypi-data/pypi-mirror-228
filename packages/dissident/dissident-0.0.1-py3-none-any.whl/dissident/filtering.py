import os
import re
import mercantile
from shapely.geometry import box
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import compress


def dir_mapbox_file_reader(file_dir):
    """Generates a list of files from the Mapbox directory

    Args:
        file_dir (list): path to the directory with Mapbox Data

    Returns:
        list: list of absolute paths to Mapbox CSV files
    """
    # first walk the dir
    file_list = []

    # get the files
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_list.append(os.path.join(root, file))

    # only keep .csv and quadkey
    file_list = [i for i in file_list if ".csv" in i and "quadkey" in i]

    return file_list


def generate_quadkeys(poly, zoom):
    """Generate a list of quadkeys that overlap with a given polygon.

    Args:
        poly (shapely.geometry Polygon).
        zoom (integer): zoom level.

    Return:
        list: List of quadkeys as string
    """

    b = box(*poly.total_bounds)

    return [mercantile.quadkey(x) for x in mercantile.tiles(*b.bounds, zoom)]


def mbox_quadname_filter(file_list, gpd_path, buffer=None, pass_gdf=None):
    """Filters list with absolute paths based on intesercted geometries from geographic data supplied by either a path or in-memory geopandas object.
    Buffering the spatial object is optional.

    Args:
        file_list (list): list with Mapbox absolute paths generated via dir_mapbox_file_reader()
        gpd_path (str): path to geographic data (anything that can be read with gpd.read_file(...))
        buffer (int, optional): buffer radius to draw to collect the data. Defaults to None.
        pass_gdf (gpd.GeoDataFrame, optional): GeoDataFrame to use for subsetting. Defaults to None.

    Return:
        list: filtered list of absolute paths to Mapbox files.
    """

    if pass_gdf is not None:
        print("using supplied geodataframe")
        geodata = pass_gdf

    # read the file
    else:
        geodata = gpd.read_file(gpd_path)

    if geodata.crs != "epsg:4326":
        geodata = geodata.to_crs("epsg:4326")

    if buffer is not None:
        geodata = gpd.GeoDataFrame(
            data=geodata.drop("geometry", axis=1),
            geometry=geodata.geometry.buffer(buffer),
        )
        geodata = geodata.to_crs("epsg:3857")
        geodata = geodata.to_crs("epsg:4326")

    quads = generate_quadkeys(geodata, 7)
    print("quads length for filtering", len(quads))

    file_quads = [re.findall(r"/(\d+)\.csv", i)[0] for i in file_list]

    # create a dataframe with file quads and file list
    lst_for_df = [list(_) for _ in zip(file_quads, file_list)]

    df = pd.DataFrame(lst_for_df, columns=["quadkey", "pathname"])
    print("df.shape", df.shape)

    df = df.loc[df.quadkey.isin(quads)]

    new_file_list = df.pathname.to_list()

    return new_file_list


def tiles_to_geo(lst_w_files):
    """Creates a GeoDataFrame with Mapbox tile geometries

    Args:
        lst_w_files (list): list with absolute paths to Mapbox files

    Returns:
        gpd.GeoDataFrame: GeoDataFrame
    """

    lst_of_boxes = {}

    for i in list(set(file_quads)):
        # convert quadkey to tile: Tile(x=24, y=50, z=7)
        tt = mercantile.quadkey_to_tile(i)

        # create a mercantile box
        bb = mercantile.bounds(tt.x, tt.y, tt.z)

        # create a shapely box
        b = box(bb.west, bb.south, bb.east, bb.north)

        # store to dict
        lst_of_boxes[i] = b

    # convert dict to geopandas geodataframe for plotting
    gdf = gpd.GeoDataFrame(
        index=[_ for _ in lst_of_boxes.keys()],
        crs="epsg:4326",
        geometry=[_ for _ in lst_of_boxes.values()],
    )

    return gdf
