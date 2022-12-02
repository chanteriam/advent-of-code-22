# --- Day 2: Rock Paper Scissors ---
# The Elves begin to set up camp on the beach. To decide whose tent gets to be
# closest to the snack storage, a giant Rock Paper Scissors tournament is already
# in progress.

# Rock Paper Scissors is a game between two players. Each game contains many
# rounds; in each round, the players each simultaneously choose one of Rock,
# Paper, or Scissors using a hand shape. Then, a winner for that round is
# selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
# If both players choose the same shape, the round instead ends in a draw.

# Appreciative of your help yesterday, one Elf gives you an encrypted strategy
# guide (your puzzle input) that they say will be sure to help you win. "The
# first column is what your opponent is going to play: A for Rock, B for Paper,
# and C for Scissors. The second column--" Suddenly, the Elf is called away to
# help with someone's tent.

# The second column, you reason, must be what you should play in response: X for
# Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious,
# so the responses must have been carefully chosen.

# The winner of the whole tournament is the player with the highest score. Your
# total score is the sum of your scores for each round. The score for a single
# round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3
# for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if
# the round was a draw, and 6 if you won).

# Since you can't be sure if the Elf is trying to help you or trick you, you
# should calculate the score you would get if you were to follow the strategy
# guide.

# For example, suppose you were given the following strategy guide:

# A Y
# B X
# C Z
# This strategy guide predicts and recommends the following:

# In the first round, your opponent will choose Rock (A), and you should choose
# Paper (Y). This ends in a win for you with a score of 8 (2 because you chose
# Paper + 6 because you won).
# In the second round, your opponent will choose Paper (B), and you should choose
# Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
# The third round is a draw with both players choosing Scissors, giving you a
# score of 3 + 3 = 6.
# In this example, if you were to follow the strategy guide, you would get a
# total score of 15 (8 + 1 + 6).

# What would your total score be if everything goes exactly according to your
# strategy guide?

MOVES = ["rock", "paper", "scissor"]
OPPONENT_MOVES = ["A", "B", "C"]
YOUR_MOVES = ["X", "Y", "Z"]
SHAPE_SCORES = [1, 2, 3]
OUTCOMES = ["lost", "draw", "won"]
OUTCOME_SCORES = [0, 3, 6]


def get_strategy_guide(file_path):
    """
    Load strategy profile for each round of rock, paper, scissors

    Inputs:
        file_path (str): file path to input dataset

    Returns:
        (int, list): tuple containing the total number of rounds and
        list tuples for play strategy in each round of the game
    """

    strategies = []
    with open(file_path, "r") as strats:
        for line in strats:
            play = (tuple(line.replace(" ", "").strip()))
            strategies.append(play)

    return len(strategies), strategies


def get_total_score(file_path, part_one=True):
    """
    Using the strategy profile, calculates the total score one would get from
    following the profile.

    Inputs:
        file_path (str): file path to input dataset

    Returns:
        (int): total score player would receive from following strategy profile
    """

    _, strategies = get_strategy_guide(file_path)
    total_score = 0

    # find total score for the entire game
    for opponent, outcome in strategies:

        # determine if using strategy from part 1 or part 2
        if (part_one):
            player = determine_move(opponent, outcome)
        else:
            player = outcome

        _, round_score = determine_outcome(opponent, player)
        total_score += round_score

    return total_score


