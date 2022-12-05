# --- Day 5: Supply Stacks ---
# The expedition can depart as soon as the final supplies have been unloaded
# from the ships. Supplies are stored in stacks of marked crates, but because
# the needed supplies are buried under many other crates, the crates need
# to be rearranged.

# The ship has a giant cargo crane capable of moving crates between stacks.
# To ensure none of the crates get crushed or fall over, the crane operator
# will rearrange them in a series of carefully-planned steps. After the crates
# are rearranged, the desired crates will be at the top of each stack.

# The Elves don't want to interrupt the crane operator during this delicate
# procedure, but they forgot to ask her which crate will end up where, and
# they want to be ready to unload them as soon as possible so they can embark.

# They do, however, have a drawing of the starting stacks of crates and the
# rearrangement procedure (your puzzle input). For example:

#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3

# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2
# In this example, there are three stacks of crates. Stack 1 contains two
# crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains
# three crates; from bottom to top, they are crates M, C, and D. Finally,
# stack 3 contains a single crate, P.

# Then, the rearrangement procedure is given. In each step of the procedure,
# a quantity of crates is moved from one stack to a different stack. In the
# first step of the above rearrangement procedure, one crate is moved from
# stack 2 to stack 1, resulting in this configuration:

# [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3
# In the second step, three crates are moved from stack 1 to stack 3. Crates
# are moved one at a time, so the first crate to be moved (D) ends up below
# the second and third crates:

#         [Z]
#         [N]
#     [C] [D]
#     [M] [P]
#  1   2   3
# Then, both crates are moved from stack 2 to stack 1. Again, because crates
# are moved one at a time, crate C ends up below crate M:

#         [Z]
#         [N]
# [M]     [D]
# [C]     [P]
#  1   2   3
# Finally, one crate is moved from stack 1 to stack 2:

#         [Z]
#         [N]
#         [D]
# [C] [M] [P]
#  1   2   3
# The Elves just need to know which crate will end up on top of each stack;
# in this example, the top crates are C in stack 1, M in stack 2, and Z in
# stack 3, so you should combine these together and give the Elves the message CMZ.

# After the rearrangement procedure completes, what crate ends up on top of
# each stack?

def load_stacks(file_path):
    """
    Loads stack placement and movement instructions.

    Inputs:
        file_path (str): file path for input data

    Returns:
        (tuple): (list of stack placements, list of movement instructions)
    """

    # read the file into a list
    file = open(file_path, "r")
    placement_moves_lst = file.readlines()

    # remove line breaks
    for i, line in enumerate(placement_moves_lst):
        if line[-1] == "\n":
            placement_moves_lst[i] = line[:-1]

    # seperate moves from stack
    moves = stacks = []
    split_indx = placement_moves_lst.index('')
    stacks = placement_moves_lst[:split_indx]
    moves = placement_moves_lst[split_indx+1:]

    # get num stacks and remove stack col numbering
    stacks.reverse()  # reverse stacks
    num_stacks = int(stacks[0][-2])
    stacks.pop(0)

    # remove extraneous characters from stack list
    remove = [' ', '[', ']']

    # find indices for stack elements
    indices = []
    for i, elem in enumerate(stacks[0]):
        if elem not in remove:
            indices.append(i)

    # create list of list for stacks
    stacks_lst = [[] for _ in range(num_stacks)]
    for i, line in enumerate(stacks):
        for j in range(num_stacks):
            if (line[indices[j]] not in remove):
                stacks_lst[j] += line[indices[j]]

    # create list of lists for moves
    moves_lst = []
    for i, line in enumerate(moves):
        line_lst = line.split(" ")
        m = []
        for elem in line_lst:
            if elem.isnumeric():
                m.append(int(elem))
        moves_lst.append(m)

    file.close()
    return stacks_lst, moves_lst


def move_stack_items(file_path, cratemover9001=False):
    """
    Re-arrange stack items according to move strategy in input file.

    Inputs:
        file_path (str): file path for input data

    Return:
        (str): string containing all elements at the top of each stack
    """

    stacks, moves = load_stacks(file_path)

    # conduct strategic moves
    for move in moves:
        items, frm, to = move

        if (not cratemover9001):
            for _ in range(items):  # move x items
                elem = stacks[frm-1].pop()  # from this list
                stacks[to-1].append(elem)  # to this list

        else:
            elems = stacks[frm-1][-items:]  # move these elems
            stacks[frm-1] = stacks[frm-1][:-items]  # from this list
            stacks[to-1].extend(elems)  # to this list

    # get string of elements at the top of each stack
    stack_str = ""
    for stack in stacks:
        stack_str += str(stack[-1])

    return stack_str


# SOLVE ADVENT CHALLENGE
def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    file_path = ("data/day5-input.txt")

    # Part 1 - moving items one at a time from one stack to another
    print(move_stack_items(file_path))

    # Part 2 - move multiple items at a time from one stack to another
    print(move_stack_items(file_path, True))
