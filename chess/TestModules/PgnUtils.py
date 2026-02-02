import sys

class PgnGame():
    def __init__(self, termination, result, moves):
        self.termination = termination
        self.result = result
        self.moves = moves

    def to_string(self):
        return f"termination: {self.termination}, result: {self.result}, moves: {self.moves}"
    
    def get_moves(self):
        return self.moves

    def get_result(self):
        return self.result

class PgnParser():
    def __init__(self, file_name):
        self.games = []
        self.position = 0
        self.file = file_name
        self.fields = {"termination", "result"}

    def to_string(self):
        output = f"parser data: position - {self.position}, file - {self.file}, fields to obtain - {self.fields}\n"
        for g in self.games:
            output += f"{g.to_string()}\n\n"
        return output

    def parse_file(self):
        print("parsing")
        for i in range(50):
            info = self.read_section()
            moves = self.read_section()
            parsed_info = self.parse_info(info)
            parsed_moves = self.parse_moves(moves)
            print("parse_file", parsed_info, parsed_moves)
            game = PgnGame(parsed_info["termination"], parsed_info["result"], parsed_moves)
            print("parse_file game,checkmate game:",game.to_string(), self.is_checkmate_game(game))
            if self.is_checkmate_game(game): # or game.get_result() == "1/2-1/2": (when we can sort on stalemates)
                print("parse_file info: ", info)
                print("parse_file: moves: ", moves)
                print("parse_file: game.to_string", game.to_string())
                self.games.append(game)

        
    def is_checkmate_game(self, game):
        moves = game.get_moves()
        return "#" in moves[-1]

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
            if "\n" in data:
                continue
            move_index = -2
            data = data.split(" ")
            parsed_moves.append(data[move_index])
        return parsed_moves

    def get_games(self):
        return self.games