from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import numpy as np
import osmnx as ox
import geopandas

# 路線データを取得
G = ox.graph_from_place("Nagoya, Japan", network_type="all", custom_filter='["railway"~"rail|subway"]')
edges: geopandas.geodataframe.GeoDataFrame = ox.graph_to_gdfs(G, nodes=False, edges=True)

# 路線の一つを選択
route = edges.sort_values("length").iloc[-1]["geometry"]

# グラフの初期設定
fig, ax = plt.subplots(figsize=(10, 10))
for _, row in edges.iterrows():
    line = row["geometry"]
    if isinstance(line, LineString):
        x, y = line.xy
        ax.plot(x, y, color="blue", linewidth=1)
#背景色を変更
ax.set_facecolor("gray")

# 路線上を移動する座標を生成
distance_interval = 0.0001
points = [route.interpolate(d) for d in np.arange(0, route.length, distance_interval)]

#電車の位置を示す点
train_marker, = ax.plot([], [], 'ro', label="Train", markersize=5)


# フレーム更新関数
def update(frame): #update関数の中でax.plotすると点が複数できちゃうから，あらかじめ，train_makerを用意し，こいつの位置を変更する
    train_marker.set_data([points[frame].x], [points[frame].y])  # リストに変換
    return train_marker,

# アニメーション作成
ani = FuncAnimation(fig, update, frames=len(points), interval=20, blit=True)

ax.set_title("Train Animation on Railway Network", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.legend()

# アニメーション表示
plt.show()
