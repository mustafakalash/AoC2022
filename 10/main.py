class Command:
    ADD_COMMAND = "addx"
    NOOP_COMMAND = "noop"
    COMMAND_CYCLES = {
        ADD_COMMAND: 2,
        NOOP_COMMAND: 1
    }

    def __init__(self, command, argument = 0):
        self.command = command
        self.argument = int(argument)
        self.cycles = Command.COMMAND_CYCLES[command]

with open("10/input", "r", encoding = "UTF-8") as f:
    SIGNAL_CYCLE_START = 20
    SIGNAL_CYCLE_INCREMENT = 40

    PIXEL_WIDTH = 3
    SCREEN_WIDTH = 40

    commands = list()
    for line in f:
        line = line.strip().split(" ")
        commands.append(Command(*line))

    cycle = 1
    x = 1
    total_signal_value = 0
    row = ""
    while len(commands) > 0:
        if cycle % SCREEN_WIDTH in range(x, x + PIXEL_WIDTH):
            row += "#"
        else:
            row += "."

        if (cycle - SIGNAL_CYCLE_START) % SIGNAL_CYCLE_INCREMENT == 0:
            total_signal_value += cycle * x

        if cycle % SCREEN_WIDTH == 0:
            print(row)
            row = ""

        if commands[0].cycles == 1:
            x += commands[0].argument
            commands.pop(0)
        else:
            commands[0].cycles -= 1

        cycle += 1

    print(f"Total signal value: {total_signal_value}")
