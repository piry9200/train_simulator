import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import Geo_Data as Geo_Data

class Viwer():
    def __init__(self, GD:Geo_Data.Geo_Data, fig_col:str="gray"):
        self.GD = GD
        self.fig_col = fig_col
        # グラフの初期設定
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        for _, row in GD.edges.iterrows():
            line = row["geometry"]
            if isinstance(line, LineString):
                x, y = line.xy
                self.ax.plot(x, y, color="blue", linewidth=1)
        #背景色を変更
        self.ax.set_facecolor(self.fig_col)

    def show(self):
        plt.show()

if __name__ == "__main__":
    place = "nagoya"
    Data = Geo_Data.Geo_Data(place)
    VW = Viwer(Data)
    VW.show()