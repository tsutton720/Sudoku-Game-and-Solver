
import pygame
import Soduku
import inspect

# returns index of an empty space


def findEmpty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row column

    return None


def checkValid(board, number, position):
    # check Row
    for i in range(len(board[0])):
        if board[position[0]][i] == number and i != position[1]:
            return False

    # ckeck Row
    for i in range(len(board)):
        if board[i][position[1]] == number and i != position[0]:
            return False

    # check box
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    return True


def solve(board):
    find = findEmpty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if checkValid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True
            board[row][col] = 0

    return False


def solveGUI(obj, dis):

    if str(type(obj)) != "<class '__main__.GUI'>":
        print("we got em")
        exit("invalid obj type")

    find = findEmpty(obj.playBoard)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if checkValid(obj.playBoard, i, (row, col)):
            obj.playBoard[row][col] = i

            obj.drawGrid(dis)
            obj.drawNums(dis)
            # GUI.drawGrid(height, width, color1, color2, screen)
            # GUI.drawBoard(width, height, numSpacing,
            #               board, numberFont, screen)

            pygame.display.update()
            pygame.time.delay(100)

            if solveGUI(obj, dis):
                return True
            obj.playBoard[row][col] = 0

    return False
