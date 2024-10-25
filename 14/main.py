import math, time

INPUT = "14/input"
SAND_SOURCE_COORD = (500, 0)
FLOOR_DISTANCE = 2

class ViType:
    OFF = 0
    FAST = 2
    SLOW = 1

VISUALIZE = ViType.FAST

class NodeType:
    AIR = "."
    SAND_SOURCE = "+"
    RESTING_SAND = "o"
    ROCK = "#"
    FALLING_SAND = "~"

class Node:
    def __init__(self, cave, x, y, type = NodeType.AIR):
        self.cave = cave
        self.x = x
        self.y = y
        
        if (self.x, self.y) == SAND_SOURCE_COORD:
            self.type = NodeType.SAND_SOURCE
        elif type is NodeType.ROCK or self.y == self.cave.y_max:
            self.type = NodeType.ROCK
        else:
            self.type = type

    def __eq__(self, other):
        return self.cave == other.cave and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.cave, self.x, self.y))
    
    def __str__(self):
        return self.type

    def sort_key(self):
        return (self.y, self.x)
    
    def get_next_node(self):
        if self.y == self.cave.y_max:
            return NodeType.ROCK
        
        if self.x == self.cave.x_min or self.x == self.cave.x_max:
            if self.x == self.cave.x_min:
                self.cave.x_min -= 1
                x = self.cave.x_min
            else:
                self.cave.x_max += 1
                x = self.cave.x_max
                
            for y in range(self.cave.y_min, self.cave.y_max + 1):
                self.cave.nodes.append(Node(self.cave, x, y))
                self.cave.nodes.sort(key=Node.sort_key)

        below = [
            self.cave.get_node(self.x, self.y + 1),
            self.cave.get_node(self.x - 1, self.y + 1),
            self.cave.get_node(self.x + 1, self.y + 1)
        ]

        for node in below:
            if node.type in [NodeType.AIR, NodeType.FALLING_SAND]:
                return node
            
        return node
    
    def tick(self):
        if self.type is not NodeType.SAND_SOURCE:
            self.type = NodeType.FALLING_SAND
        
        if VISUALIZE is ViType.SLOW:
            self.cave.write_map()
            time.sleep(0.04)

        next_node = self.get_next_node()
        if next_node is None or next_node.type is NodeType.FALLING_SAND:
            if self.type is not NodeType.SAND_SOURCE:
                self.cave.current_sand = self.cave.sand_source
            else:
                self.cave.current_sand = None
        elif next_node.type in [NodeType.ROCK, NodeType.RESTING_SAND]:
            if self.type is not NodeType.SAND_SOURCE:
                self.cave.current_sand = self.cave.sand_source
            else:
                self.cave.current_sand = None

            self.type = NodeType.RESTING_SAND
            self.cave.sand_at_rest += 1

            if VISUALIZE is ViType.FAST:
                self.cave.write_map()
        elif next_node.type is NodeType.AIR:
            if self.type is not NodeType.SAND_SOURCE:
                self.type = NodeType.AIR
            self.cave.current_sand = next_node
    
class Cave:
    def __init__(self):
        self.nodes = []
        self.sand_at_rest = 0
        with open(INPUT, "r", encoding="utf-8") as f:
            for line in f:
                ray_points = list(map(lambda ray_point: [int(ray_point.split(",")[0]), int(ray_point.split(",")[1])], line.split("->")))
                for i, ray_point in enumerate(ray_points[:-1]):
                    ray_point2 = ray_points[i+1]
                    x_sign = int(math.copysign(1, ray_point2[0] - ray_point[0]))
                    y_sign = int(math.copysign(1, ray_point2[1] - ray_point[1]))
                    x_range = range(ray_point[0], ray_point2[0] + x_sign, x_sign)
                    y_range = range(ray_point[1], ray_point2[1] + y_sign, y_sign)
                    for x in x_range:
                        for y in y_range:
                            node = Node(self, x, y, NodeType.ROCK)
                            if node not in self.nodes:
                                self.nodes.append(node)

        self.x_min = min(map(lambda node: node.x, self.nodes)) - 1
        self.x_max = max(map(lambda node: node.x, self.nodes)) + 1
        self.y_min = 0
        self.y_max = max(map(lambda node: node.y, self.nodes)) + FLOOR_DISTANCE
        for y in range(self.y_min, self.y_max + 1):
            for x in range(self.x_min, self.x_max + 1):
                if Node(self, x, y) not in self.nodes:
                    self.nodes.append(Node(self, x, y))
                    
        self.nodes.sort(key=Node.sort_key)
        self.sand_source = self.current_sand = self.get_node(*SAND_SOURCE_COORD)

        self.write_map()
        self.tick()
        self.write_map()

        print(self.sand_at_rest)

    def tick(self):
        while self.current_sand:
            self.current_sand.tick()

    def get_node(self, x, y):
        index = x - self.x_min + (y - self.y_min) * (self.x_max - self.x_min + 1)

        return self.nodes[index]
    
    def write_map(self):
        with open("14/output", "w", encoding="utf-8") as f:
            f.write(str(self))

    def __str__(self):
        string = line_padding = " " * (len(str(self.y_max))) + " "
        for pv in range(len(str(self.x_max))):
            for i in range(self.x_min, self.x_max + 1):
                digit = len(str(i)) - len(str(self.x_max)) + pv
                if digit >= 0:
                    string += str(i)[digit]
                else:
                    string += " "

            string += "\n" + (line_padding if pv != len(str(self.x_max)) - 1 else "")

        padding = len(str(self.y_max))
        string += " " * (padding - 1) + "0 "
        for node in self.nodes:
            string += str(node)
            if node.x == self.x_max and node.y != self.y_max:
                string += f"\n" + " " * (padding - len(str(node.y+1))) + str(node.y+1) + " "

        return string

Cave()