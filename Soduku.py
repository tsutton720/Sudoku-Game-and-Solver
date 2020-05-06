
import random
import copy
import Solver


def createCandidates():

    size = 9
    candidates = []
    for i in range(size):
        candidates.append(i + 1)

    random.shuffle(candidates)
    return candidates


def makeAnswer(size=9):
    board = [[0] * size for i in range(size)]
    can = createCandidates()
    counter = 0

    for i in range(3):
        for j in range(3):
            board[counter] = can[:]

            counter += 1

            first3 = can[0:3]
            del can[0:3]
            can.extend(first3)

        first = can[0]
        del can[0]
        can.append(first)

    return board


def makeGameBoard(bo):
    gb = copy.deepcopy(bo)

    for i in range(9):
        rand = random.randint(5, 7)
        for j in range(rand):
            location = random.randint(0, 8)
            value = 0
            gb[i][location] = value
    return gb

# TODO Randomize board even more swap 3x3 left-right or up-down - should perserve soduku rules
