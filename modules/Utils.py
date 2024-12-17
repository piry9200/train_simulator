from shapely.geometry import LineString, Point, MultiLineString, Polygon
import shapely
import shapely.ops

#レールを表すPointのリストと駅を表すポリゴンから，電車がレイル上で留まるべき位置をPointで返す．
def culc_station_point(rail:list[Point], station:Polygon) -> Point:
    candidate_points = list()
    for rail_point in rail:
        if( shapely.within(rail_point, station) ):
            candidate_points.append(rail_point)
    return candidate_points[len(candidate_points)//2] #リストの真ん中のインデックスのPointを返す


def culc_line_segment(polygon1:Polygon, polygon2:Polygon, line:MultiLineString):
    #ある2つのPointと，*Linestringが与えられたとき，2点を両端とする*Linestringを返す
    # 0   1   2   3   4
    #---[---]---[---]---　　←「この状態」
    #-が路線，[--]が駅ポリゴンとその内側の路線を表す．ある区間を走らせるには1,2,3の情報だけをあればいい．
    #すべての入力駅と路線が「この関係」になっていることが仮定されている
    #[--]---[---]--
    #みたいなケースがあったらうまく動かないかも
    edge_polygons = shapely.multipolygons([polygon1, polygon2])
    segments = shapely.ops.split(line, edge_polygons)
    segments = shapely.multilinestrings([segments.geoms[1], segments.geoms[2], segments.geoms[3]]) #1,2,3の情報を抜き出す．
    return segments