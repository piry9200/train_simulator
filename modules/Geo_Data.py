import osmnx as ox
import geopandas

class Geo_Data():
    def __init__(self, place:str):
        self.place = place
        #self._L = ox.graph_from_place(self.place, network_type="all", custom_filter='["railway"~"rail|subway"]')
        self.edges = ox.features_from_place(self.place, tags={"railway":["rail", "subway"]})
        self.edges["length"] = self.culc_length(self.edges)
        self.stations = ox.features_from_place(self.place, tags={"public_transport":"station", "railway":"station"})
        #self.edges = ox.graph_to_gdfs(self._L, nodes=False, edges=True)  #graph_*を使うと，LineStringの長さとかの情報が得られる

    def get_sorted_edges(self) -> geopandas.geodataframe.GeoDataFrame:
        return self.edges.sort_values("length")
    
    #各行の線路の距離を投影座標へ変換してから計算して返す
    def culc_length(self, gdf):
        gdf = gdf.to_crs(epsg=3857)
        return gdf.length


if __name__ == "__main__":
    place = "nagoya"
    Data = Geo_Data(place)
    print(Data.stations.iloc[0]["geometry"].x)