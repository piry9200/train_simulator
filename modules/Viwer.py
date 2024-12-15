import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import Data_Loader

class Viwer():
    def __init__(self, DL:Data_Loader.Data_Loader, fig_col:str="gray"):
        self.DL = DL
        self.fig_col = fig_col
        # グラフの初期設定
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        for _, row in DL.edges.iterrows():
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
    Data = Data_Loader.Data_Loader(place)
    VW = Viwer(Data)
    VW.show()