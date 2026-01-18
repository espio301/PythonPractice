#from abc import ABC, abstractmethod

class Piece():
    #a piece should be able to move,
    def __init__(self, color : str, coordinates):
        self.name = ""
        self.color = color
        self.coordinates = coordinates 

    def set_coords(self, coordinates):
        self.coordinates = coordinates

    def get_coords(self):
        return self.coordinates

    def move(self):
        pass

    #should have a name
    #should have 