import sys

class PgnGame():
    def __init__(self):
        self.termination = None
        self.result

class PgnParser():
    def __init__(self, file_name):
        self.games = []
        self.position = 0
        self.file = file_name


    def parse_file(self):
        info = self.read_section()
        moves = self.read_section()
        print(info,moves)
        #self.parse_info(info)
        #self.parse_moves(moves)
        #self.parse_game()
        
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
              
parser = PgnParser(sys.argv[1])
parser.parse_file()
