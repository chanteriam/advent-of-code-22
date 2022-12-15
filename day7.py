# --- Day 7: No Space Left On Device ---
# You can hear birds chirping and raindrops hitting leaves as the expedition
# proceeds. Occasionally, you can even hear much louder sounds in the distance;
# how big do the animals get out here, anyway?

# The device the Elves gave you has problems with more than just its
# communication system. You try to run a system update:

# $ system-update --please --pretty-please-with-sugar-on-top
# Error: No space left on device
# Perhaps you can delete some files to make space for the update?

# You browse around the filesystem to assess the situation and save the
# resulting terminal output (your puzzle input). For example:

# $ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k
# The filesystem consists of a tree of files (plain data) and directories
# (which can contain other directories or files). The outermost directory is
# called /. You can navigate around the filesystem, moving into or out of
# directories and listing the contents of the directory you're currently in.

# Within the terminal output, lines that begin with $ are commands you executed,
# very much like some modern computers:

# cd means change directory. This changes which directory is the current
# directory, but the specific result depends on the argument:
# cd x moves in one level: it looks in the current directory for the directory
# named x and makes it the current directory.
# cd .. moves out one level: it finds the directory that contains the current
# directory, then makes that directory the current directory.
# cd / switches the current directory to the outermost directory, /.
# ls means list. It prints out all of the files and directories immediately
# contained by the current directory:
# 123 abc means that the current directory contains a file named abc with
# size 123.
# dir xyz means that the current directory contains a directory named xyz.
# Given the commands and output in the example above, you can determine that
# the filesystem looks visually like this:

# - / (dir)
#   - a (dir)
#     - e (dir)
#       - i (file, size=584)
#     - f (file, size=29116)
#     - g (file, size=2557)
#     - h.lst (file, size=62596)
#   - b.txt (file, size=14848514)
#   - c.dat (file, size=8504156)
#   - d (dir)
#     - j (file, size=4060174)
#     - d.log (file, size=8033020)
#     - d.ext (file, size=5626152)
#     - k (file, size=7214296)
# Here, there are four directories: / (the outermost directory), a and d
# (which are in /), and e (which is in a). These directories also contain
# files of various sizes.

# Since the disk is full, your first step should probably be to find directories
# that are good candidates for deletion. To do this, you need to determine the
# total size of each directory. The total size of a directory is the sum of
# the sizes of the files it contains, directly or indirectly. (Directories
# themselves do not count as having any intrinsic size.)

# The total sizes of the directories above can be found as follows:

# The total size of directory e is 584 because it contains a single file i of
# size 584 and no other directories.
# The directory a has total size 94853 because it contains files f (size 29116),
# g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e
# which contains i).
# Directory d has total size 24933642.
# As the outermost directory, / contains every file. Its total size is 48381165,
# the sum of the size of every file.
# To begin, find all of the directories with a total size of at most 100000,
# then calculate the sum of their total sizes. In the example above, these
# directories are a and e; the sum of their total sizes is 95437 (94853 + 584).
# (As in this example, this process can count files more than once!)

# Find all of the directories with a total size of at most 100000. What is the
# sum of the total sizes of those directories?

from dir_structure import Directory
from dir_structure import File


def load_input(file_path):
    """
    Load the input commands.

    Inputs:
        file_path (str): the file path containing the input

    Returns:
        (Directory): directory structure
    """

    cur_dir = None
    cur_path = ""
    main_dir = None
    files = []

    with open(file_path, "r") as i:
        for line in i:

            # if the line if a command
            if "$" in line:

                # take all of the files from ls and add them to current directory
                if (len(files) > 0):
                    add_files(cur_dir, files)
                    files = []

                # if we're changing our current directory
                if "cd" in line:
                    dir_name = line.split()[-1]

                    # if we're moving back to the main directory
                    if (dir_name == "/"):
                        if main_dir == None:  # initializing the main directory
                            main_dir = Directory("Main")
                        cur_dir = main_dir
                        cur_path = "Main/"

                    # if we're moving back one level
                    elif dir_name == "..":

                        # an ugly way to get 1-level up path
                        cur_path = \
                            cur_path[:-1][::-1][cur_path[:-1]
                                                [::-1].index("/"):][::-1]
                        cur_dir = main_dir.get_directory(cur_path)

                    # if we're moving into a subdirectory
                    else:
                        cur_path += dir_name + "/"
                        cur_dir = main_dir.get_directory(cur_path)

            # take note of listed files
            else:
                files.append(line)

        if len(files) > 0:
            add_files(cur_dir, files)
    return main_dir


