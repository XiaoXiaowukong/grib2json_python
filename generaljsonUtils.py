# -*- coding:utf-8 -*-
topflor = 0  # 最外层
import json


class GeneraljsonUtils():
    def __init__(self):
        pass

    def initParams(self, **kwgs):
        print kwgs
        alljson = {}
        for kwarg_key in kwgs.keys():
            print kwarg_key
            print kwgs[kwarg_key]
            if (kwgs[kwarg_key][0] == 0):

                alljson[kwarg_key] = kwgs[kwarg_key][1]

        print json.dumps(alljson)
        print alljson
