'''
A GIS toolkit based on Autonavi API. 
'''
import math
import json
import requests
from vnpt import round_half_even

def haversine(lat1, lon1, lat2, lon2):
    """
    计算两个坐标之间的距离(以十进制表示)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def calcPolylineLength(polyline, spilt_str=';',lng_lat=True, unit_as_meter=False):
    '''
    计算折线长度
    polyline 折线坐标
    spilt_str 分隔符
    lng_lat True-longitude在前,latitude在后
    use_meter_unit 使用米作为单位，否则是千米
    '''
    coord_arr = [c for c in polyline.split(spilt_str) if c!='']
    coord_nums = len(coord_arr)
    assert coord_nums>1, f'坐标集合需要大于1，len(polyline)={coord_nums}'
    total_distance = 0 # 总距离-单位-km
    for idx in range(coord_nums - 1):
        coord1 = coord_arr[idx].split(',')
        coord2 = coord_arr[idx+1].split(',')
        total_distance += haversine(float(coord1[0-int(lng_lat)]),float(coord1[1-int(lng_lat)]),float(coord2[0-int(lng_lat)]),float(coord2[1-int(lng_lat)]))
    if unit_as_meter: # 使用米做单位
        total_distance *= 1000
    return total_distance

def transform2gcj02(apikey, coord_str, origin_crs='gps'):
    '''
    转换到gcj02坐标
    经度和纬度用","分割，经度在前，纬度在后，经纬度小数点后不得超过6位。多个坐标对之间用”|”进行分隔最多支持40对坐标。
    'gps'=>crs84

    '''
    url = f"https://restapi.amap.com/v3/assistant/coordinate/convert?locations={coord_str}&coordsys={origin_crs}&output=json&key={apikey}"
    r = requests.get(url)
    if r.status_code==200:
        result = json.loads(r.text)
        result = result['locations']
        return result
    else:
        print(r.text)
        
def coord_transform(apikey, coordinates:list, origin_crs='gps'):
    '''
    批量转换坐标的坐标系到gcj02
    apikey:高德地图apikey
    coordinates：坐标集合，[[lng1,lat1],[lng2,lat2]]
    origin_crs:原始坐标系
    return:转换后的坐标集合
    '''
    limit = 40
    epochs = math.ceil(len(coordinates)/limit)
    transformations = []
    for epoch in range(epochs):
        collections = coordinates[epoch*limit: min(epoch*limit+limit, len(coordinates))]
        for i,coord in enumerate(collections):
            coord = list(map(lambda x:round_half_even(x, 6), coord))# round to six decimal places
            collections[i] = ",".join(map(lambda x:str(x),coord))
        coord_str = "|".join(collections)
        locations = transform2gcj02(apikey,coord_str,origin_crs).split(';')
        for coord in locations:
            transformations.append([float(x) for x in coord.split(',')])
    return transformations

class GisTool():
    def __init__(self,apikey) -> None:
        self.apikey = apikey
        
    @staticmethod
    def load_geojson(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def crs_transform(self,geojson):
        if not (isinstance(geojson,dict) and 'features' in geojson.keys()):
            geojson = GisTool.load_geojson(geojson)
        features = geojson['features']
        limit = 40 # The API can only tranform 40 coordinates at a time. 
        assert len(features)>0,'The amount of the features in GeoJson should be greater than 0.'
        for idx,featrue in enumerate(features):
            geometry = featrue['geometry']
            coordinates = geometry['coordinates'][0][0]
            transformations = coord_transform(self.apikey, coordinates)
            geometry['coordinates'][0][0] = list(transformations)

