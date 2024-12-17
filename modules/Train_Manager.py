from Geo_Data import Geo_Data
from shapely.geometry import LineString, Point, MultiLineString, Polygon
from geopandas import GeoDataFrame
import numpy as np
import Utils

class Train():
    def __init__(self, id, rail:list[Point], departure:Point, destination:Point):
        self.id:int = id
        self.ismove:bool = False 
        self.departure:Point = departure
        self.destination:Point = destination
        self.rail:list[Point] = rail
        self.rail_length = len(self.rail)
        self.posi_idx = 0
        self.coord:Point = self.rail[self.posi_idx]
    
    def move(self) ->None:
        if(self.posi_idx < self.rail_length-1):
            self.posi_idx += 1
            self.coord = self.rail[self.posi_idx]

class Train_Manager():
    #インスタンス作成時に，IDと走るレールの情報を持った電車インスタンスを作成し，リストで管理(動的に作れるようにするべき)
    def __init__(self, rails:list[list[Point]], departures:list[Point], destinations:list[Point]): #ここのrailsは後々電車の運行を管理するクラスのインスタンスとかになるべき
        self.train_num = len(rails)#ここも便宜的にこうしてる
        self.enableID = 0 #電車に付与するID．ある電車に付与するたびにインクリメント
        self.train_list:list[Train] = list()
        for i in range(self.train_num):
            train = Train(self.enableID, rails[i], departures[i], destinations[i])
            self.train_list.append(train)
            self.enableID += 1 #IDをインクリメント

    #リスト内の電車を次の座標へ移動させ，すべての電車らの位置をもつ辞書型を返す．keyは該当する電車のID
    def step(self) ->dict[int:Point]:
        train_coord_dict = dict()
        for train in self.train_list:
            train_coord_dict[train.id] = train.coord
            train.move()
        return train_coord_dict
    
if __name__ == "__main__":
    # data = Geo_Data()
    # distance_interval = 0.0001
    # #路線を選択
    # route1_gdf = data.rail_data.iloc[0]
    # route1_MultiSt:MultiLineString = route1_gdf["geometry"]
    # #路線の位置情報を表すPointのリストを作成
    # route1_rail:list[Point] = [route1_MultiSt.interpolate(d) for d in np.arange(0, route1_MultiSt.length, distance_interval)]
    # #その路線上の駅を選択
    # route1_line:str = route1_gdf["路線名"]
    # stations:GeoDataFrame = data.station_data[ data.station_data["路線名"] == route1_line ]
    # route1_departure:Polygon = stations[ stations["駅名"] == "保見" ]["geometry"].values[0]
    # route1_destination:Polygon = stations[ stations["駅名"] == "八草" ]["geometry"].values[0]
    # #路線上を表すPointリストの中から，駅に該当するPointを取得
    # route1_departure:Point = Utils.culc_station_point(route1_rail, route1_departure)
    # route1_destination:Point = Utils.culc_station_point(route1_rail, route1_destination)

    # rails:list[MultiLineString] = [route1_MultiSt]
    # departures:list[Point] = [route1_departure]
    # destinations:list[Point] = [route1_destination]


    data = Geo_Data()
    distance_interval = 0.0001
    #路線を選択
    route1_gdf = data.rail_data.iloc[0]
    route1_MultiSt:MultiLineString = route1_gdf["geometry"]
    #その路線で移動するための，始発駅と終点駅を選択
    route1_line:str = route1_gdf["路線名"]
    stations:GeoDataFrame = data.station_data[ data.station_data["路線名"] == route1_line ]
    route1_departure:Polygon = stations[ stations["駅名"] == "保見" ]["geometry"].values[0]
    route1_destination:Polygon = stations[ stations["駅名"] == "八草" ]["geometry"].values[0]
    #決定した区間の走行位置を表すPointのリストを作る．
    route1_MultiSt = Utils.culc_line_segment(route1_departure, route1_destination, route1_MultiSt) #区間のMultiStringでroute1_MultiStを上書き
    route1_rail:list[Point] = [route1_MultiSt.interpolate(d) for d in np.arange(0, route1_MultiSt.length, distance_interval)]

    #↑が複数あると仮定して，リストにまとめる
    rails:list[list[Point]] = [route1_rail]
    departures:list[Polygon] = [route1_departure]
    destinations:list[Polygon] = [route1_destination]


    #路線の位置情報を表すPointのリストを作成
    train_m = Train_Manager(rails, departures, destinations)
    for i in range(30):
        print(train_m.step())
