import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation
from shapely.geometry import LineString, Point, MultiLineString
import numpy as np
from Geo_Data import Geo_Data
from Train_Manager import Train_Manager

class Viwer():
    def __init__(self, GD:Geo_Data, Train_M:Train_Manager, fig_col:str="black"):
        self.GD = GD
        self.Train_M = Train_M
        self.fig_col = fig_col
        # グラフの初期設定
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        #愛知県と路線と駅をプロット
        self.GD._aichi_data.plot(ax=self.ax, color="gray")
        self.GD.rail_data.plot(ax=self.ax, column="路線名", cmap="tab20c")
        self.GD.station_data.plot(ax=self.ax, markersize=9.0, column="路線名")        
        #背景色を変更
        self.ax.set_facecolor(self.fig_col)

        #存在している電車の座標を表す点の一覧を作成．(このままだと電車数の動的な変化に対応できないので改善の余地あり)
        self.train_point_dict:dict[int:Line2D] = dict()
        for train in self.Train_M.train_list:
            #電車を表すための点オブジェクトをself.ax上に用意. ,は重要．ax.plotは複数の戻り値を返すが，その先頭だけを受け取りたい．
            train_point, = self.ax.plot([], [], 'ro', label="Train", markersize=5)
            self.train_point_dict[train.id] = train_point

        # アニメーション作成
        self.ani = FuncAnimation(fig=self.fig, func=self.step, interval=10)

    def step(self, frame)->plt.axes:
        train_coord_dict = self.Train_M.step()
        for train_id in train_coord_dict.keys():
            train_coord = train_coord_dict[train_id]
            self.train_point_dict[train_id].set_data([train_coord.x], [train_coord.y])  # リストに変換

    def show(self):
        self.ax.axis("off")
        plt.show()

if __name__ == "__main__":
    data = Geo_Data()
    route:MultiLineString = data.rail_data.iloc[6]["geometry"]
    distance_interval = 0.0001
    rail = [route.interpolate(d) for d in np.arange(0, route.length, distance_interval)]
    train_m = Train_Manager(rail)
    VW = Viwer(data, train_m)
    VW.show()