import sys

class PgnGame():
    def __init__(self, termination, result, moves):
        self.termination = termination
        self.result = result
        self.moves = moves

    def to_string(self):
        return f"termination: {self.termination}, result: {self.result}, moves: {self.moves}"


class PgnParser():
    def __init__(self, file_name):
        self.games = []
        self.position = 0
        self.file = file_name
        self.fields = {"termination", "result"}

    def parse_file(self):
        for i in range(50):
            info = self.read_section()
            moves = self.read_section()
            
            parsed_info = self.parse_info(info)
            parsed_moves = self.parse_moves(moves)
            self.games.append(PgnGame(parsed_info["termination"], parsed_info["result"], parsed_moves))

        for g in self.games:
            print()
            print()
            print(g.to_string())
        
    def read_section(self):
        output = ""
        with open(self.file) as f:
            f.seek(self.position)
            line = f.readline()
            while line != "\n":
                output += line
                line = f.readline()
            self.position = f.tell()
        return output
              
    def parse_info(self, info):
        info = info.split("\n")
        info_map = {}
        for line in info:
            if line == "":
                continue
            field = self.get_field(line).lower()
            if field in self.fields:
                info_map[field] = self.get_value(line)
        return info_map

    def get_field(self, line):
        line = line.split(" ")[0]
        return line[1:]
    
    def get_value(self, line):
        return line.split("\"")[1]

    def parse_moves(self, move_data):
        parsed_moves = []
        moves = move_data.split("{")
        for data in moves:
            move_index = -2
            if "\n" in data:
                data = data[:-1]
                move_index = -1
            data = data.split(" ")
            parsed_moves.append(data[move_index])
        return parsed_moves

parser = PgnParser(sys.argv[1])
parser.parse_file()
