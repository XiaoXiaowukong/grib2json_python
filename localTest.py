# -*- coding:utf-8 -*-
from windjsonUtils import WindJsonUtil
from umOpener.openUtils import OpenUtils
import numpy as np
import time

np.set_printoptions(suppress=True)


def readnc():
    myOpenUtils_u = OpenUtils()
    myOpenUtils_u.initParams(
        "/Volumes/pioneer/gdal_Demo/cldas_/NAFP_CLDAS2.0_RT_GRB_WIU10_20181128-18.nc",
        file_type="nc",
        out_file="./tif2tif.tif",
        export_type="GeoTiff",
        data_type='float32',
        lat_order="asc",
        values_strs=["lats", "lons", "abc"],
        nc_values=["LAT", "LON", "WIU10"],
        is_rewirte_data=False,
        proj="mercator")
    myOpenUtils_v = OpenUtils()
    myOpenUtils_v.initParams(
        "/Volumes/pioneer/gdal_Demo/cldas_/NAFP_CLDAS2.0_RT_GRB_WIV10_20181128-18.nc",
        file_type="nc",
        out_file="./tif2tif.tif",
        export_type="GeoTiff",
        data_type='float32',
        lat_order="asc",
        values_strs=["lats", "lons", "abc"],
        nc_values=["LAT", "LON", "WIV10"],
        is_rewirte_data=False,
        proj="mercator")
    return (myOpenUtils_u.lats, myOpenUtils_u.lons, myOpenUtils_u.data, myOpenUtils_v.lats, myOpenUtils_v.lons,
            myOpenUtils_v.data)


if __name__ == '__main__':
    starttime = time.time()
    u_lat, u_lon, u_data, v_lat, v_lon, v_data = readnc()
    print u_data.shape
    print v_data.shape
    myWindJsonUtil = WindJsonUtil()
    myWindJsonUtil.initParams(u_lat, u_lon, u_data, v_lat, v_lon, v_data, export_file="./wind.json")

    print "end time %s" % str(time.time() - starttime)
