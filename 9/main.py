def clamp(value, bottom, top):
    return max(bottom, min(value, top))


class Knot:
    _X_INDEX = 0
    _Y_INDEX = 1

    _directions = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1)
    }

    def __init__(self, tail=None):
        self.pos = (0, 0)
        self.visited_positions = set()
        self.visited_positions.add(self.pos)
        self.tail = tail

    def move(self, direction, amount=1):
        if isinstance(direction, str):
            direction = self._directions[direction]

        for _ in range(amount):
            self.pos = (self.pos[self._X_INDEX] + direction[self._X_INDEX],
                        self.pos[self._Y_INDEX] + direction[self._Y_INDEX])
            self.visited_positions.add(self.pos)

            if self.tail:
                if (abs(self.pos[self._X_INDEX] - self.tail.pos[self._X_INDEX]) > 1
                        or abs(self.pos[self._Y_INDEX] - self.tail.pos[self._Y_INDEX]) > 1):

                    displacement = (
                        clamp(self.pos[self._X_INDEX] - self.tail.pos[self._X_INDEX], -1, 1),
                        clamp(self.pos[self._Y_INDEX] - self.tail.pos[self._Y_INDEX], -1, 1)
                    )

                    self.tail.move(displacement)


def __main__():
    with open("9/input", "r", encoding = "UTF-8") as f:
        MOVE_INDEX = 0
        AMOUNT_INDEX = 1
        KNOTS = 10

        tail = Knot()
        head = tail
        for _ in range(KNOTS - 1):
            head = Knot(head)

        p1_tail = head.tail

        for line in f:
            line = line.strip().split(" ")
            if not line:
                continue

            head.move(line[MOVE_INDEX], int(line[AMOUNT_INDEX]))

        print(len(p1_tail.visited_positions))
        print(len(tail.visited_positions))


__main__()
