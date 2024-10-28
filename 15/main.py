import time

INPUT = "test"
OUTPUT = "15/output"
TEST_ROW = 10

class ViType:
    OFF = 0
    SLOW = 1
    FAST = 2

VISUALIZE = ViType.SLOW

class Node:
    def __init__(self, cave, x, y, can_have_beacon=True):
        self.cave = cave
        self.x = x
        self.y = y
        self.can_have_beacon = can_have_beacon

        if self not in self.cave.nodes:
            self.cave.nodes.append(self)

    def __str__(self):
        return "." if self.can_have_beacon else "#"
    
    def __eq__(self, other):
        return self.cave == other.cave and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.cave, self.x, self.y))

    def sort_key(self):
        return (self.y, self.x)

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
class Sensor(Node):
    def __init__(self, cave, x, y, closest_beacon):
        super().__init__(cave, x, y, False)
        self.closest_beacon = closest_beacon
        self.beacon_distance = self.distance_to(self.closest_beacon)

    def __str__(self):
        return "S"
    
class Beacon(Node):
    def __init__(self, cave, x, y):
        super().__init__(cave, x, y, False)
        
    def __str__(self):
        return "B"

class Cave:
    def __init__(self):
        print("reading input")
        self.nodes = []
        with open(INPUT, mode="r", encoding="utf-8") as f:
            for line in f:
                coord_pairs = []
                for coords in line.split(":"):
                    coord_pairs.append(list(map(lambda coord: int(coord.split("=")[1]), coords.split(","))))

                beacon = Beacon(self, coord_pairs[1][0], coord_pairs[1][1])
                Sensor(self, coord_pairs[0][0], coord_pairs[0][1], beacon)

        print("filling map")
        self.x_min = min(map(lambda node: node.x, self.nodes))
        self.x_max = max(map(lambda node: node.x, self.nodes))
        self.y_min = min(map(lambda node: node.y, self.nodes))
        self.y_max = max(map(lambda node: node.y, self.nodes))

        self.update_size(force_update = True)

        self.write_map()

        print("rule out beacons")
        print(self.rule_out_beacons())

        if VISUALIZE is ViType.OFF:
            self.write_map()

    def update_size(self, x_min = None, y_min = None, x_max = None, y_max = None, force_update = False):
        update = force_update
        if x_min is not None: self.x_min = min(self.x_min, x_min); update = True
        if y_min is not None: self.y_min = min(self.y_min, y_min); update = True
        if x_max is not None: self.x_max = max(self.x_max, x_max); update = True
        if y_max is not None: self.y_max = max(self.y_max, y_max); update = True

        if update:
            for x in range(self.x_min, self.x_max + 1):
                for y in range(self.y_min, self.y_max + 1):
                    y_width = max(len(str(self.y_min)), len(str(self.y_max)))
                    x_width = max(len(str(self.x_min)), len(str(self.x_max)))
                    print(f"{x}, {y}".ljust(x_width + y_width + 2), end="\r")
                    Node(self, x, y)

            print()

            self.nodes.sort(key=Node.sort_key)

        if force_update:
            print("adjusting map for beacon radius")
            for node in filter(lambda n: isinstance(n, Sensor), self.nodes):
                x_min = node.x - node.beacon_distance
                x_max = node.x + node.beacon_distance
                y_min = node.y - node.beacon_distance
                y_max = node.y + node.beacon_distance
                self.update_size(x_min, y_min, x_max, y_max)

    def get_node(self, x, y):
        index = x - self.x_min + (y - self.y_min) * (self.x_max - self.x_min + 1)

        return self.nodes[index]
    
    def __str__(self):
        x_label_width = max(len(str(self.x_max)), len(str(self.x_min)))
        y_label_width = max(len(str(self.y_max)), len(str(self.y_min)))

        string = " " * (y_label_width + 1)
        for pv in range(x_label_width):
            for i in range(self.x_min, self.x_max + 1):
                digit = len(str(i)) - x_label_width + pv
                if digit >= 0:
                    string += str(i)[digit]
                else:
                    string += " "
            string += "\n" + (" " * (y_label_width + 1) if pv < x_label_width - 1 else "")
        for y in range(self.y_min, self.y_max + 1):
            string += str(y).rjust(y_label_width) + " "
            for x in range(self.x_min, self.x_max + 1):
                string += str(self.get_node(x, y))
            string += "\n"

        return string
    
    def write_map(self):
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(str(self))

    def rule_out_beacons(self):
        test_no_beacons = 0
        
        for sensor in filter(lambda n: isinstance(n, Sensor), self.nodes):
            for node in self.nodes:
                if node.can_have_beacon:
                    if node.distance_to(sensor) <= sensor.beacon_distance:
                        node.can_have_beacon = False
                        if node.y == TEST_ROW:
                            test_no_beacons += 1
                        if VISUALIZE is ViType.SLOW:
                            self.write_map()
                            time.sleep(0.05)

        if VISUALIZE is ViType.FAST:
            self.write_map()

        return test_no_beacons

Cave()