# -*- coding:utf-8 -*-
from windjsonUtils import WindJsonUtil
from umOpener.openUtils import OpenUtils
import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import *

np.set_printoptions(suppress=True)
import os


def readnc(u_file, v_file):
    myOpenUtils_u = OpenUtils()
    myOpenUtils_u.initParams(
        u_file,
        file_type="nc",
        data_type='float',
        nc_values="LAT,LON,WIU10",
        is_rewirte_data=False,
        proj="mercator")
    myOpenUtils_v = OpenUtils()
    myOpenUtils_v.initParams(
        v_file,
        file_type="nc",
        data_type='float',
        nc_values="LAT,LON,WIV10",
        is_rewirte_data=False,
        proj="mercator")
    return (myOpenUtils_u.lats, myOpenUtils_u.lons, myOpenUtils_u.data[0], myOpenUtils_v.lats, myOpenUtils_v.lons,
            myOpenUtils_v.data[0])


if __name__ == '__main__':
    starttime = time.time()
    uvdir = "/Volumes/pioneer/gdal_Demo/uv/"
    uvlist = os.listdir(uvdir)
    u_files = []
    v_files = []
    myWindJsonUtil = WindJsonUtil()
    # uvlist = ["NAFP_CLDAS2.0_RT_GRB_WIU10_20181128-11.nc"]
    for uvfile in uvlist:
        u_file = os.path.join(uvdir, uvfile)
        v_file = os.path.join(uvdir, uvfile.replace("WIU", "WIV"))
        if (os.path.exists(u_file) and os.path.exists(v_file)):
            jsonName = os.path.splitext(u_file)[0].replace("WIU", "WIUV")

            u_lat, u_lon, u_data, v_lat, v_lon, v_data = readnc(u_file, v_file)
            print jsonName
            myWindJsonUtil.initParams(u_lat, u_lon, u_data, v_lat, v_lon, v_data,
                                      export_file="%s.json" % jsonName)
        break

print "end time %s" % str(time.time() - starttime)
