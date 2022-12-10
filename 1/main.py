import bisect

with open("1/input", "r", encoding = "UTF-8") as f:
    current_calories = 0
    calories = list()
    for line in f:
        try:
            current_calories += int(line)
        except ValueError:
            bisect.insort_right(calories, current_calories)
            current_calories = 0

    print(calories[-1])
    print(sum(calories[-3:]))
    