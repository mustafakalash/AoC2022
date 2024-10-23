import math

ROUNDS = 10000
RELIEF = False
monkeys = []
worry_divisor = 1

class Monkey:
    def __init__(self, items, operation, divisor, true_monkey, false_monkey):
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.outcomes = {True: true_monkey, False: false_monkey}
        self.inspections = 0

    def test(self, worry):
        test = self.outcomes[worry % self.divisor == 0]
        return test
    
    def operate(self, worry):
        worry = eval(self.operation)
        if RELIEF:
            worry = worry // 3
        else:
            worry %= worry_divisor

        return worry

    def inspect(self):
        while len(self.items):
            worry = self.items.pop(0)
            worry = self.operate(worry)
            target_monkey = self.test(worry)
            monkeys[target_monkey].items.append(worry)
            self.inspections += 1
        

with open("11/input", "r", encoding = "UTF-8") as f:
    lines = list(f)
    while len(lines):
        lines.pop(0)
        items = list(map(int, lines.pop(0).split(":")[1].strip().split(",")))
        operation = lines.pop(0).split(":")[1].strip().split("=")[1].replace("old", "worry")
        divisor = int(lines.pop(0).split("by")[1].strip())
        worry_divisor *= divisor
        true_monkey = int(lines.pop(0).split("monkey")[1].strip())
        false_monkey = int(lines.pop(0).split("monkey")[1].strip())
        monkeys.append(Monkey(items, operation, divisor, true_monkey, false_monkey))

        if(len(lines)):
            lines.pop(0)
    
    for i in range(ROUNDS):
        for monkey in monkeys:
            monkey.inspect()

    monkeys.sort(key = lambda monkey: monkey.inspections, reverse=True)

    print(monkeys[0].inspections * monkeys[1].inspections)