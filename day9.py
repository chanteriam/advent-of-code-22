# --- Day 9: Rope Bridge ---
# This rope bridge creaks as you walk along it. You aren't sure how old it is,
# or whether it can even support your weight.

# It seems to support the Elves just fine, though. The bridge spans a gorge
# which was carved out by the massive river far below you.

# You step carefully; as you do, the ropes stretch and twist. You decide to
# distract yourself by modeling rope physics; maybe you can even figure out
# where not to step.

# Consider a rope with a knot at each end; these knots mark the head and the
# tail of the rope. If the head moves far enough away from the tail, the tail
# is pulled toward the head.

# Due to nebulous reasoning involving Planck lengths, you should be able to
# model the positions of the knots on a two-dimensional grid. Then, by following
# a hypothetical series of motions (your puzzle input) for the head, you can
# determine how the tail will move.

# Due to the aforementioned Planck lengths, the rope must be quite short; in
# fact, the head (H) and tail (T) must always be touching (diagonally adjacent
# and even overlapping both count as touching):

# ....
# .TH.
# ....

# ....
# .H..
# ..T.
# ....

# ...
# .H. (H covers T)
# ...
# If the head is ever two steps directly up, down, left, or right from the tail,
# the tail must also move one step in that direction so it remains close enough:

# .....    .....    .....
# .TH.. -> .T.H. -> ..TH.
# .....    .....    .....

# ...    ...    ...
# .T.    .T.    ...
# .H. -> ... -> .T.
# ...    .H.    .H.
# ...    ...    ...
# Otherwise, if the head and tail aren't touching and aren't in the same row or
# column, the tail always moves one step diagonally to keep up:

# .....    .....    .....
# .....    ..H..    ..H..
# ..H.. -> ..... -> ..T..
# .T...    .T...    .....
# .....    .....    .....

# .....    .....    .....
# .....    .....    .....
# ..H.. -> ...H. -> ..TH.
# .T...    .T...    .....
# .....    .....    .....
# You just need to work out where the tail goes as the head follows a series of
# motions. Assume the head and the tail both start at the same position,
# overlapping.

# For example:

# R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2
# This series of motions moves the head right four steps, then up four steps,
# then left three steps, then down one step, and so on. After each step, you'll
# need to update the position of the tail if the step means the head is no
# longer adjacent to the tail.

def load_input(file_path):

    movements = []

    with open(file_path, "r") as f:
        for line in f:
            move = tuple(line.strip("\n").split())
            movements.append(move)

    return movements


def move_knots(movements, knots=2):
    """
    Determine the number of locations tail visits in response to head's 
        movements

    Inputs:
        movements (list): list of directions and steps for heads to make

    Returns:
        count of positions tail visits at least once
    """

    knot_positions = [(0, 0)] * knots
    prev_positions = [(0, 0)] * knots
    tail_positions = {(0, 0)}

    for direction, steps in movements:
        for s in range(int(steps)):
            for i, knot in enumerate(knot_positions):

                # advance head knot step up, down, left, or right
                if (i == 0):
                    if direction == "R":
                        knot_positions[i] = prev_positions[i][0] + \
                            1, prev_positions[i][1]
                    elif direction == "L":
                        knot_positions[i] = prev_positions[i][0] - \
                            1, prev_positions[i][1]
                    elif direction == "U":
                        knot_positions[i] = prev_positions[i][0], prev_positions[i][1] + 1
                    else:
                        knot_positions[i] = prev_positions[i][0], prev_positions[i][1] - 1

                # advance current knot to position of prev
                else:
                    if not adjacent(knot_positions[i-1], knot):
                        if (move_diagonal(knot_positions[i-1], knot)):
                            knot_positions[i] = diagonal_move(
                                knot_positions[i-1], knot)
                        else:
                            knot_positions[i] = prev_positions[i-1]

                # is this the tail knot? - populate tail knot positions
                if (i+1) == knots:
                    tail_positions.add(knot_positions[i])

            for i, pos in enumerate(knot_positions):
                prev_positions[i] = pos

    return len(tail_positions)


def diagonal_move(knot_one, knot_two):
    new_x = knot_two[0]
    new_y = knot_two[1]

    if knot_one[0] > knot_two[0]:
        new_x += 1
    else:
        new_x -= 1

    if knot_one[1] > knot_two[1]:
        new_y += 1
    else:
        new_y -= 1

    return (new_x, new_y)


def adjacent(head, tail):
    """
    Determines if two points are adjacent to head other.

    Inputs:
        head (tuple): point 1
        tail (tuple): point 2

    Returns:
        (bool): True if the two points are adjacent
    """

    return (abs(head[0] - tail[0]) <= 1) and (abs(head[1] - tail[1]) <= 1)


def move_diagonal(head, tail):
    """
    Determines tail needs to move diagonally, defined as when tail and head
        and in both a different row and a different column.

    Inputs:
        head (tuple): point 1
        tail (tuple): point 2

    Returns:
        (bool): True if tail must move diagnoally 
    """

    return (abs(head[0] - tail[0]) > 0) and (abs(head[1] - tail[1]) > 0)


# --- Part Two ---
# A rope snaps! Suddenly, the river is getting a lot closer than you remember.
# The bridge is still there, but some of the ropes that broke are now whipping
# toward you as you fall through the air!

# The ropes are moving too quickly to grab; you only have a few seconds to
# choose how to arch your body to avoid being hit. Fortunately, your simulation
# can be extended to support longer ropes.

# Rather than two knots, you now must simulate a rope consisting of ten knots.
# One knot is still the head of the rope and moves according to the series of
# motions. Each knot further down the rope follows the knot in front of it using
# the same rules as before.
# Now, you need to keep track of the positions the new tail, 9, visits. In this
# example, the tail never moves, and so it only visits 1 position. However, be
# careful: more types of motion are possible than before, so you might want to
# visually compare your simulated rope to the one above.
# Simulate your complete series of motions on a larger rope with ten knots.
# How many positions does the tail of the rope visit at least once?


# SOLVE ADVENT CHALLENGES
def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    file_path = "data/day9-input.txt"
    movements = load_input(file_path)

    # Part 1 - number of unique tail movements
    print(move_knots(movements))

    # Part 2 - number of unique tail movements with 10 total knots
    print(move_knots(movements, 10))
