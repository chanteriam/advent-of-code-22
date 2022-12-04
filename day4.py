# --- Day 4: Camp Cleanup ---
# Space needs to be cleared before the last supplies can be unloaded from the
# ships, and so several Elves have been assigned the job of cleaning up sections
# of the camp. Every section has a unique ID number, and each Elf is assigned a
# range of section IDs.

# However, as some of the Elves compare their section assignments with each other,
# they've noticed that many of the assignments overlap. To try to quickly find
# overlaps and reduce duplicated effort, the Elves pair up and make a big list
# of the section assignments for each pair (your puzzle input).

# For example, consider the following list of section assignment pairs:

# 2-4,6-8
# 2-3,4-5
# 5-7,7-9
# 2-8,3-7
# 6-6,4-6
# 2-6,4-8
# For the first few pairs, this list means:

# Within the first pair of Elves, the first Elf was assigned sections 2-4
# (sections 2, 3, and 4), while the second Elf was assigned sections 6-8
# (sections 6, 7, 8).
# The Elves in the second pair were each assigned two sections.
# The Elves in the third pair were each assigned three sections: one got sections
# 5, 6, and 7, while the other also got 7, plus 8 and 9.
# This example list uses single-digit section IDs to make it easier to draw;
# your actual list might contain larger numbers. Visually, these pairs of
# section assignments look like this:

# .234.....  2-4
# .....678.  6-8

# .23......  2-3
# ...45....  4-5

# ....567..  5-7
# ......789  7-9

# .2345678.  2-8
# ..34567..  3-7

# .....6...  6-6
# ...456...  4-6

# .23456...  2-6
# ...45678.  4-8
# Some of the pairs have noticed that one of their assignments fully
# contains the other. For example, 2-8 fully contains 3-7, and 6-6 is
# fully contained by 4-6. In pairs where one assignment fully contains
# the other, one Elf in the pair would be exclusively cleaning sections
# their partner will already be cleaning, so these seem like the most in
# need of reconsideration. In this example, there are 2 such pairs.

# In how many assignment pairs does one range fully contain the other?

def load_section_assignments(file_path):
    """
    Loads pair section assisngments.

    Inputs:
        file_path (str): file path for input data

    Returns:
        (list): list of tuples, where each tuple contains section assignments
            for the pairs
    """

    section_pairs = []
    with open(file_path, "r") as secs:
        for line in secs:
            pair = tuple(line.strip().split(","))
            section_pairs.append(pair)

    return section_pairs


def determine_paired_overlap(file_path):
    """
    Determines how many elf pairs have section overlaps.

    Inputs:
        file_path (str): file path for input data

    Returns:
        (int): count of pairs with overlaps
    """

    overlap_count = 0
    section_pairs = load_section_assignments(file_path)
    for pair in section_pairs:

        # split pair sections into seperate lists
        section1, section2 = pair_to_list(pair)

        # determine overlap
        if determine_subset(section1, section2):
            overlap_count += 1

    return overlap_count


def pair_to_list(pair):
    """
    Converts tuple section pairs to lists containing range of values.

    Inputs:
        pair (tuple): a pair containing string ranges, such as ("18-21", "6-9")

    Returns:
        (tuple): tuple containing expanded list ranges for pair.
    """

    p1, p2 = pair
    sec1_split = p1.split("-")
    sec2_split = p2.split("-")

    section1 = [i for i in range(
        int(sec1_split[0]), int(sec1_split[1]) + 1)]
    section2 = [i for i in range(
        int(sec2_split[0]), int(sec2_split[1]) + 1)]

    return section1, section2


def determine_subset(lst1, lst2):
    """
    Determine if there is overlap between two lists.

    Inputs:
        lst1 (list), lst2 (list): lists to determine overlap between

    Return:
        (bool) if one of the lists is a subset of another
    """

    if len(lst1) > len(lst2):
        if (set(lst2).issubset(set(lst1))):
            return True
    else:
        if (set(lst1).issubset(set(lst2))):
            return True

    return False


# --- Part Two ---
# It seems like there is still quite a bit of duplicate work planned. Instead,
# the Elves would like to know the number of pairs that overlap at all.

# In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap,
# while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8)
# do overlap:

# 5-7,7-9 overlaps in a single section, 7.
# 2-8,3-7 overlaps all of the sections 3 through 7.
# 6-6,4-6 overlaps in a single section, 6.
# 2-6,4-8 overlaps in sections 4, 5, and 6.
# So, in this example, the number of overlapping assignment pairs is 4.

# In how many assignment pairs do the ranges overlap?

def determine_overlap(lst1, lst2):
    """
    Determine if any shared elements between lst1 and lst2

    Inputs:
        lst1 (list), lst2 (list): lists to determine overlap between

    Return:
        (bool): if any overlap between two lists
    """

    for l in lst1:
        if l in lst2:
            return True

    return False


def determine_any_overlap(file_path):
    """
    Determines any overlap between section pairs for elves.
    
    Inputs:
        file_path (str): file path for input data

    Return:
        (int): count of pairs that have any overlap
    """

    overlap_count = 0
    section_pairs = load_section_assignments(file_path)

    # get list of all sections
    for pair in section_pairs:
        section1, section2 = pair_to_list(pair)
        if determine_overlap(section1, section2):
            overlap_count += 1

    return overlap_count


# SOLVE ADVENT CHALLENGE
def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    # Part 1 - determine complete overlap
    file_path = "data/day4-input.txt"
    print(determine_paired_overlap(file_path))

    # Part 2 - determine any overlap
    print(determine_any_overlap(file_path))
