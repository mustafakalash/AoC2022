INPUT = "test"
OUTPUT = "15/output"

class Node:
    def __init__(self, cave, x, y):
        self.cave = cave
        self.x = x
        self.y = y
        self.can_have_beacon = True

        if self not in self.cave.nodes:
            self.cave.nodes.append(self)
            self.cave.nodes.sort(key=Node.sort_key)

    def __str__(self):
        return "." if self.can_have_beacon else "#"
    
    def __eq__(self, other):
        return self.cave == other.cave and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.cave, self.x, self.y))

    def sort_key(self):
        return (self.y, self.x)
    
class Sensor(Node):
    def __init__(self, cave, x, y, closest_beacon):
        super().__init__(cave, x, y)
        self.closest_beacon = closest_beacon

    def __str__(self):
        return "S"
    
class Beacon(Node):
    def __str__(self):
        return "B"

class Cave:
    def __init__(self):
        self.nodes = []
        with open(INPUT, mode="r", encoding="utf-8") as f:
            for line in f:
                coord_pairs = []
                for coords in line.split(":"):
                    coord_pairs.append(list(map(lambda coord: int(coord.split("=")[1]), coords.split(","))))

                beacon = Beacon(self, coord_pairs[1][0], coord_pairs[1][1])
                Sensor(self, coord_pairs[0][0], coord_pairs[0][1], beacon)

        self.x_min = min(map(lambda node: node.x, self.nodes))
        self.x_max = max(map(lambda node: node.x, self.nodes))
        self.y_min = min(map(lambda node: node.y, self.nodes))
        self.y_max = max(map(lambda node: node.y, self.nodes))

        for x in range(self.x_min, self.x_max + 1):
            for y in range(self.y_min, self.y_max + 1):
                    Node(self, x, y)

        self.write_map()

    def get_node(self, x, y):
        index = x - self.x_min + (y - self.y_min) * (self.x_max - self.x_min + 1)

        return self.nodes[index]
    
    def __str__(self):
        y_padding = len(str(self.y_max))
        string = " " * (y_padding + 1)
        for y in range(self.y_min, self.y_max + 1):
            string += str(y).rjust(y_padding) + " "
            for x in range(self.x_min, self.x_max + 1):
                string += str(self.get_node(x, y))
            string += "\n"

        return string
    
    def write_map(self):
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(str(self))

Cave()