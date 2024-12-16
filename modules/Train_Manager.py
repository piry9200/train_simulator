from Geo_Data import Geo_Data
from shapely.geometry import LineString, Point, MultiLineString
import numpy as np

class Train():
    def __init__(self, id, rail:list[Point]):
        self.id = id
        self.rail = rail
        self.rail_length = len(self.rail)
        self.posi_idx = 0
        self.coord:Point = self.rail[self.posi_idx]
    
    def move(self) ->None:
        if(self.posi_idx < self.rail_length-1):
            self.posi_idx += 1
            self.coord = self.rail[self.posi_idx]

class Train_Manager():
    #インスタンス作成時に，走るレールの情報を持った電車を作成し，リストで管理
    def __init__(self, rails:list[list[Point]]): #ここのrailsは後々電車の運行を管理するクラスのインスタンスとかになるべき
        self.train_num = len(rails)#ここも便宜的にこうしてる
        self.enableID = 0 #電車に付与するID．ある電車に付与するたびにインクリメント
        self.train_list:list[Train] = list()
        for i in range(self.train_num):
            train = Train(self.enableID, rails[i])
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
    data = Geo_Data()
    distance_interval = 0.0001
    route1:MultiLineString = data.rail_data.iloc[6]["geometry"]
    rail1 = [route1.interpolate(d) for d in np.arange(0, route1.length, distance_interval)]
    route2:MultiLineString = data.rail_data.iloc[0]["geometry"]
    rail2 = [route2.interpolate(d) for d in np.arange(0, route2.length, distance_interval)]
    rails = [rail1, rail2]
    train_m = Train_Manager(rails)
    for i in range(30):
        print(train_m.step())
