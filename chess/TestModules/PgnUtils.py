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

    def ends_checkmated(self):
        return self.moves != [] and "#" in self.moves[-1]


class PgnParser():
    def __init__(self, file_name, frmt):
        self.games = []
        self.position = 0
        self.file = file_name
        self.fields = {"termination", "result"}
        self.format = frmt

    def to_string(self):
        output = f"parser data: position - {self.position}, file - {self.file}, fields to obtain - {self.fields}\n"
        for g in self.games:
            output += f"{g.to_string()}\n\n"
        return output

    def parse_file(self):
        print(f"parsing {self.file} mode {self.format}")
        
        while True:
            info = self.read_section()
            if info == "":
                break
            moves = self.read_section()
            parsed_info = self.parse_info(info)
            parsed_moves = self.parse_moves(moves)
            print("parse_file", parsed_info, parsed_moves)
            game = PgnGame(parsed_info["termination"], parsed_info["result"], parsed_moves)
            #print("parse_file game,checkmate game:",game.to_string(), self.is_checkmate_game(game))
            print("here",game.get_moves(), game.get_moves() == [])
            if game.get_moves() != []: # or game.get_result() == "1/2-1/2": (when we can sort on stalemates)
                print("parse_file info: ", info)
                print("parse_file: moves: ", moves)
                print("parse_file: game.to_string", game.to_string())
                self.games.append(game)

    def is_checkmate_game(self, game):
        return game.ends_checkmated()

    def read_section(self):
        output = ""
        with open(self.file) as f:
            f.seek(self.position)
            line = f.readline()
            while line != "\n" and line != "":
                output += line
                line = f.readline()
            self.position = f.tell()
        return output
              
    def parse_info(self, info):
        info_map = {}
        if self.format == "custom":
            info_map = {"termination":"custom", "result":"custom"}
        info = info.split("\n")
        for line in info:
            if line == "":
                continue
            field = self.get_field(line).lower()
            if field in self.fields:
                info_map[field] = self.get_value(line)
        print("parse_info:", info_map)
        return info_map

    def get_field(self, line):
        line = line.split(" ")[0]
        return line[1:]
    
    def get_value(self, line):
        return line.split("\"")[1]

    def parse_moves(self, move_data):
        if self.format == "custom":
            move_list = self.custom_parse_moves(move_data)
            return self.add_potential_exit(move_list)
        parsed_moves = []
        moves = move_data.split("{")
        for data in moves:
            if "\n" in data:
                continue
            move_index = -2
            data = data.split(" ")
            parsed_moves.append(data[move_index])
        parsed_moves = self.add_potential_exit(parsed_moves)
        return parsed_moves

    def custom_parse_moves(self, moves):
        moves = self.separate_moves(moves)
        output = []
        for move in moves:
            if move == '' or self.is_result(move) or move == '' or (move[0].isdigit() and move.replace(".", "").isdigit()):
                continue
            else:
                move = move.split(".")[-1]
            output.append(move)
        return output

    def separate_moves(self, moves):
        output = []
        moves = moves.split("\n")
        for move_line in moves:
            output += move_line.split(" ")
        return output

    def is_result(self, move):
        return "1-0" in move or "0-1" in move or "1/2-1/2" in move

    def add_potential_exit(self, moves):
        if not self.is_checkmate_game(PgnGame("N/A", "N/A", moves)):
            return moves + ["exit"]
        return moves

    def get_games(self):
        return self.games