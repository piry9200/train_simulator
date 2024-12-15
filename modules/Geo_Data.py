import osmnx as ox
import geopandas

class Geo_Data():
    def __init__(self, place:str):
        self.place = place
        #線路データを成形
        self.edges = ox.features_from_place(self.place, tags={"railway":["rail", "subway"]})
        self.edges = self.edges[["geometry", "name"]]
        self.edges = self.edges.dropna(how="any")
        self.edges["length"] = self.culc_length(self.edges)
        #駅データを成形
        self.stations = ox.features_from_place(self.place, tags={"railway":"station"})
        self.stations = self.stations[["geometry", "name"]]
        self.stations = self.stations.dropna(how="any")
        
        

    def get_sorted_edges(self) -> geopandas.geodataframe.GeoDataFrame:
        return self.edges.sort_values("length")
    
    #各行の線路の距離を投影座標へ変換してから計算して返す
    def culc_length(self, gdf):
        gdf = gdf.to_crs(epsg=3857)
        return gdf.length


if __name__ == "__main__":
    place = "Aichi,Japan"
    Data = Geo_Data(place)
    print(Data.edges)