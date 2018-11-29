# -*- coding:utf-8 -*-
__version__ = '$Id: windjsonUtils.py 27349 2018-11-29 18:58:51Z rouault $'
import numpy as np
import os
import json


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
        arguments = []
        for kwarg_key in kwgs.keys():
            arguments.append("--%s" % kwarg_key)
            arguments.append(kwgs[kwarg_key])
        (self.options, self.args) = self.parser.parse_args(args=arguments)
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
        # [{"header":{"discipline":0,"disciplineName":"Meteorological products","gribEdition":2,"gribLength":133963,"center":7,"centerName":"US National Weather Service - NCEP(WMC)","subcenter":0,"refTime":"2014-11-30T06:00:00.000Z","significanceOfRT":1,"significanceOfRTName":"Start of forecast","productStatus":0,"productStatusName":"Operational products","productType":1,"productTypeName":"Forecast products","productDefinitionTemplate":0,"productDefinitionTemplateName":"Analysis/forecast at horizontal level/layer at a point in time","parameterCategory":2,"parameterCategoryName":"Momentum","parameterNumber":2,"parameterNumberName":"U-component_of_wind","parameterUnit":"m.s-1","genProcessType":2,"genProcessTypeName":"Forecast","forecastTime":6,"surface1Type":100,"surface1TypeName":"Isobaric surface","surface1Value":85000,"surface2Type":255,"surface2TypeName":"Missing","surface2Value":0,"gridDefinitionTemplate":0,"gridDefinitionTemplateName":"Latitude_Longitude","numberPoints":65160,"shape":6,"shapeName":"Earth spherical with radius of 6,371,229.0 m","gridUnits":"degrees","resolution":48,"winds":"true","scanMode":0,"nx":360,"ny":181,"basicAngle":0,"subDivisions":0,"lo1":0,"la1":90,"lo2":359,"la2":-90,"dx":1,"dy":1},"data":[3.88
        # "lo1":0, "la1":90, "lo2":359, "la2":-90
        # ,{"header":{"discipline":0,"disciplineName":"Meteorological products","gribEdition":2,"gribLength":133963,"center":7,"centerName":"US National Weather Service - NCEP(WMC)","subcenter":0,"refTime":"2014-11-30T06:00:00.000Z","significanceOfRT":1,"significanceOfRTName":"Start of forecast","productStatus":0,"productStatusName":"Operational products","productType":1,"productTypeName":"Forecast products","productDefinitionTemplate":0,"productDefinitionTemplateName":"Analysis/forecast at horizontal level/layer at a point in time","parameterCategory":2,"parameterCategoryName":"Momentum","parameterNumber":3,"parameterNumberName":"V-component_of_wind","parameterUnit":"m.s-1","genProcessType":2,"genProcessTypeName":"Forecast","forecastTime":6,"surface1Type":100,"surface1TypeName":"Isobaric surface","surface1Value":85000,"surface2Type":255,"surface2TypeName":"Missing","surface2Value":0,"gridDefinitionTemplate":0,"gridDefinitionTemplateName":"Latitude_Longitude","numberPoints":65160,"shape":6,"shapeName":"Earth spherical with radius of 6,371,229.0 m","gridUnits":"degrees","resolution":48,"winds":"true","scanMode":0,"nx":360,"ny":181,"basicAngle":0,"subDivisions":0,"lo1":0,"la1":90,"lo2":359,"la2":-90,"dx":1,"dy":1}
        # U
        u_windJson = {}
        u_header = {}
        u_header["nx"] = int(self.u_data.shape[1])
        u_header["ny"] = int(self.u_data.shape[2])
        u_header["lo1"] = float(min(self.u_lon))
        u_header["lo2"] = float(max(self.u_lon))
        u_header["la1"] = float(max(self.u_lat))
        u_header["la2"] = float(min(self.u_lat))
        u_header["parameterNumberName"] = "U-component_of_wind"
        u_header["parameterUnit"] = "m.s-1"
        u_header["parameterCategory"] = 2
        u_header["numberPoints"] = u_header["nx"] * u_header["ny"]
        u_header["meta"] = {"date": "2014-11-30T12:00:00.000Z"}
        u_header["gridDefinitionTemplateName"] = "Latitude_Longitude"

        print min(self.u_lon)
        print max(self.u_lon)
        u_windJson["header"] = u_header
        u_wind_data = self.u_data[0].flatten()
        u_windJson["data"] = u_wind_data.tolist()

        # V
        v_windJson = {}
        v_header = {}
        v_header["nx"] = int(self.u_data.shape[1])
        v_header["ny"] = int(self.u_data.shape[2])
        v_header["lo1"] = float(min(self.u_lon))
        v_header["lo2"] = float(max(self.u_lon))
        v_header["la1"] = float(max(self.u_lat))
        v_header["la2"] = float(min(self.u_lat))
        v_header["parameterNumberName"] = "V-component_of_wind"
        v_header["parameterUnit"] = "m.s-1"
        v_header["parameterCategory"] = 2
        v_header["numberPoints"] = v_header["nx"] * v_header["ny"]
        v_header["meta"] = {"date": "2014-11-30T12:00:00.000Z"}
        v_header["gridDefinitionTemplateName"] = "Latitude_Longitude"

        print min(self.u_lon)
        print max(self.u_lon)
        v_windJson["header"] = v_header
        v_wind_data = self.v_data[0].flatten()
        v_windJson["data"] = v_wind_data.tolist()
        windjson = {}
        windjson["json"] = [u_windJson, v_windJson]

        f = open(self.options.exportFile, "w")
        f.write(json.dumps(windjson["json"]))
        f.close()
        pass

    # ==================================================================================================
    def stop(self):
        self.stopped = True
