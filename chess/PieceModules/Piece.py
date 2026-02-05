class Piece():
    #a piece should be able to move,
    def __init__(self, color : str, coordinates):
        self.name = ""
        self.color = color
        self.coordinates = coordinates
        self.move_patterns = []

    def set_coords(self, coordinates):
        self.coordinates = coordinates

    def to_string(self):
        return self.color[0] + self.name[0]

    def get_coords(self):
        return self.coordinates

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_move_patterns(self):
        return self.move_patterns

    def copy(self):
        type_piece = type(self)
        copy_coords = []
        for i in self.coordinates:
            copy_coords.append(i)
        return type_piece(self.color, copy_coords)

    def is_valid_move_pattern(self, destination):
        movement_delta = []
        for i in range(2):
            movement_delta.append(destination[i] - self.coordinates[i])
        if movement_delta in self.move_patterns:
            return True
        return False
