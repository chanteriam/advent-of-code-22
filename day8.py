# --- Day 8: Treetop Tree House ---
# The expedition comes across a peculiar patch of tall trees all planted
# carefully in a grid. The Elves explain that a previous expedition planted
# these trees as a reforestation effort. Now, they're curious if this would be
# a good location for a tree house.

# First, determine whether there is enough tree cover here to keep a tree house
# hidden. To do this, you need to count the number of trees that are visible
# from outside the grid when looking directly along a row or column.

# The Elves have already launched a quadcopter to generate a map with the height
# of each tree (your puzzle input). For example:

# 30373
# 25512
# 65332
# 33549
# 35390
# Each tree is represented as a single digit whose value is its height, where
# 0 is the shortest and 9 is the tallest.

# A tree is visible if all of the other trees between it and an edge of the
# grid are shorter than it. Only consider trees in the same row or column; that
# is, only look up, down, left, or right from any given tree.

# All of the trees around the edge of the grid are visible - since they are
# already on the edge, there are no trees to block the view. In this example,
# that only leaves the interior nine trees to consider:

# The top-left 5 is visible from the left and top. (It isn't visible from the
# right or bottom since other trees of height 5 are in the way.)
# The top-middle 5 is visible from the top and right.
# The top-right 1 is not visible from any direction; for it to be visible,
# there would need to only be trees of height 0 between it and an edge.
# The left-middle 5 is visible, but only from the right.
# The center 3 is not visible from any direction; for it to be visible, there
# would need to be only trees of at most height 2 between it and an edge.
# The right-middle 3 is visible from the right.
# In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
# With 16 trees visible on the edge and another 5 visible in the interior, a
# total of 21 trees are visible in this arrangement.

# Consider your map; how many trees are visible from outside the grid?

def load_input(file_path):
    """
    Load the input file to get the tree grid.

    Inputs:
        file_path (str): file path where the input is located

    Returns:
        (lst) a list of strings representing the tree grid
    """

    grid = []

    with open(file_path, "r") as f:
        for line in f:
            lst = []
            l = line.strip("\n")
            for num in l:
                lst.append(int(num))
            grid.append(lst)

    return grid


def calc_visible_trees(grid):
    """
    Determines number of trees that are visible at the edges of the forest.

    Inputs:
        grid (list): list of list, representing a grid of trees

    Returns:
        (int): count of visible trees
    """

    count = 0
    for i, row in enumerate(grid):
        if (i == 0) or (i == len(grid) - 1):  # outsice trees are visible
            count += len(row)
            continue

        for j, tree in enumerate(row):
            if (j == 0) or (j == len(row)-1):  # outer trees are visible
                count += 1
                continue

            visible = True

            # check left
            k = j-1
            while (visible and k >= 0):
                if grid[i][k] >= tree:
                    visible = False
                k -= 1

            if visible:
                count += 1
                continue

            # check right
            visible = True
            k = j+1
            while (visible and k < len(row)):
                if grid[i][k] >= tree:
                    visible = False
                k += 1

            if visible:
                count += 1
                continue

            # check up
            visible = True
            k = i-1
            while (visible and k >= 0):
                if grid[k][j] >= tree:
                    visible = False
                k -= 1

            if visible:
                count += 1
                continue

            # check down
            visible = True
            k = i+1
            while (visible and k < len(grid)):
                if grid[k][j] >= tree:
                    visible = False
                k += 1

            if visible:
                count += 1
                continue

    return count


# --- Part Two ---
# Content with the amount of tree cover available, the Elves just need to know
# the best spot to build their tree house: they would like to be able to see a
# lot of trees.

# To measure the viewing distance from a given tree, look up, down, left, and
# right from that tree; stop if you reach an edge or at the first tree that is
# the same height or taller than the tree under consideration. (If a tree is
# right on the edge, at least one of its viewing distances will be zero.)

# The Elves don't care about distant trees taller than those found by the rules
# above; the proposed tree house has large eaves to keep it dry, so they
# wouldn't be able to see higher than the tree house anyway.

# In the example above, consider the middle 5 in the second row:

# 30373
# 25512
# 65332
# 33549
# 35390
# Looking up, its view is not blocked; it can see 1 tree (of height 3).
# Looking left, its view is blocked immediately; it can see only 1 tree (of
# height 5, right next to it).
# Looking right, its view is not blocked; it can see 2 trees.
# Looking down, its view is blocked eventually; it can see 2 trees (one of
# height 3, then the tree of height 5 that blocks its view).
# A tree's scenic score is found by multiplying together its viewing distance in
# each of the four directions. For this tree, this is 4 (found by multiplying
# 1 * 1 * 2 * 2).

# However, you can do even better: consider the tree of height 5 in the middle
# of the fourth row:

# 30373
# 25512
# 65332
# 33549
# 35390
# Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
# Looking left, its view is not blocked; it can see 2 trees.
# Looking down, its view is also not blocked; it can see 1 tree.
# Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
# This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the
# tree house.

# Consider each tree on your map. What is the highest scenic score possible for
# any tree?

def calculate_max_scenic_score(grid):
    """
    Calculates the maximum scenic score of any tree in the grid.

    Inputs:
        grid (list): list of list, representing a grid of trees

    Returns:
        (int): maximum scenic score
    """

    max_score = 0

    for i, row in enumerate(grid):
        if (i == 0) or (i == len(grid)-1):  # edges will end up having a scenic score of 0
            continue

        for j, tree in enumerate(row):

            # edges will end up having a scenic score of 0
            if (j == 0) or (j == len(row) - 1):
                continue
            scores = []

            # check up
            count = 0
            k = i-1
            while (k >= 0):
                if grid[k][j] >= tree:
                    count += 1
                    break
                k -= 1
                count += 1
            scores.append(count)

            # check left:
            count = 0
            k = j-1
            while (k >= 0):
                if grid[i][k] >= tree:
                    count += 1
                    break
                k -= 1
                count += 1
            scores.append(count)

            # check right
            count = 0
            k = j+1
            while (k < len(row)):
                if grid[i][k] >= tree:
                    count += 1
                    break
                k += 1
                count += 1
            scores.append(count)

            # check down
            count = 0
            k = i+1
            while (k < len(grid)):
                if grid[k][j] >= tree:
                    count += 1
                    break
                k += 1
                count += 1
            scores.append(count)

            # get scenic score
            s = 1
            for score in scores:
                s *= score

            max_score = max(max_score, s)

    return max_score


# SOLVE ADVENT CHALLENGE
def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    file_path = "data/day8-input.txt"
    grid = load_input(file_path)

    # Part 1 - Calculate number of trees with visibility
    print(calc_visible_trees(grid))

    # Part 2 - Calculate maximum scenic score
    print(calculate_max_scenic_score(grid))
