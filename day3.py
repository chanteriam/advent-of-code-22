# --- Day 3: Rucksack Reorganization ---
# One Elf has the important job of loading all of the rucksacks with supplies for
# the jungle journey. Unfortunately, that Elf didn't quite follow the packing
# instructions, and so a few items now need to be rearranged.

# Each rucksack has two large compartments. All items of a given type are meant
# to go into exactly one of the two compartments. The Elf that did the packing
# failed to follow this rule for exactly one item type per rucksack.

# The Elves have made a list of all of the items currently in each rucksack
# (your puzzle input), but they need your help finding the errors. Every item
# type is identified by a single lowercase or uppercase letter (that is, a and
# A refer to different types of items).

# The list of items for each rucksack is given as characters all on a single
# line. A given rucksack always has the same number of items in each of its
# two compartments, so the first half of the characters represent items in the
# first compartment, while the second half of the characters represent items in
# the second compartment.

# For example, suppose you have the following list of contents from six rucksacks:
# vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw

# The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means
# its first compartment contains the items vJrwpWtwJgWr, while the second
# compartment contains the items hcsFMMfFFhFp. The only item type that appears
# in both compartments is lowercase p.
# The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL.
# The only item type that appears in both compartments is uppercase L.
# The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only
# common item type is uppercase P.
# The fourth rucksack's compartments only share item type v.
# The fifth rucksack's compartments only share item type t.
# The sixth rucksack's compartments only share item type s.
# To help prioritize item rearrangement, every item type can be converted to a
# priority:

# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.
# In the above example, the priority of the item type that appears in both
# compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t),
# and 19 (s); the sum of these is 157.

# Find the item type that appears in both compartments of each rucksack.
# What is the sum of the priorities of those item types?

import string


class Rucksack:
    """
    Simple class for representing a rucksack.
    """

    def __init__(self, contents=""):
        """
        Contructs a new rucksack.

        Inputs:
            contents (str): the contents of the Rucksack
        """
        self.first_compartment = contents[:len(contents)//2]
        self.second_compartment = contents[len(contents)//2:]

    def find_duplicates(self):
        """
        Finds items that are duplicated across both compartments.

        Returns:
            (set): duplicate items
        """

        duplicates = set()

        for item in self.first_compartment:
            if item in self.second_compartment:
                duplicates.add(item)

        return duplicates

    def __repr__(self):
        """
        Defines print representation of rucksack object.
        """

        s = "First Compartment: " + str(self.first_compartment) + "\n"
        s += "Second Compartment: " + str(self.second_compartment)

        return s


def load_rucksacks(file_path):
    """
    Generate a list of rucksack objects from .txt file.

    Inputs:
        file_path (str): filepath for the rucksack data

    Returns:
        (list): list of rucksack objects
    """

    rucksacks = []
    with open(file_path, "r") as rs:
        for line in rs:
            rucksacks.append(Rucksack(line))

    return rucksacks


def get_score(str):
    """
    Calculates score of items, where score is determined by alphabetic
        characters in string: lower case characters have scores 1-26, upper case
        characters have scores 27-52

    Input:
        str (string): the string to generate score of

    Return:
        (int): calculated score
    """

    LOWER = list(string.ascii_lowercase)
    UPPER = list(string.ascii_uppercase)
    ALPHABET = LOWER + UPPER
    SCORES = [i for i in range(1, 53)]

    score = 0
    for character in str:
        score += SCORES[ALPHABET.index(character)]

    return score


# --- Part Two ---
# As you finish identifying the misplaced items, the Elves come to you with
# another issue.

# For safety, the Elves are divided into groups of three. Every Elf carries a
# badge that identifies their group. For efficiency, within each group of three
# Elves, the badge is the only item type carried by all three Elves. That is,
# if a group's badge is item type B, then all three Elves will have item type B
# somewhere in their rucksack, and at most two of the Elves will be carrying any
# other item type.

# The problem is that someone forgot to put this year's updated authenticity
# sticker on the badges. All of the badges need to be pulled out of the
# rucksacks so the new authenticity stickers can be attached.

# Additionally, nobody wrote down which item type corresponds to each group's
# badges. The only way to tell which item type is the right one is by finding
# the one item type that is common between all three Elves in each group.

# Every set of three lines in your list corresponds to a single group, but each
# group can have a different badge item type. So, in the above example, the
# first group's rucksacks are the first three lines:

# vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# And the second group's rucksacks are the next three lines:

# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw
# In the first group, the only item type that appears in all three rucksacks is
# lowercase r; this must be their badges. In the second group, their badge item
# type must be Z.

# Priorities for these items must still be found to organize the sticker
# attachment efforts: here, they are 18 (r) for the first group and 52 (Z)
# for the second group. The sum of these is 70.

# Find the item type that corresponds to the badges of each three-Elf group.
# What is the sum of the priorities of those item types?

def define_groups(file_path, k=3):
    """
    Splits rucksacks into groups of size k.

    Inputs:
        file_path (str): filepath for the rucksack data
        k (int): size of the group

    Returns:
        (list): list of tuples containing groups of rucksacks
    """

    rucksacks = load_rucksacks(file_path)
    groups = [tuple(rucksacks[i:i+k]) for i in range(0, len(rucksacks), k)]
    return groups


def find_badge(rucksack_groups):
    """
    Finds common items across each group of rucksacks.

    Inputs:
        rucksack_groups (list): a list of tuple rucksack groups of equal size

    Returns:
        (list): badges corresponding to each rucksack group, where a badge is
            determine by a shared valued across each rucksack in a given group
    """
    pass


# SOLVE ADVENT CHALLENGE
def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    # Part 1 - get duplicates score
    file_path = "data/day3-input.txt"
    rucksacks = load_rucksacks(file_path)
    duplicate_score = 0

    for rucksack in rucksacks:
        duplicates = "".join(rucksack.find_duplicates())
        duplicate_score += get_score(duplicates)

    print(duplicate_score)
