import itertools
import copy

SPACE_BETWEEN_CRATES = 4
CRATE_START = 1
AMOUNT_INDEX = 1
FROM_INDEX = 3
TO_INDEX = 5

def display_crates(c):
    c = list(itertools.zip_longest(*c))
    c.reverse()
    for row in c:
        for crate in row:
            if crate:
                print(f"[{crate}]", end=" ")
            else:
                print(" " * (SPACE_BETWEEN_CRATES - 1), end=" ")
        print()

with open("5/input", "r") as f:
    crates = list()
    p2_crates = list()

    lines = f.readlines()
    for i in range(len(lines[0]) // SPACE_BETWEEN_CRATES):
        crates.append(list())

    all_crates_loaded = False
    for line in lines:
        if not all_crates_loaded:
            for i in range(CRATE_START, len(line), SPACE_BETWEEN_CRATES):
                if line.strip()[0].isdigit():
                    all_crates_loaded = True
                    break
                if not line[i].isspace():
                    crates[(i - CRATE_START) // SPACE_BETWEEN_CRATES].insert(0, line[i])
        else:
            if line.isspace():
                p2_crates = copy.deepcopy(crates)
                continue

            line = line.split(" ")
            amount = int(line[AMOUNT_INDEX])
            from_stack = int(line[FROM_INDEX]) - 1
            to_stack = int(line[TO_INDEX]) - 1

            for i in range(amount):
                crates[to_stack].append(crates[from_stack].pop())

            p2_crates[to_stack] += p2_crates[from_stack][-amount:]
            del p2_crates[from_stack][-amount:]

    display_crates(crates)
    print("-" * len(lines[0]))
    display_crates(p2_crates)