def determine_outcome(opponent_move, player_move):
    """
    Determine the outcome of one game of rock, paper, scissors.

    Inputs:
        opponent_move (str): the move the opponent makes, from ["A", "B", "C"],
            which corresponds with rock, paper, or scissors
        player_move (str): the move the players makes, from ["X", "Y", "Z"],
            which corresponds with rock, paper, or scissors

    Returns:
        (str, int): tuple containing outcome of round (lost, draw, won) and
            player score for the round
    """

    # Paper beats rock (paper > rock)
    # scissors beats paper (scissors > paper)
    # rock beats scissors (rock < scissors)
    OPPONENT_MOVES = ["A", "B", "C"]
    PLAYER_MOVES = ["X", "Y", "Z"]
    SHAPE_SCORES = [1, 2, 3]
    OUTCOMES = ["lost", "draw", "won"]
    OUTCOME_SCORES = [0, 3, 6]

    # Opponent plays rock
    opponent_idx = OPPONENT_MOVES.index(opponent_move)
    player_idx = PLAYER_MOVES.index(player_move)

    # it's a draw
    if (opponent_idx == player_idx):  # a draw
        return OUTCOMES[1], OUTCOME_SCORES[1] + SHAPE_SCORES[player_idx]

    # opponent plays rock
    if opponent_idx == 0:

        # player plays paper - win
        if player_idx == 1:
            return OUTCOMES[2], OUTCOME_SCORES[2] + SHAPE_SCORES[player_idx]

        # player plays scissors - lose
        if player_idx == 2:
            return OUTCOMES[0], OUTCOME_SCORES[0] + SHAPE_SCORES[player_idx]

    # opponent plays paper
    if opponent_idx == 1:

        # player plays rock - lose
        if player_idx == 0:
            return OUTCOMES[0], OUTCOME_SCORES[0] + SHAPE_SCORES[player_idx]

        # player plays scissors - win
        if player_idx == 2:
            return OUTCOMES[2], OUTCOME_SCORES[2] + SHAPE_SCORES[player_idx]

    # opponent plays scissors
    if opponent_idx == 2:

        # player plays rock - win
        if player_idx == 0:
            return OUTCOMES[2], OUTCOME_SCORES[2] + SHAPE_SCORES[player_idx]

        # player plays paper - lose
        if player_idx == 1:
            return OUTCOMES[0], OUTCOME_SCORES[0] + SHAPE_SCORES[player_idx]


# --- Part Two ---
# The Elf finishes helping with the tent and sneaks back over to you. "Anyway,
# the second column says how the round needs to end: X means you need to lose,
# Y means you need to end the round in a draw, and Z means you need to win. Good
# luck!"

# The total score is still calculated in the same way, but now you need to figure
# out what shape to choose so the round ends as indicated. The example above now
# goes like this:

# In the first round, your opponent will choose Rock (A), and you need the round
# to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
# In the second round, your opponent will choose Paper (B), and you choose Rock
# so you lose (X) with a score of 1 + 0 = 1.
# In the third round, you will defeat your opponent's Scissors with Rock for a
# score of 1 + 6 = 7.
# Now that you're correctly decrypting the ultra top secret strategy guide, you
# would get a total score of 12.

# Following the Elf's instructions for the second column, what would your total
# score be if everything goes exactly according to your strategy guide?

def determine_move(opponent, outcome):
    """
    Determine what move the player needs to make in response to the opponents
    move in order to ensure the given outcome.

    Inputs:
        opponent (str): the opponents move of rock, paper, or scissors
        outcome (str): what the outcome of the round needs to be - lose, draw,
            or win

    Return:
        (str): the move the player should make, i,e, rock ("X"), paper ("Y"), or
            scissors ("Z")
    """

    # X = lose, Y = draw, Z = win
    OPPONENT_MOVES = ["A", "B", "C"]
    PLAYER_MOVES = ["X", "Y", "Z"]

    # need a draw?
    if outcome == "Y":
        return PLAYER_MOVES[OPPONENT_MOVES.index(opponent)]

    # need to lose?
    if outcome == "X":

        # if opponent plays rock - play scissors
        if opponent == "A":
            return "Z"

        # if opponent plays paper - play rock
        if opponent == "B":
            return "X"

        # if opponent plays scissors - play paper
        if opponent == "C":
            return "Y"

    # need to win?
    if outcome == "Z":

        # if opponent plays rock - play paper
        if opponent == "A":
            return "Y"

        # if opponent plays paper - play scissors
        if opponent == "B":
            return "Z"

        # if opponent plays scissors - play rock
        if opponent == "C":
            return "X"


# SOLVE ADVENT CHALLENGES
def main():
    """
    Calls relevant functions for solving advent calendar problems

    Return:
        Outcomes for parts 1 and 2
    """

    file_path = "data/day2-input.txt"
    partone_score = get_total_score(file_path)
    parttwo_score = get_total_score(file_path, False)

    return partone_score, parttwo_score
