# --- Day 10: Cathode-Ray Tube ---
# You avoid the ropes, plunge into the river, and swim to shore.

# The Elves yell something about meeting back up with them upriver, but the
# river is too loud to tell exactly what they're saying. They finish crossing
# the bridge and disappear from view.

# Situations like this must be why the Elves prioritized getting the
# communication system on your handheld device working. You pull it out of your
# pack, but the amount of water slowly draining from a big crack in its screen
# tells you it probably won't be of much immediate use.

# Unless, that is, you can design a replacement for the device's video system!
# It seems to be some kind of cathode-ray tube screen and simple CPU that are
# both driven by a precise clock circuit. The clock circuit ticks at a constant
# rate; each tick is called a cycle.

# Start by figuring out the signal being sent by the CPU. The CPU has a single
# register, X, which starts with the value 1. It supports only two instructions:

# addx V takes two cycles to complete. After two cycles, the X register is
# increased by the value V. (V can be negative.)
# noop takes one cycle to complete. It has no other effect.
# The CPU uses these instructions in a program (your puzzle input) to, somehow,
# tell the screen what to draw.

# Consider the following small program:

# noop
# addx 3
# addx -5
# Execution of this program proceeds as follows:

# At the start of the first cycle, the noop instruction begins execution.
# During the first cycle, X is 1. After the first cycle, the noop instruction
# finishes execution, doing nothing.
# At the start of the second cycle, the addx 3 instruction begins execution.
# During the second cycle, X is still 1.
# During the third cycle, X is still 1. After the third cycle, the addx 3
# instruction finishes execution, setting X to 4.
# At the start of the fourth cycle, the addx -5 instruction begins execution.
# During the fourth cycle, X is still 4.
# During the fifth cycle, X is still 4. After the fifth cycle, the addx -5
# instruction finishes execution, setting X to -1.
# Maybe you can learn something by looking at the value of the X register
# throughout execution. For now, consider the signal strength (the cycle number
# multiplied by the value of the X register) during the 20th cycle and every 40
# cycles after that (that is, during the 20th, 60th, 100th, 140th, 180th, and
# 220th cycles).

def load_input(file_path):
    """
    Load the input file to get the cycle instructions.

    Inputs:
        file_path (str): file path where the input is located

    Returns:
        (lst) a list of tuples representing the cycle instructions
    """

    instructions = []

    with open(file_path, "r") as file:
        for line in file:
            instructions.append(line.strip("\n").split())

    return instructions


def get_signal_strength(instructions, to_sum=[20, 60, 100, 140, 180, 220]):
    """
    Calculate the sum of the signal strengths at the specified cycles.

    Inputs:
        instructions (list): list of signal instructions, either "noop" or "addx"
        to_sum (list): cycles during which to generate sum of signal strength

    Returns:
        (int): sum of signal strenghts at specified cycles.
    """

    cycle = 1
    sum_cycle_strength = 0
    x = 1

    for instruction in instructions:
        if instruction[0] == 'noop':
            num_cycles = 1
        else:
            num_cycles = 2

        for i in range(num_cycles):
            if cycle in to_sum:
                sum_cycle_strength += cycle * x

            if i == 1:
                x += int(instruction[1])
            cycle += 1

    return sum_cycle_strength

# --- Part Two ---
# It seems like the X register controls the horizontal position of a sprite.
# Specifically, the sprite is 3 pixels wide, and the X register sets the
# horizontal position of the middle of that sprite. (In this system, there is
# no such thing as "vertical position": if the sprite's horizontal position
# puts its pixels where the CRT is currently drawing, then those pixels will
# be drawn.)

# You count the pixels on the CRT: 40 wide and 6 high. This CRT screen draws
# the top row of pixels left-to-right, then the row below that, and so on.
# The left-most pixel in each row is in position 0, and the right-most pixel
# in each row is in position 39.

# Like the CPU, the CRT is tied closely to the clock circuit: the CRT draws a
# single pixel during each cycle. Representing each pixel of the screen as a #,
# here are the cycles during which the first and last pixel in each row are
# drawn:

# Cycle   1 -> ######################################## <- Cycle  40
# Cycle  41 -> ######################################## <- Cycle  80
# Cycle  81 -> ######################################## <- Cycle 120
# Cycle 121 -> ######################################## <- Cycle 160
# Cycle 161 -> ######################################## <- Cycle 200
# Cycle 201 -> ######################################## <- Cycle 240
# So, by carefully timing the CPU instructions and the CRT drawing operations,
# you should be able to determine whether the sprite is visible the instant each
# pixel is drawn. If the sprite is positioned such that one of its three pixels
# is the pixel currently being drawn, the screen produces a lit pixel (#);
# otherwise, the screen leaves the pixel dark (.).
# Render the image given by your program. What eight capital letters appear on
# your CRT?


def get_sprite_position(instructions):
    """
    Generate CRT image of sprite.

    Inputs:
        instructions (list): list of signal instructions, either "noop" or "addx"

    Outputs:
        (list of lists): CRT image of sprite; also outputs a .txt file with 
            chars representing the sprite image
    """

    lit_pixels = []
    crt = []
    cur_row = []
    x = 1
    pos = 0

    for instruction in instructions:
        if instruction[0] == 'noop':
            num_cycles = 1
        else:
            num_cycles = 2

        for i in range(num_cycles):
            if pos in [x-1, x, x+1]:
                cur_row.append(pos)

            if i == 1:
                inc = int(instruction[1])
                x += inc
            pos += 1

            if pos >= 40:
                pos = 0
                lit_pixels.append(cur_row)
                cur_row = []

    for line in lit_pixels:
        crt.append(['#' if n in line else '.' for n in range(40)])

    with open("data/day10-output.txt", "w") as f:
        for line in crt:
            for l in line:
                f.write(l)
            f.write("\n")

    return crt


# SOLVE ADVENT CHALLENG
def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    file_path = "data/day10-input.txt"
    instructions = load_input(file_path)

    # Part 1 - get sum of signal strength during 20th, 60th, 100th,
    # 140th, 180th cycles
    print(get_signal_strength(instructions))

    # Part 2 - render CRT image
    print(get_sprite_position(instructions))
