# -*- coding:utf-8 -*-
from windjsonUtils import WindJsonUtil
import time
from mpl_toolkits.basemap import *

np.set_printoptions(suppress=True)
import os

if __name__ == '__main__':
    starttime = time.time()
    uvdir = "/Volumes/pioneer/gdal_Demo/uv/"
    uvlist = os.listdir(uvdir)
    myWindJsonUtil = WindJsonUtil()
    for uvfile in uvlist:
        u_file = os.path.join(uvdir, uvfile)
        v_file = os.path.join(uvdir, uvfile.replace("WIU", "WIV"))
        if (os.path.exists(u_file) and os.path.exists(v_file)):
            jsonName = os.path.splitext(u_file)[0].replace("WIU", "WIUV")
            myWindJsonUtil.initParams(input_u_file=u_file,
                                      input_v_file=v_file,
                                      grid_width ="120",
                                      grid_height="120",
                                      input_data_type="nc",
                                      input_nodata="9999.0",
                                      export_file="%s.json" % jsonName)
        break

print "end time %s" % str(time.time() - starttime)
