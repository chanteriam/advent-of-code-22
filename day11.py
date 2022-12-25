# --- Day 11: Monkey in the Middle ---
# As you finally start making your way upriver, you realize your pack is much
# lighter than you remember. Just then, one of the items from your pack goes
# flying overhead. Monkeys are playing Keep Away with your missing things!

# To get your stuff back, you need to be able to predict where the monkeys will
# throw your items. After some careful observation, you realize the monkeys
# operate based on how worried you are about each item.

# You take some notes (your puzzle input) on the items each monkey currently has,
# how worried you are about those items, and how the monkey makes decisions
# based on your worry level. For example:

# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3

# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0

# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3

# Monkey 3:
#   Starting items: 74
#   Operation: new = old + 3
#   Test: divisible by 17
#     If true: throw to monkey 0
#     If false: throw to monkey 1
# Each monkey has several attributes:

# Starting items lists your worry level for each item the monkey is currently
# holding in the order they will be inspected.
# Operation shows how your worry level changes as that monkey inspects an item.
# (An operation like new = old * 5 means that your worry level after the monkey
# inspected the item is five times whatever your worry level was before
# inspection.)
# Test shows how the monkey uses your worry level to decide where to throw an
# item next.
# If true shows what happens with an item if the Test was true.
# If false shows what happens with an item if the Test was false.
# After each monkey inspects an item but before it tests your worry level, your
# relief that the monkey's inspection didn't damage the item causes your worry
# level to be divided by three and rounded down to the nearest integer.

# The monkeys take turns inspecting and throwing items. On a single monkey's
# turn, it inspects and throws all of the items it is holding one at a time and
# in the order listed. Monkey 0 goes first, then monkey 1, and so on until each
# monkey has had one turn. The process of each monkey taking a single turn is
# called a round.

# When a monkey throws an item to another monkey, the item goes on the end of
# the recipient monkey's list. A monkey that starts a round with no items could
# end up inspecting and throwing many items by the time its turn comes around.
# If a monkey is holding no items at the start of its turn, its turn ends.
# Chasing all of the monkeys at once is impossible; you're going to have to
# focus on the two most active monkeys if you want any hope of getting your
# stuff back. Count the total number of times each monkey inspects items over
# 20 rounds:

# Monkey 0 inspected items 101 times.
# Monkey 1 inspected items 95 times.
# Monkey 2 inspected items 7 times.
# Monkey 3 inspected items 105 times.
# In this example, the two most active monkeys inspected items 101 and 105
# times. The level of monkey business in this situation can be found by
# multiplying these together: 10605.

# Figure out which monkeys to chase by counting how many items they inspect over
# 20 rounds. What is the level of monkey business after 20 rounds of
# stuff-slinging simian shenanigans?
import copy


class Monkey:
    """
    Provides implementation of a Monkey class.

    Attributes:
        id (int): the monkey's number or id
        items_held (list): list of items the monkey is currently holding
        num_inspections (int): the number of times a monkey has inspected items
    """

    def __init__(self, id, start_items, operation, test, throw_to):
        """
        Instantiates a Monkey object.

        InputsL
            id (int): the monkey's ID number
            start_items (list): the list of items the monkeys starts out holding
            operation (str): the operation a monkey performs on a given item
            test (int): int to divide item by to test which monkey to throw to
                next
            throw_to (list): list of monkeys to throw tested items to
        """

        self.id = id
        self.items = start_items
        self.op = operation
        self.t = test
        self.throw_to = copy.deepcopy(throw_to)
        self.num_inspections = 0

    def operation(self):
        """
        Conducts a monkey's inspection operation on an item.
        """

        self.num_inspections += 1
        old = self.items[0]
        self.items[0] = eval(self.op)

    def test(self, monkeys):
        """
        Tests whether the current item is divisible by the test int t to
            determine the monkey to throw the item to

        Inputs:
            monkeys (list): list of potential monkeys to throw the item to
        """

        if self.has_items():
            append = 0
            if self.items[0] % self.t != 0:
                append = 1

            for monkey in monkeys:

                # throwing current item to another monkey
                if monkey.id == self.throw_to[append]:
                    monkey.items.append(self.items.pop(0))
                    break

    def has_items(self):
        """
        Determines if a monkey currently holds any items

        Returns:
            (bool): true if the monkey holds items, false otherwise
        """

        return len(self.items) > 0

    def __repr__(self):
        """
        Overwrites default string representation of a Monkey object.

        Returns:
            (str): string representation of a monkey object
        """
        s = "Monkey: {}\n".format(self.id)
        s += "Total number of inspections: {}\n".format(self.num_inspections)
        s += "Items Held: {}\n".format(self.items)
        return s

    def relief(self):
        """
        Divides item worry level by 3.
        """

        self.items[0] = self.items[0] // 3


def load_input(file_path):
    """
    Loads in input of Monkeys and their attributes.

    Inputs:
        file_path (str): file path where the input file is located

    Returns:
        (list): list of Monkey objects
    """

    monkeys = []
    start_items = []
    throw_to = []
    operation = ''
    id = 0
    test = 1

    with open(file_path, "r") as file:
        for line in file:
            if line == "\n":
                monk = Monkey(id, start_items, operation, test, throw_to)
                monkeys.append(monk)
                operation = ''
                throw_to = []

            # get the monkey id
            elif "Monkey" in line:
                id = int(line.split()[-1][0:-1])

            # get the items the money has
            elif "Starting items" in line:
                start_items = line.replace(",", "").split()[2:]
                for i, it in enumerate(start_items):
                    start_items[i] = int(it)

            # get the monkey's worry operation
            elif "Operation" in line:
                operation = operation.join(line.split()[3:])

            # get the test case
            elif "Test" in line:
                test = int(line.split()[-1])

            # get monkeys to throw to
            else:
                throw_to.append(int(line.split()[-1]))

    monk = Monkey(id, start_items, operation, test, throw_to)
    monkeys.append(monk)
    return monkeys


def get_monkey_business(monkeys, r=20, k=2, relief=True):
    """
    Determines the top k monkeys with the most inspections after number of 
        r rounds and calculates their monkey business score

    Inputs:
        monkeys (list): list of monkeys
        r (int): number of rounds to play
        k (int): top k number of monkeys to return

    Returns:
        (int) the total of monkey business, calculated by multiplying the total
            number of inspections the top k monkeys conducted over the course of
            r rounds
    """

    round = 0
    monkey_business = 1
    while round < r:
        round += 1
        for monkey in monkeys:
            while monkey.has_items():
                # monkey inspects current item
                monkey.operation()

                # monkey gets bored with current item
                if relief:
                    monkey.relief()

                # monkey conducts operation on current item
                monkey.test(monkeys)

    monkeys.sort(key=lambda monkey: monkey.num_inspections, reverse=True)

    for monkey in monkeys[:k]:
        monkey_business *= monkey.num_inspections

    return monkey_business


# SOLVE ADVENT CHALLENGES
def main():
    """
     Calls relevant functions for solving advent calendar problems

     Return:
         Outcomes for parts 1 and 2
     """

    file_path = "data/day11-input.txt"
    monkeys = load_input(file_path)

    # Part 1 - Calculate monkey business
    print(get_monkey_business(monkeys))
