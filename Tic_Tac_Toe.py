import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_W = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQ_SIZE = 200
CIRC_RAD = 60
CIRC_W = 15
CROSS_W = 25
SPC = 55

# RGB Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRC_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Display Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Super Tic Tac Toe')
screen.fill(BG_COLOR)

# Board Setup
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Pygame Clock
clock = pygame.time.Clock()

def draw_lines():
    # Draw grid lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQ_SIZE), (WIDTH, i * SQ_SIZE), LINE_W)
        pygame.draw.line(screen, LINE_COLOR, (i * SQ_SIZE, 0), (i * SQ_SIZE, HEIGHT), LINE_W)

def draw_figures():
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            center = (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2)
            if board[r][c] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (center[0] - SPC, center[1] - SPC), (center[0] + SPC, center[1] + SPC), CROSS_W)
                pygame.draw.line(screen, CROSS_COLOR, (center[0] + SPC, center[1] - SPC), (center[0] - SPC, center[1] + SPC), CROSS_W)
            elif board[r][c] == 'O':
                pygame.draw.circle(screen, CIRC_COLOR, center, CIRC_RAD, CIRC_W)

def check_winner():
    for r in range(BOARD_ROWS):
        if board[r][0] == board[r][1] == board[r][2] and board[r][0] is not None:
            return board[r][0]
    for c in range(BOARD_COLS):
        if board[0][c] == board[1][c] == board[2][c] and board[0][c] is not None:
            return board[0][c]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def minimax(board, maxing):
    winner = check_winner()
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif not any(None in row for row in board):
        return 0

    if maxing:
        best = -float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] is None:
                    board[r][c] = 'X'
                    score = minimax(board, False)
                    board[r][c] = None
                    best = max(score, best)
        return best
    else:
        best = float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] is None:
                    board[r][c] = 'O'
                    score = minimax(board, True)
                    board[r][c] = None
                    best = min(score, best)
        return best

def ai_move():
    best = -float('inf')
    move = None
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] is None:
                board[r][c] = 'X'
                score = minimax(board, False)
                board[r][c] = None
                if score > best:
                    best = score
                    move = (r, c)
    if move:
        board[move[0]][move[1]] = 'X'
        return check_winner() == 'X'

def main():
    running = True
    player = 'O'  # Human is 'O', AI is 'X'
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not check_winner():
                mouseX, mouseY = event.pos
                col, row = mouseX // SQ_SIZE, mouseY // SQ_SIZE
                if board[row][col] is None:
                    board[row][col] = player
                    if check_winner() == 'O':
                        print("Human wins!")
                        running = False
                    if not running or ai_move():
                        print("AI Won")
                        running = False

        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        pygame.display.update()
        clock.tick(60)

main()