import pygame
import Soduku
import Solver
import copy


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(
                win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('genevattf', 25)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class GUI:

    def __init__(self):
        super().__init__()

        self.answerBoard = Soduku.makeAnswer()
        self.OGBoard = Soduku.makeGameBoard(self.answerBoard)
        self.playBoard = copy.deepcopy(self.OGBoard)
        self.answerBoard2 = None

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (200, 200, 200)
        self.darkGray = (120, 120, 120)
        self.blue = (66, 245, 182)

        self.numberFont = pygame.font.SysFont("genevattf", 50)

        self.screen_mult = 9  # this could change to size if i end up doing that
        self.screen_size = 80

        self.width = self.screen_size * self.screen_mult
        self.height = self.screen_size * self.screen_mult
        self.pad = self.width // 9
        self.boardW = self.width - self.pad * 2
        self.boardH = self.height - self.pad * 2

    def drawGrid(self, display):

        squareVert = self.boardW // 3
        squareHor = self.boardH // 3

        cubeVert = squareVert // 3
        cubeHor = squareHor // 3

        display.fill(self.white)

        font = pygame.font.SysFont("genevattf", 90)
        text = font.render("Sudoku", 1, self.blue)
        display.blit(text, (self.width//2 - 120, self.pad//2 - 30))

        # draw cube vert
        for i in range(self.pad, self.boardW + self.pad, cubeVert):
            pygame.draw.line(display, self.gray,
                             (i, self.pad), (i, self.boardH + self.pad))
        # draw cube hor
        for i in range(self.pad, self.boardH + self.pad, cubeHor):
            pygame.draw.line(display, self.gray,
                             (self.pad, i), (self.boardH + self.pad, i))

        for i in range(self.pad, self.boardW + self.pad, squareVert):
            pygame.draw.line(display, self.black,
                             (i, self.pad), (i, self.boardH + self.pad))

        for i in range(self.pad, self.boardH + self.pad, squareHor):
            pygame.draw.line(display, self.black,
                             (self.pad, i), (self.boardH + self.pad, i))

    def drawNums(self, display):

        spacing = self.boardW // 9
        Y = self.pad + (self.boardW // 18) - 15

        #offsetY = (self.width // 18) - 25

        for i in range(len(self.playBoard)):
            # offsetX = (self.width // 18) - 15
            X = self.pad + (self.boardH // 18) - 10
            for j in range(len(self.playBoard[0])):
                if self.playBoard[i][j] != 0:
                    pos = (X, Y)

                    if(self.OGBoard[i][j] != 0):
                        numSurf = self.numberFont.render(
                            str(self.playBoard[i][j]), 1, self.black)
                        display.blit(numSurf, pos)

                    else:
                        numSurf = self.numberFont.render(
                            str(self.playBoard[i][j]), 1, self.darkGray)
                        display.blit(numSurf, pos)
                X += spacing
            Y += spacing

    def placeNum(self, num, loc):
        x = loc[0]
        y = loc[1]

        if (self.OGBoard[x][y] == 0):
            self.playBoard[x][y] = num

    def checkAnsewr(self):
        return self.playBoard == self.answerBoard or self.playBoard == self.answerBoard2

    def reset(self):
        self.playBoard = copy.deepcopy(self.OGBoard)

    def solve(self, dis):
        self.playBoard = copy.deepcopy(self.OGBoard)
        Solver.solveGUI(self, dis)
        self.answerBoard2 = copy.deepcopy(self.playBoard)


def findCube(XY, board):

    mouseX = XY[0]
    mouseY = XY[1]

    if(mouseX > board.pad and mouseX < board.width - board.pad and mouseY > board.pad and mouseY < board.height - board.pad):
        j = (mouseX - board.pad) // (board.boardH//9)
        i = (mouseY - board.pad) // (board.boardW//9)

        return (i, j)  # locaiton in matrix

    return None


def main():
    pygame.init()
    board = GUI()

    fps = 10
    fpsCount = pygame.time.Clock()

    font = pygame.font.SysFont("genevattf", 100)

    pygame.display.set_caption("Sudoku")
    icon = pygame.image.load("nine.png")

    display = pygame.display.set_mode(
        (board.width, board.height))

    pygame.display.set_icon(icon)
    # fpsCount.tick(fps)

    buttonY = board.boardH + (board.pad * 1.25)
    buttonX = board.width // 5 - 17

    submit = button((0, 162, 199), buttonX, buttonY, 90, 40, "Submit")
    clear = button((0, 162, 199), buttonX*2, buttonY, 90, 40, "Clear")
    solve = button((0, 162, 199), buttonX*3, buttonY, 90, 40, "Solve")
    newGame = button((0, 162, 199), buttonX*4,
                     buttonY, 90, 40, "New Game")

    running = True
    key = None
    location = None
    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                exit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if submit.isOver(pos):
                    if board.checkAnsewr():

                        board.drawGrid(display)
                        board.drawNums(display)
                        submit.draw(display)
                        clear.draw(display)
                        solve.draw(display)
                        newGame.draw(display)

                        text = font.render("Correct", 1, (0, 255, 0))
                        display.blit(
                            text, (board.width//2 - 120, board.height//2 - 20))
                        pygame.display.update()
                        pygame.time.delay(1000)

                    else:
                        board.drawGrid(display)
                        board.drawNums(display)
                        submit.draw(display)
                        clear.draw(display)
                        solve.draw(display)
                        newGame.draw(display)

                        text = font.render("Try Again!", 1, (255, 0, 0))
                        display.blit(
                            text, (board.width//2 - 150, board.height//2 - 20))
                        pygame.display.update()
                        pygame.time.delay(1000)

                if clear.isOver(pos):
                    board.reset()

                if solve.isOver(pos):
                    board.solve(display)

                if newGame.isOver(pos):
                    board = GUI()

                else:
                    location = findCube(pos, board)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

            if(location != None and key != None):
                board.placeNum(key, location)
                key = None

        board.drawGrid(display)
        board.drawNums(display)
        submit.draw(display)
        clear.draw(display)
        solve.draw(display)
        newGame.draw(display)

        pygame.display.update()


main()
