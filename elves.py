class Elf(object):
    """
    Simple class for representing Santa's elves.

    Attributes:
        [insert]
    """

    def __init__(self, calorie_lst=[], name="", ):
        """
        Contructs a new elf.

        Inputs:
            calories (int): the sum of calories a given elf is holding
            name (str): the elf's name
        """
        self.name = name
        self.total_calories = sum(calorie_lst)

    def __repr__(self):
        s = "Name: " + self.name + "\n"
        s += "Total Calories Held: " + str(self.total_calories) + "\n"
        return s
