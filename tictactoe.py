import numpy as np
import pygame
import sys

CONST_WIDTH = 600
CONST_HEIGHT = 600
CONST_BG_COLOR = (30, 129, 176)
CONST_LINE_COLOR = (17, 95, 132, 1)
CONST_SHAPE_COLOR = (255, 255, 255)
CONST_BOARD_ROWS = 3
CONST_BOARD_COLUMNS = 3
CONST_CIRCLE_RADIUS = 60
CONST_CIRCLE_WIDTH = 15
CONST_X_WIDTH = 25
CONST_SQUARE_SIZE = 200
CONST_SPACE = 55
CONST_RED = (255, 0, 0)
CONST_MAGIC_NUMBER = 15


class Game:
    def __init__(self):
        self.board = np.zeros((CONST_BOARD_ROWS, CONST_BOARD_COLUMNS))
        pygame.init()
        self.screen = pygame.display.set_mode((CONST_WIDTH, CONST_HEIGHT))
        self.set_screen()
        self.draw_lines()
        self.curr_Player = 1
        self.gamestate = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.gamestate:
                    self.x_pos_mouse = event.pos[0]
                    self.y_pos_mouse = event.pos[1]

                    self.clicked_Col = int(self.x_pos_mouse // 200)
                    self.clicked_Row = int(self.y_pos_mouse // 200)

                    if self.check_square(self.clicked_Row, self.clicked_Col):
                        self.place(self.clicked_Row, self.clicked_Col, self.curr_Player)
                        if self.check_win(self.curr_Player):
                            self.gamestate = False
                        if self.check_board_full():
                            self.gamestate = False

                        self.curr_Player = self.curr_Player % 2 + 1
                        self.draw_shapes()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                        self.gamestate = True
            pygame.display.update()

    def restart(self):
        self.set_screen()
        self.draw_lines()
        self.curr_Player = 1
        for row in range(CONST_BOARD_ROWS):
            for col in range(CONST_BOARD_COLUMNS):
                self.board[row][col] = 0

    def set_screen(self):
        self.screen.fill(CONST_BG_COLOR)

    def draw_lines(self):
        # Horizontal
        pygame.draw.line(self.screen, CONST_LINE_COLOR, (0, 200), (600, 200), 15)
        pygame.draw.line(self.screen, CONST_LINE_COLOR, (0, 400), (600, 400), 15)
        # Vertical
        pygame.draw.line(self.screen, CONST_LINE_COLOR, (200, 0), (200, 600), 15)
        pygame.draw.line(self.screen, CONST_LINE_COLOR, (400, 0), (400, 600), 15)

    def place(self, row, col, player):
        self.board[row][col] = player

    def check_square(self, row, column):
        # check if 0 / is empty
        return self.board[row][column] == 0

    def check_board_full(self):
        # check each row for 0 if there is 0, board is not full
        for row in range(CONST_BOARD_ROWS):
            for col in range(CONST_BOARD_COLUMNS):
                if self.board[row][col] == 0:
                    return False
        return True

    def draw_shapes(self):
        for row in range(CONST_BOARD_ROWS):
            for col in range(CONST_BOARD_COLUMNS):
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, CONST_SHAPE_COLOR, (int(col * 200 + 100), int(row * 200 + 100)),
                                       CONST_CIRCLE_RADIUS, CONST_CIRCLE_WIDTH)
                elif self.board[row][col] == 2:
                    pygame.draw.line(self.screen, CONST_SHAPE_COLOR,
                                     (col * CONST_SQUARE_SIZE + CONST_SPACE,
                                      row * CONST_SQUARE_SIZE + CONST_SQUARE_SIZE - CONST_SPACE),
                                     (col * CONST_SQUARE_SIZE + CONST_SQUARE_SIZE - CONST_SPACE,
                                      row * CONST_SQUARE_SIZE + CONST_SPACE), CONST_X_WIDTH)
                    pygame.draw.line(self.screen, CONST_SHAPE_COLOR,
                                     (col * CONST_SQUARE_SIZE + CONST_SPACE, row * CONST_SQUARE_SIZE + CONST_SPACE), (
                                         col * CONST_SQUARE_SIZE + CONST_SQUARE_SIZE - CONST_SPACE,
                                         row * CONST_SQUARE_SIZE + CONST_SQUARE_SIZE - CONST_SPACE), CONST_X_WIDTH)

    def check_win(self, player):
        for col in range(CONST_BOARD_COLUMNS):
            if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                self.drawVerticalLine(col)
                return True
        for row in range(CONST_BOARD_ROWS):
            if self.board[row][0] == player and self.board[row][1] == player and self.board[row][2] == player:
                self.drawHorizontalLine(row)
                return True
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            self.drawDescendingLine()
            return True
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            self.drawAscendingLine()
            return True

    def drawVerticalLine(self, col):
        x_pos = col * 200 + 100
        pygame.draw.line(self.screen, CONST_RED, (x_pos, 15), (x_pos, CONST_HEIGHT - 15), 15)

    def drawHorizontalLine(self, row):
        y_pos = row * 200 + 100
        pygame.draw.line(self.screen, CONST_RED, (15, y_pos), (CONST_WIDTH - 15, y_pos), 15)

    def drawDescendingLine(self):
        pygame.draw.line(self.screen, CONST_RED, (15, 15), (CONST_WIDTH - 15, CONST_HEIGHT - 15), 15)

    def drawAscendingLine(self):
        pygame.draw.line(self.screen, CONST_RED, (15, CONST_HEIGHT - 15), (CONST_WIDTH - 15, 15), 15)


if __name__ == '__main__':
    tictactoe = Game()
