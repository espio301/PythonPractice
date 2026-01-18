class Piece():
    #a piece should be able to move,
    def __init__(self, color : str, coordinates):
        self.name = ""
        self.color = color
        self.coordinates = coordinates

    def set_coords(self, coordinates):
        self.coordinates = coordinates

    def to_string(self):
        return self.color[0] + self.name[0]

    def get_coords(self):
        return self.coordinates

    def get_color(self):
        return self.color
        
    def move(self):
        pass