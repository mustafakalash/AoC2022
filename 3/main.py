import string

with open("3/input", "r", encoding = "UTF-8") as f:
    priorities = string.ascii_lowercase + string.ascii_uppercase
    total_priority = 0
    total_badge_priority = 0

    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        compartment1 = line[:len(line)//2]
        compartment2 = line[len(line)//2:]

        doubleFound = False
        badgeFound = False
        for item in line:
            if item in compartment2 and not doubleFound:
                total_priority += priorities.index(item) + 1
                doubleFound = True

            if i % 3 == 2:
                if item in lines[i - 2] and item in lines[i - 1] and not badgeFound:
                    total_badge_priority += priorities.index(item) + 1
                    badgeFound = True

            if doubleFound and badgeFound:
                break

    print(total_priority)
    print(total_badge_priority)