def add_files(directory, lst):
    """
    Populates a directory with File and Directory objects.

    Inputs:
        directory (Directory): directory object to populate
        lst (list): list of File and Directory objects to add to directory
    """

    for obj in lst:
        x, y = obj.split()

        if (x == "dir"):  # adding a directory
            directory.add_directory(Directory(y))

        else:  # adding a file
            directory.add_file(File(int(x), y))


def find_dir_size(directory, threshold=100000):
    """
    Finds the subdirectories with at most the size of the threshold, and sums
    these sizes.

    Inputs:
        directory (Directory): directory object to traverse
        threshold (int): max size of the subdirectories under consideration

    Returns:
        (int): sum of directory sizes, where sizes are >= threshold
    """

    sum = 0
    if directory.num_subdirectories() > 0:

        # recursively traverse subdirectories
        for d in directory.subdirectories:
            if d.get_size() <= threshold:
                sum += d.get_size()
            sum += find_dir_size(d, threshold)

    return sum


# --- Part Two ---
# Now, you're ready to choose a directory to delete.

# The total disk space available to the filesystem is 70000000. To run the
# update, you need unused space of at least 30000000. You need to find a
# directory you can delete that will free up enough space to run the update.

# In the example above, the total size of the outermost directory (and thus
# the total amount of used space) is 48381165; this means that the size of the
# unused space must currently be 21618835, which isn't quite the 30000000
# required by the update. Therefore, the update still requires a directory with
# total size of at least 8381165 to be deleted before it can run.

# To achieve this, you have the following options:

# Delete directory e, which would increase unused space by 584.
# Delete directory a, which would increase unused space by 94853.
# Delete directory d, which would increase unused space by 24933642.
# Delete directory /, which would increase unused space by 48381165.
# Directories e and a are both too small; deleting them would not free up enough
# space. However, directories d and / are both big enough! Between these, choose
# the smallest: d, increasing unused space by 24933642.

# Find the smallest directory that, if deleted, would free up enough space on
# the filesystem to run the update. What is the total size of that directory?

def find_dir_to_delete(directory, needed, cur):
    """
    Traverses the main directory to determine the smallest directory to delete
        in order to free up the space needed.

    Inputs:
        directory (Directory): the Directory object to traverse
        cur_unused (int): the current amount of unused space the current directory uses
        total_space (int): the total amount of space the drive can hold
        space_needed (int): the amount of free space needed

    Returns:
        (int): size of the smallest directory able to delete to free up the 
            space needed
    """
    if (directory.num_subdirectories() > 0):

        for d in directory.subdirectories:
            if d.get_size() >= needed and d.get_size() < cur:
                cur = d.get_size()

            cur = find_dir_to_delete(d, needed, cur)

    return cur

 # SOLVE ADVENT CHALLENGES


def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    file_path = "data/day7-input.txt"
    main = load_input(file_path)
    main.update_size()

    # Part 1 - total size of directories with size <= 100,000
    print(find_dir_size(main))

    # Part 2 - size of directory needed to delete
    total_disk_size = 70000000
    unused = total_disk_size - main.get_size()
    needed = 30000000 - unused
    print(find_dir_to_delete(main, needed, main.get_size()))
