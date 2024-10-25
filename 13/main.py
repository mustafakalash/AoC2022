from functools import cmp_to_key
from copy import deepcopy

DIVIDER_PACKETS = [[[2]], [[6]]]

def compare(a, b, depth = 0):
    print("\t" * (depth) + f"- Compare {a} vs {b}")

    #only one is a list
    if bool(isinstance(a, list)) is not bool(isinstance(b, list)):
        if isinstance(a, list):
            print("\t" * (depth + 1) + f"- Mixed types, convert right to [{b}] and retry comparison")
        else:
            print("\t" * (depth + 1) + f"- Mixed types, convert left to [{a}] and retry comparison")
        a = a if isinstance(a, list) else [a]
        b = b if isinstance(b, list) else [b]
        return compare(a, b, depth + 1)
    
    if isinstance(a, list) and isinstance(b, list):
        a = deepcopy(a)
        b = deepcopy(b)
        while len(a):
            if not len(b):
                print("\t" * (depth + 1) + "- Right side ran out of items, so inputs are not in the right order")
                return 1
            
            comparison = compare(a.pop(0), b.pop(0), depth + 1)
            if comparison is not 0:
                return comparison
            
        if len(b):
            print("\t" * (depth + 1) + "- Left side ran out of items, so inputs are in the right order")
            
        return -1 if len(b) else 0
    
    if a < b:
        print("\t" * (depth + 1) + "- Left side is smaller, so inputs are in the right order")
    elif a > b:
        print("\t" * (depth + 1) + "- Right side is smaller, so inputs are not in the right order")

    return 0 if a == b else -1 if a < b else 1

with open("13/input", "r", encoding="UTF-8") as f:
    pairs = []
    for line in f:
        if line is "\n":
            continue

        pairs.append(eval(line))

    for packet in DIVIDER_PACKETS:
        pairs.append(packet)
    
    pairs.sort(key=cmp_to_key(compare))

    key = 1
    for packet in DIVIDER_PACKETS:
        key *= pairs.index(packet) + 1

    print(key)