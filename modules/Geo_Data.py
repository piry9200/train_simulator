import osmnx as ox
import geopandas as gpd
import pandas as pd
from enum import Enum
from shapely.geometry import LineString, MultiLineString
import matplotlib.pyplot as plt


class Geo_Data():
    def __init__(self):
        self._rail_file = "/Users/k22018kk/pri_prg/python/train_simulator/data/railway_data/N02-20_RailroadSection.shp"
        self._station_file = "/Users/k22018kk/pri_prg/python/train_simulator/data/railway_data/N02-20_Station.shp"
        self._aichi_file = "/Users/k22018kk/pri_prg/python/train_simulator/data/Aichi_shape/N03-20240101_23.shp"
        self._aichi_data = gpd.read_file(self._aichi_file)
        self.rail_data = gpd.read_file(self._rail_file)
        self.station_data = gpd.read_file(self._station_file)

        #愛知県内の路線を切り出し，整える
        self.rail_data = self.rail_data.overlay(self._aichi_data, how="intersection")
        self.rail_data = self.rail_data[["N02_003", "geometry"]]
        self.rail_data.columns = ["name", "geometry"]
        #↓name(路線名)ごとにMultilineにまとめる. convertallの仕様上，路線名のカラム名を「name」にしている.
        self.rail_data = convert_all(self.rail_data, "geopandas")
        self.rail_data.columns = ["geometry", "路線名", ]
        self.rail_data.crs = "EPSG:6668" #converallを使うとcrsが消えるので再設定

        #愛知県内の駅を切り出し，整える
        self.station_data = self.station_data.overlay(self._aichi_data, how="intersection")
        self.station_data = self.station_data[["N02_003", "N02_004", "N02_005", "N03_001", "N03_004", "geometry"]]
        self.station_data.columns = ["路線名", "運営会社", "駅名", "都道府県", "市区町村", "geometry"]
        self.station_data["geometry"] = self.station_data["geometry"].centroid # 駅はSTRINGで表されているので，それをPOINTへ変換


# https://arakaki.tokyo/20210919/ から頂いた．同じnameを持つ行のLineStringをMultiLineにまとめる．
#convert_allで返ってくるgdfにはcrsがセットされてないことに注意
def reduce_lines(gdf, to, name):
    '''
    parameters
        gdf: geopandas.GeoDataFrame
            geometry列がLineString型またはMultiLineString型
        to: str
            "pandas" or "geopandas"
        name: 戻り値のDataFrameのname列に使われる
        
    return 
     pandas.DataFrame　columns: ['name', 'group', 'lon', 'lat' ] or
     geopandas.GeoDataFrame columns: ['name', 'geometry']
    '''
    
    class Direction(Enum):
        FORWARD = 0
        BACKWARD = 1   
        
        
    def list_to_gdf(l):
        '''
        parameters
            l: list of tuple of lon/lat
        return
            geopandas.GeoDataFrame
            columns: ['geometry' ]
        '''
        
        gdf = gpd.GeoDataFrame({"geometry": [LineString(l)]})
        return gdf
        
    def list_to_df(l):
        '''
        parameters
            l: list of tuple of lon/lat
        return
            pandas.DataFrame
            columns: ['group', 'lon', 'lat' ]
        '''
        
        df = pd.DataFrame(l, columns=['lon', 'lat'])
        df['group'] = f'{name}_{group_count}'
        return df
    
    def line_to_tuple(iterable, list_of_tuple):
        for i in iterable:
            if isinstance(i, LineString):
                list_of_tuple.append(tuple(i.coords))
            elif isinstance(i, MultiLineString): 
                line_to_tuple(i.geoms, list_of_tuple) #ここは借用元から改変．「i」->「i.geoms」.MultiLineをiterableに取り出すために「geoms」を使う
            
    if to == "pandas":
        list_to = list_to_df
    elif to == "geopandas":
        list_to = list_to_gdf
    else:
        raise TypeError("'to' argument must be 'pandas' or 'geopandas'")
        return
    

    work = list()
    dfs = list()
    lines = list()
    line_to_tuple(gdf.geometry, lines)
    
    lines = list(set(lines))
    
    dir = Direction.BACKWARD
    group_count = 1
    
    
    while lines:
        if not work:
            work.extend(lines.pop(0))
            continue
        
        if dir == Direction.BACKWARD:
            for i, line in enumerate(lines):
                if work[-1] in line:
                    l = list(lines.pop(i))
                    if l[0] != work[-1]:
                        l.reverse()
                    work.extend(l[1:])
                    break
            else:
                dir = Direction.FORWARD
                continue
        else:
            for i, line in enumerate(lines):
                if work[0] in line:
                    l = list(lines.pop(i))
                    if l[-1] != work[0]:
                        l.reverse()
                    work[0:0] = l[:-1]
                    break
            else:
                dfs.append(list_to(work))
                group_count += 1
                work = list()
                dir = Direction.BACKWARD
    
    if work:
        dfs.append(list_to(work))
        
    all = pd.concat(dfs)
    
    if to == "geopandas":
        all = all.dissolve()
    else:
        all.reset_index(drop=True, inplace=True)
        
    all["name"] = name
    return all


def convert_all(gdf, to):
    all = list()
    for name in gdf.name.unique():
        all.append(reduce_lines(gdf.query(f'name.str.startswith("{name}")', engine='python'), to, name))

    all_df = pd.concat(all)
    all_df.reset_index(drop=True, inplace=True)
    return all_df


if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(10, 10))
    Data = Geo_Data()
    #print(Data.station_data.head())
    print(Data.rail_data)
    # Data._aichi_data.plot(ax=ax, color="gray")
    # Data.rail_data.plot(ax=ax, column="路線名", cmap="tab20c")
    # Data.station_data.plot(ax=ax, markersize=10.0, column="路線名")
    # plt.show()
    