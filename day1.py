# --- Day 1: Calorie Counting ---
# Santa's reindeer typically eat regular reindeer food, but they need a lot of
# magical energy to deliver presents on Christmas. For that, their favorite snack
# is a special type of star fruit that only grows deep in the jungle. The Elves
# have brought you on their annual expedition to the grove where the fruit grows.

# To supply enough magical energy, the expedition needs to retrieve a minimum of
# fifty stars by December 25th. Although the Elves assure you that the grove has
# plenty of fruit, you decide to grab any fruit you see along the way, just in case.

# Collect stars by solving puzzles. Two puzzles will be made available on each
# day in the Advent calendar; the second puzzle is unlocked when you complete
# the first. Each puzzle grants one star. Good luck!

# The jungle must be too overgrown and difficult to navigate in vehicles or
# access from the air; the Elves' expedition traditionally goes on foot. As your
# boats approach land, the Elves begin taking inventory of their supplies. One
# important consideration is food - in particular, the number of Calories each
# Elf is carrying (your puzzle input).

# The Elves take turns writing down the number of Calories contained by the
# various meals, snacks, rations, etc. that they've brought with them, one item
# per line. Each Elf separates their own inventory from the previous Elf's
# inventory (if any) by a blank line.

import elves


# --- PART ONE ---
# Find the Elf carrying the most Calories. How many total Calories is
# that Elf carrying?

def create_elves(file_path):
    """
    Creates a list of elves based on calorie file path input

    Inputs:
        file_path (str): file path for data listing calories held

    Returns: (lst) list of Elf objects
    """

    elf_lst = []
    cals = []

    # split elves based on calorie file line breaks
    with open(file_path, "r") as calories:
        for line in calories:

            # splitting based on calorie groupings in txt for each elf
            if line == "\n":
                elf_lst.append(elves.Elf(cals))
                cals = []
                continue

            cals.append(int(line))
    return elf_lst


def find_max_calories(file_path):
    """
    Finds the elf carrying the max number of calories.

    Inputs:
        file_path (str): file path for data listing calories held

    Returns: (int) max calories held by one elf
    """

    elf_lst = create_elves(file_path)
    sort_elves(elf_lst)
    return elf_lst[0].total_calories


# --- PART TWO ---
# By the time you calculate the answer to the Elves' question, they've already
# realized that the Elf carrying the most Calories of food might eventually run
# out of snacks.

# To avoid this unacceptable situation, the Elves would instead like to know the
# total Calories carried by the top three Elves carrying the most Calories. That
# way, even if one of those Elves runs out of snacks, they still have two backups.

# In the example above, the top three Elves are the fourth Elf (with 24000 Calories),
# then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories).
# The sum of the Calories carried by these three elves is 45000.

# Find the top three Elves carrying the most Calories. How many Calories are those
# Elves carrying in total?

def find_top_elves(file_path, k=3):
    """
    Find the top k elves holding the most calories.

    Input:
        file_path (str): file path for data listing calories held
        k (int): number of top elves to return

    Returns: (list) list of top k calories elves are carrying
        if k > total number of elves, returns all calories
    """

    elf_lst = create_elves(file_path)
    sort_elves(elf_lst)

    return elf_lst[:k]


def sort_elves(elf_lst):
    """
    Sorts elves from most to least calories helpd.

    Input:
        elf_lst (list): a list of Elf objects
    """

    elf_lst.sort(reverse=True, key=lambda elf: elf.total_calories)


def sum_elves(elf_lst):
    """
    Finds the total calories held by all elves in the elf list
    """

    total = sum([elf.total_calories for elf in elf_lst])
    return total


# SOLVE ADVENT CHALLENGES
def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    # Part 1 - get max calories
    file_path = "data/day1-input.txt"
    top_calories = find_max_calories(file_path)

    # Part 2 - find sum of top 3 calories
    top3 = sum_elves(find_top_elves(file_path))

    return top_calories, top3
