# grib2json_python

# 运行环境
* python 版本：2.7

# 基础环境
* numpy 版本：1.15.3
* gdal 版本：2.3.1
* umOpener 版本：0.0.9

## 参数说明（带*为必传参数）
* ***input_u_file** 输入U风文件
* ***input_v_file** 输入V风文件
* grid_width 插值宽度 默认120
* grid_height 插值高度 默认120
* input_data_type 输入UV风文件格式 默认nc
* input_nodata 输入文件nodata值 默认：9999.0
* ***export_file** 输出文件 例xxx.json


## 示例
```
myWindJsonUtil = WindJsonUtil()
myWindJsonUtil.initParams(input_u_file=u_file,
                          input_v_file=v_file,
                          grid_width ="120",
                          grid_height="120",
                          input_data_type="nc",
                          input_nodata="9999.0",
                          export_file="%s.json" % jsonName)
```

## 外部调用参数说明（带*为必传参数）
* ***--input_u_file** 输入U风文件
* ***--input_v_file** 输入V风文件
* --grid_width 插值宽度 默认120
* --grid_height 插值高度 默认120
* --input_data_type 输入UV风文件格式 默认nc
* --input_nodata 输入文件nodata值 默认：9999.0
* ***--export_file** 输出文件 例xxx.json

## 示例
```angular2html
python windjsonUtils.py --input_u_file /Volumes/pioneer/gdal_Demo/uv/NAFP_CLDAS2.0_RT_GRB_WIU10_20181126-11.nc \
                        --grid_width 120 \
                        --grid_height 120 \
                        --input_v_file /Volumes/pioneer/gdal_Demo/uv/NAFP_CLDAS2.0_RT_GRB_WIV10_20181126-11.nc \
                        --export_file ./abc.json
```
