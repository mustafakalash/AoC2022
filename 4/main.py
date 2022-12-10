with open("4/input", "r", encoding = "UTF-8") as f:
    total_full_overlaps = 0
    total_partial_overlaps = 0
    for line in f:
        line = line.strip()
        ranges = line.split(",")
        elf1 = ranges[0].split("-")
        elf2 = ranges[1].split("-")
        if int(elf1[0]) >= int(elf2[0]) and int(elf1[0]) <= int(elf2[1]) \
                or int(elf2[0]) >= int(elf1[0]) and int(elf2[0]) <= int(elf1[1]):
            total_partial_overlaps += 1
        if int(elf1[0]) >= int(elf2[0]) and int(elf1[1]) <= int(elf2[1]) \
                or int(elf2[0]) >= int(elf1[0]) and int(elf2[1]) <= int(elf1[1]):
            total_full_overlaps += 1

    print(total_full_overlaps)
    print(total_partial_overlaps)
        