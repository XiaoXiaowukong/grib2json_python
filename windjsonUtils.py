# -*- coding:utf-8 -*-
__version__ = '$Id: windjsonUtils.py 27349 2018-11-29 18:58:51Z rouault $'
import numpy as np
import os
import json
from osgeo import gdal, ogr
from umOpener.openUtils import OpenUtils
import time


class WindJsonUtil():
    def __init__(self):
        print "__init__"

    # 初始化
    def initParams(self, u_lat, u_lon, u_data, v_lat, v_lon, v_data, **kwgs):
        print kwgs
        self.stopped = False
        self.optparse_init()
        self.u_lat = u_lat
        self.u_lon = u_lon
        self.u_data = u_data
        self.v_lat = v_lat
        self.v_lon = v_lon
        self.v_data = v_data
        print self.u_lat.shape
        print self.u_lon.shape
        print self.u_data.shape
        self.grid_width = 120
        self.grid_height = 120
        arguments = []
        for kwarg_key in kwgs.keys():
            arguments.append("--%s" % kwarg_key)
            arguments.append(kwgs[kwarg_key])
        (self.options, self.args) = self.parser.parse_args(args=arguments)
        self.mid_file = os.path.splitext(self.options.exportFile)[0]
        self.u_mid_file = '%s_u.tif' % self.mid_file
        self.v_mid_file = '%s_v.tif' % self.mid_file
        print self.options
        self.process()

    # 解析参数
    def optparse_init(self):
        """Prepare the option parser for input (argv)"""
        from optparse import OptionParser, OptionGroup
        usage = 'Usage: %prog [options] input_file(s) [output]'
        p = OptionParser(usage, version='%prog ' + __version__)
        p.add_option(
            '-e',
            '--export_file',
            dest='exportFile',
            help='export file',
        )
        p.set_defaults(
            latOrder="asc",
            dataOrder="asc",
            nodata=None,
            cmp="jet",
            isOpenColorBar=False,
            axis="off",
            dpi=80,  # 标准分辨率
        )
        self.parser = p

    # ==================================================================================================

    def process(self):
        print "开始的最大值", np.max(self.u_data)
        print "开始的最小值", np.min(self.u_data)
        startTime = time.time()
        self.makePolygon()
        makepolygonTime = time.time() - startTime
        print "makepolygonTime", makepolygonTime
        startTime = time.time()
        self.gdal_grid()
        gdalGridTime = time.time() - startTime
        print "gdalGridTime", gdalGridTime
        startTime = time.time()
        self.makeUVjson()
        makeuvTime = time.time() - startTime
        print "makeuvTime", makeuvTime

    # ==================================================================================================
    def stop(self):
        self.stopped = True

    def makePolygon(self):
        lat_maxSize = self.u_lat.__len__()
        lon_maxSize = self.u_lon.__len__()
        print "lat_maxSize", lat_maxSize
        print "lon_maxSize", lon_maxSize
        u_Wkt = 'POLYGON (('
        v_Wkt = 'POLYGON (('
        for index_lat, lat in enumerate(self.u_lat):
            for index_lon, lon in enumerate(self.u_lon):
                u_Wkt = u_Wkt + "%s %s %s" % (lon, lat, self.u_data[index_lon, index_lat])
                v_Wkt = v_Wkt + "%s %s %s" % (lon, lat, self.v_data[index_lon, index_lat])

                if (index_lat + 1 == lat_maxSize and index_lon + 1 == lon_maxSize):
                    u_Wkt = u_Wkt + "))"
                    v_Wkt = v_Wkt + "))"
                else:
                    u_Wkt = u_Wkt + ","
                    v_Wkt = v_Wkt + ","
        self.u_Wkt = u_Wkt
        self.v_Wkt = v_Wkt

    def gdal_grid(self):
        u_polygon = ogr.CreateGeometryFromWkt(self.u_Wkt)
        v_polygon = ogr.CreateGeometryFromWkt(self.v_Wkt)
        print [np.min(self.u_lon), np.min(self.u_lat), np.max(self.u_lon), np.max(self.u_lat)]
        print [np.min(self.u_lon), np.min(self.u_lat), np.max(self.u_lon), np.max(self.u_lat)]
        ds_u = gdal.Grid("", u_polygon.ExportToJson(), \
                         width=self.grid_width, height=self.grid_height, outputType=gdal.GDT_Float32,
                         outputSRS='EPSG:4326',
                         outputBounds=[np.min(self.u_lon), np.min(self.u_lat), np.max(self.u_lon), np.max(self.u_lat)], \
                         format='MEM', algorithm='nearest', noData=9999.0)
        cols_u = ds_u.RasterXSize  # 获取文件的列数
        rows_u = ds_u.RasterYSize  # 获取文件的行数
        currentBand_u = ds_u.GetRasterBand(1)
        current_data_u = currentBand_u.ReadAsArray(0, 0, cols_u, rows_u)
        current_geotransf_u = ds_u.GetGeoTransform()  # 获取放射矩阵
        (current_lat_u, current_lon_u) = self.createXY(current_geotransf_u, cols_u, rows_u)
        self.u_lon = current_lon_u
        self.u_lat = current_lat_u
        self.u_data = current_data_u[::-1]
        del ds_u
        # ===============================
        ds_v = gdal.Grid("", v_polygon.ExportToJson(), \
                         width=self.grid_width, height=self.grid_height, outputType=gdal.GDT_Float32,
                         outputSRS='EPSG:4326',
                         outputBounds=[np.min(self.u_lon), np.min(self.u_lat), np.max(self.u_lon), np.max(self.u_lat)], \
                         format='MEM', algorithm='nearest', noData=9999.0)
        cols_v = ds_v.RasterXSize  # 获取文件的列数
        rows_v = ds_v.RasterYSize  # 获取文件的行数
        currentBand_v = ds_v.GetRasterBand(1)
        current_data_v = currentBand_v.ReadAsArray(0, 0, cols_v, rows_v)
        current_geotransf_v = ds_v.GetGeoTransform()  # 获取放射矩阵
        (current_lat_v, current_lon_v) = self.createXY(current_geotransf_v, cols_v, rows_v)
        self.v_lon = current_lon_v
        self.v_lat = current_lat_v
        self.v_data = current_data_v[::-1]
        del ds_v

    def createXY(self, transform, xSize, ySize):
        lat = np.linspace(transform[5] * ySize + transform[3], transform[3], ySize)
        lon = np.linspace(transform[0], transform[1] * xSize + transform[0], xSize)
        lat = list(lat)
        lat.reverse()
        lat = np.asarray(lat)
        return (lat, lon)

    def read_mid_data(self):
        myOpenUtils = OpenUtils()
        myOpenUtils.initParams(
            self.u_mid_file,
            file_type="GeoTiff",
            data_type='float',
            is_rewirte_data=False,
            proj="mercator")
        self.u_lon = myOpenUtils.lons
        self.u_lat = myOpenUtils.lats
        self.u_data = myOpenUtils.data
        print self.u_data
        print max(self.u_lon), min(self.u_lon)
        print max(self.u_lat), min(self.u_lat)
        myOpenUtils.initParams(
            self.v_mid_file,
            file_type="GeoTiff",
            data_type='float',
            is_rewirte_data=False,
            proj="mercator")
        self.v_lon = myOpenUtils.lons
        self.v_lat = myOpenUtils.lats
        self.v_data = myOpenUtils.data

        print max(self.v_lon), min(self.v_lon)
        print max(self.v_lat), min(self.v_lat)

    def makeUVjson(self):
        dx = float((max(self.u_lon) - min(self.u_lon)) / self.grid_width)
        dy = float((max(self.u_lat) - min(self.u_lat)) / self.grid_height)

        # U=================================================
        u_windJson = {}
        u_header = {}
        u_header["nx"] = int(self.u_data.shape[0])
        u_header["ny"] = int(self.u_data.shape[1])
        u_header["lo1"] = float(min(self.u_lon))
        u_header["lo2"] = float(max(self.u_lon))
        u_header["la1"] = float(max(self.u_lat))
        u_header["la2"] = float(min(self.u_lat))
        u_header["dx"] = dx
        u_header["dy"] = dy
        u_header["gridUnits"] = "degrees"

        u_header["parameterNumberName"] = "U-component_of_wind"
        u_header["parameterUnit"] = "m.s-1"
        u_header["parameterCategory"] = 2
        u_header["parameterNumber"] = 2
        u_header["numberPoints"] = u_header["nx"] * u_header["ny"]
        u_header["meta"] = {"date": "2014-11-30T12:00:00.000Z"}
        u_header["gridDefinitionTemplateName"] = "Latitude_Longitude"
        u_header["surface2Type"] = 255

        print min(self.u_lon)
        print max(self.u_lon)
        u_windJson["header"] = u_header
        u_wind_data = self.u_data.flatten()
        u_wind_data_list = []
        for u_data in u_wind_data:
            u_wind_data_list.append(str(u_data))
        print u_wind_data
        u_windJson["data"] = u_wind_data_list

        # V=====================================================
        v_windJson = {}
        v_header = {}
        v_header["nx"] = int(self.u_data.shape[0])
        v_header["ny"] = int(self.u_data.shape[1])
        v_header["lo1"] = float(min(self.u_lon))
        v_header["lo2"] = float(max(self.u_lon))
        v_header["la1"] = float(max(self.u_lat))
        v_header["la2"] = float(min(self.u_lat))
        v_header["dx"] = dx
        v_header["dy"] = dy
        v_header["gridUnits"] = "degrees"

        v_header["parameterNumberName"] = "V-component_of_wind"
        v_header["parameterUnit"] = "m.s-1"
        v_header["parameterCategory"] = 2
        v_header["parameterNumber"] = 3
        v_header["numberPoints"] = v_header["nx"] * v_header["ny"]
        v_header["meta"] = {"date": "2014-11-30T12:00:00.000Z"}
        v_header["gridDefinitionTemplateName"] = "Latitude_Longitude"
        v_header["surface2Type"] = 255

        v_windJson["header"] = v_header
        v_wind_data = self.v_data.flatten()
        v_wind_data_list = []
        for v_data in v_wind_data:
            v_wind_data_list.append(str(v_data))

        print v_wind_data
        v_windJson["data"] = v_wind_data_list
        # --------
        windjson = {}
        windjson["json"] = [u_windJson, v_windJson]
        f = open(self.options.exportFile, "w")
        f.write(json.dumps(windjson["json"]))
        f.close()
