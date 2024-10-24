CHECK_ALL_STARTS = True

START_SYMBOL = "S"
END_SYMBOL = "E"
START_ELEVATION = "a"
END_ELEVATION = "z"

squares = []
starts = []
end = None

class Square:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    DIRS = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, x, y, elevation):
        self.g = None
        self.h = None
        self.parent = None

        self.x = x
        self.y = y
        
        if elevation == START_SYMBOL:
            self.elevation = START_ELEVATION
            starts.insert(0, self)
        elif elevation == START_ELEVATION:
            self.elevation = elevation
            starts.append(self)
        elif elevation == END_SYMBOL:
            self.elevation = END_ELEVATION
            global end
            end = self
        else:
            self.elevation = elevation

    def get_adjacent(self, direction):
        if direction == Square.UP and self.y > 0:
            return squares[self.y - 1][self.x]
        elif direction == Square.DOWN and self.y < len(squares) - 1:
            return squares[self.y + 1][self.x]
        elif direction == Square.LEFT and self.x > 0:
            return squares[self.y][self.x - 1]
        elif direction == Square.RIGHT and self.x < len(squares[self.y]) - 1:
            return squares[self.y][self.x + 1]
        else:
            return None
        
    def compare_elevation(self, other):
        return ord(other.elevation) - ord(self.elevation)

    def can_go(self, direction):
        other = self.get_adjacent(direction)
        return other is not None and self.compare_elevation(other) <= 1
    
    def get_exits(self):
        return [self.get_adjacent(direction) for direction in Square.DIRS if self.can_go(direction)]
    
    def get_h(self):
        if self.h is None:
            self.h = abs(self.x - end.x) + abs(self.y - end.y)

        return self.h
    
    def get_f(self):
        return self.g + self.get_h()
    
    def __str__(self):
        symbol = self.elevation
        if self == start:
            symbol = START_SYMBOL
        elif self == end:
            symbol = END_SYMBOL

        return symbol 

def print_map(current_square, open_list = []):
    path = []
    while current_square:
        path.append(current_square)
        current_square = current_square.parent

    print("\033[H\033[3J", end="") #clear screen
    for row in squares:
        for square in row:
            symbol = str(square)
            #bold for either highlight
            if square in path or square in open_list:
                symbol = "\033[1m" + symbol + "\033[0m"
            # red for path
            if square in path:
                symbol = "\033[91m" + symbol + "\033[0m"
            # blue for open
            elif square in open_list:
                symbol = "\033[94m" + symbol + "\033[0m"
            print(symbol, end="")
        print()
    
    if shortest_path:
        print(f"Shortest path: {shortest_path}")

with open("12/input", "r", encoding="UTF-8") as f:
    for y, line in enumerate(f):
        squares.append([])
        for x, elevation in enumerate(line.strip()):
            squares[y].append(Square(x, y, elevation))

    if not CHECK_ALL_STARTS:
        starts = [starts[0]]

    shortest_path = None
    for start in starts:
        open_list = [start]
        start.g = 0
        closed_list = []
        current_square = None

        while len(open_list):
            current_square = open_list.pop(0)
            if current_square == end:
                if shortest_path is None or current_square.g < shortest_path:
                    shortest_path = current_square.g
                print_map(current_square)
                break

            closed_list.append(current_square)
            for exit in current_square.get_exits():
                if exit in closed_list:
                    continue

                if exit in open_list:
                    if exit.g > current_square.g:
                        continue

                if exit.parent:
                    if exit.g < current_square.g + 1:
                        continue

                if CHECK_ALL_STARTS:
                    if exit.elevation == START_ELEVATION:
                        continue
                    elif shortest_path and current_square.g + 1 >= shortest_path:
                        continue

                exit.g = current_square.g + 1
                exit.parent = current_square
                open_list.append(exit)
            
            open_list.sort(key=lambda square: square.get_f())
            print_map(current_square, open_list)

            
