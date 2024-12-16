import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from shapely.geometry import LineString, Point, MultiLineString
import numpy as np
from Geo_Data import Geo_Data
from Train import Train

class Viwer():
    def __init__(self, GD:Geo_Data, Train:Train, fig_col:str="gray"):
        self.GD = GD
        self.Train = Train
        self.fig_col = fig_col
        # グラフの初期設定
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        #愛知県と路線と駅をプロット
        self.GD._aichi_data.plot(ax=self.ax, color="gray")
        self.GD.rail_data.plot(ax=self.ax, column="路線名", cmap="tab20c")
        self.GD.station_data.plot(ax=self.ax, markersize=9.0, column="路線名")        
        #背景色を変更
        self.ax.set_facecolor(self.fig_col)

        #電車を表すための点オブジェクトをself.ax上に用意. ,は重要．ax.plotは複数の戻り値を返すが，その先頭だけを受け取りたい．
        self.train_point, = self.ax.plot([], [], 'ro', label="Train", markersize=5)

        # アニメーション作成
        self.ani = FuncAnimation(fig=self.fig, func=self.step, interval=10, blit=True)

    def step(self, frame)->plt.axes:
        train_coord = self.Train.coord
        self.Train.move()
        self.train_point.set_data([train_coord.x], [train_coord.y])  # リストに変換
        return self.train_point,

    def show(self):
        self.ax.set_title("Train Animation on Railway Network", fontsize=16)
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")
        self.ax.legend()
        plt.show()

if __name__ == "__main__":
    data = Geo_Data()
    route:LineString = data.rail_data.iloc[260]["geometry"]
    distance_interval = 0.0001
    rail = [route.interpolate(d) for d in np.arange(0, route.length, distance_interval)]
    train = Train(rail)
    VW = Viwer(data, train)
    VW.show()