import osmnx as ox
import geopandas

class Data_Loader():
    def __init__(self, place:str):
        self.place = place
        self._G = ox.graph_from_place(self.place, network_type="all", custom_filter='["railway"~"rail|subway"]')
        self.edges = ox.graph_to_gdfs(self._G, nodes=False, edges=True)
    
    def get_sorted_edges(self) -> geopandas.geodataframe.GeoDataFrame:
        return self.edges.sort_values("length")

if __name__ == "__main__":
    place = "nagoya"
    Data = Data_Loader(place)
    longest_edge = Data.get_sorted_edges().iloc[-1]["geometry"]
    print(longest_edge)