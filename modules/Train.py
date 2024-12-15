from shapely.geometry import LineString, Point

class Train():
    def __init__(self, rail:list):
        self.rail = rail
        self.rail_length = len(self.rail)
        self.posi_idx = 0
        self.coord:Point = self.rail[self.posi_idx]
    
    def move(self) ->None:
        if(self.posi_idx < self.rail_length-1):
            self.posi_idx += 1
            self.coord = self.rail[self.posi_idx]