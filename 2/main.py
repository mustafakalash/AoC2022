class Throw:
    points = None
    beats = None

    @classmethod
    def __gt__(cls, other):
        return cls.beats.__eq__(other)

    @classmethod
    def __eq__(cls, other):
        return cls.points == other.points

class Scissors(Throw):
    points = 3

class Rock(Throw):
    points = 1
    beats = Scissors

class Paper(Throw):
    points = 2
    beats = Rock

Scissors.beats = Paper

THROWS = {
    "A": Rock,
    "X": Rock,
    "B": Paper,
    "Y": Paper,
    "C": Scissors,
    "Z": Scissors
}

LOSE = 0
TIE = 1
WIN = 2

OUTCOMES = {
    "X": LOSE,
    "Y": TIE,
    "Z": WIN
}

part1_score = 0
part2_score = 0
with open("2/input") as f:
    for line in f:
        line = line.strip().split(" ")
        opponent = THROWS[line[0]]
        part1_you = THROWS[line[1]]
        outcome = OUTCOMES[line[1]]

        part1_score += part1_you.points

        if part1_you.__gt__(opponent):
            part1_score += 6
        elif part1_you.__eq__(opponent):
            part1_score += 3

        if outcome == LOSE:
            part2_you = opponent.beats
        elif outcome == TIE:
            part2_you = opponent
            part2_score += 3
        elif outcome == WIN:
            part2_you = opponent.beats.beats
            part2_score += 6

        part2_score += part2_you.points

    print(f"Part 1: {part1_score}\nPart 2: {part2_score}")
