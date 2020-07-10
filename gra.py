import random, os, sys
import pygame
from pygame.locals import*

FPS = 5
BOXSIZE = 32
BOXWIDTH = 12
BOXHEIGHT = 12
DIFF = 1

class Button:
    def __init__(self):
        self.bomb = False
        self.flag = False
        self.visible = False
        self.number = 0

    def __str__(self):
        s1 = 'B' if self.bomb else '.'
        s2 = 'f' if self.flag else '.'
        s3 = 'v' if self.visible else '.'
        return "[%s%s%s]" % (s1, s2, s3)


class Game:

    def __init__(self, diff, rows, cols):
        self.rows = rows
        self.cols = cols
        self.diff = diff
        self.board = [[Button() for i in range(cols)] for j in range(rows)]
        self.bombCounter = int(rows * cols * diff // 10)
        self.state = "running"

    def placeBombs(self):
        for i in range(self.bombCounter):
            while(True):
                x = random.randint(0, self.rows-1)
                y = random.randint(0, self.cols-1)
                if(self.board[x][y].bomb == False):
                    self.board[x][y].bomb = True
                    break

    def bombAround(self, x, y):
        count = 0
        if(self.board[x][y].bomb == False):
            if(x > 0 and y > 0):
                count += self.board[x-1][y-1].bomb
            if(x > 0):
                count += self.board[x-1][y].bomb
            if(x > 0 and y < self.cols-1):
                count += self.board[x-1][y+1].bomb
            if(y > 0):
                count += self.board[x][y-1].bomb
            if(y < self.cols-1):
                count += self.board[x][y+1].bomb
            if(x < self.rows-1):
                count += self.board[x+1][y].bomb
            if(x < self.rows-1 and y > 0):
                count += self.board[x+1][y-1].bomb
            if(x < self.rows-1 and y < self.cols-1):
                count += self.board[x+1][y+1].bomb
        return count

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print()

    def fieldInfo(self, x, y):
        if(x < 0 or x >= self.rows or y < 0 or y >= self.cols):
            return '#'
        if(self.board[x][y].visible == False and self.board[x][y].flag == True):
            return 'F'
        if(self.board[x][y].visible == False and self.board[x][y].flag == False):
            return '_'
        if(self.board[x][y].visible == True and self.board[x][y].bomb == True):
            return 'x'
        if(self.board[x][y].visible == True and self.bombAround(x, y) == 0):
            return ' '
        if(self.board[x][y].visible == True and self.bombAround(x, y) > 0):
            return self.bombAround(x, y)


class View:
    def __init__(self, game):
        self.game = game

    def display(self):
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                print("[%s]" % str(self.game.fieldInfo(i, j)), end="")
            print()

    def takeInput(self):
        x, y = map(int, input("Podaj wspolrzedne punktu: ").split())
        return (x, y)

    def revealField(self, x, y):
        if(self.game.fieldInfo(x, y) != '#' and self.game.board[x][y].visible == False):

            self.game.board[x][y].visible = True
            if(self.game.bombAround(x, y) == 0):
                self.revealField(x-1, y-1)
                self.revealField(x-1, y)
                self.revealField(x-1, y+1)
                self.revealField(x, y-1)
                self.revealField(x, y+1)
                self.revealField(x+1, y-1)
                self.revealField(x+1, y)
                self.revealField(x+1, y+1)
        if(self.game.fieldInfo(x, y) == 'x'):
            print("Przegrales")
            sys.exit()

    def play(self):
        while(True):
            x, y = self.takeInput()
            self.revealField(x-1, y-1)
            self.display()

class Gui:

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((BOXSIZE * BOXWIDTH, BOXSIZE * BOXHEIGHT), 0, 32)
        self.texture = pygame.image.load("C:/Users/jakub/Desktop/gra 3/tiles.jpg")
        self.win.blit(self.texture,(0,0))
        pygame.display.update()
        self.game = Game(DIFF, BOXHEIGHT, BOXWIDTH)
        self.game.placeBombs()
        self.view = View(self.game)

    def display(self):
        for i in range(len(self.game.board)):
            for j in range((len(self.game.board[i]))):
                field = self.game.fieldInfo(i,j)

                if field == 'F':
                    self.win.blit(self.texture, (j * BOXSIZE, i * BOXSIZE),
                     (11 * BOXSIZE, 0, BOXSIZE, BOXSIZE))
                elif field == '_':
                    self.win.blit(self.texture, (j * BOXSIZE, i * BOXSIZE),
                    (10 * BOXSIZE, 0, BOXSIZE, BOXSIZE))
                elif field == 'x':
                    self.win.blit(self.texture, (j * BOXSIZE, i * BOXSIZE),
                    (9 * BOXSIZE, 0, BOXSIZE, BOXSIZE))
                elif field == '_':
                    self.win.blit(self.texture, (j * BOXSIZE, i * BOXSIZE),
                    (10 * BOXSIZE, 0, BOXSIZE, BOXSIZE))
                elif field == ' ':
                    self.win.blit(self.texture, (j * BOXSIZE, i * BOXSIZE),
                    (0, 0, BOXSIZE, BOXSIZE))
                elif field != '#':
                    self.win.blit(self.texture, (j * BOXSIZE, i * BOXSIZE),
                    (int(field) * BOXSIZE, 0, BOXSIZE, BOXSIZE))

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x //= BOXSIZE
                    y //= BOXSIZE
                    self.view.revealField(y, x)
                    self.view.display()
                    print()
                    print()
                    print()
                elif event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    x //= BOXSIZE
                    y //= BOXSIZE
                    if(self.game.fieldInfo(y,x) == '_'):
                        self.game.board[y][x].flag = True
                    elif(self.game.fieldInfo(y,x) == 'F'):
                        self.game.board[y][x].flag = False


    def play(self):
        clock = pygame.time.Clock()
        while True:
            self.handleEvent()
            self.display()
            pygame.display.update()
            clock.tick(FPS)
