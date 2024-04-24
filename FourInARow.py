import pygame
import sys
import numpy as np

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 110
RADIUS = int(SQUARESIZE / 2 - 5)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PVP = 1
PVAI = 2
AIVAI = 3

# Initialize pygame
pygame.init()

# Create the game window
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("4-in-a-row")

# Function to create the game board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))
    
# Function to drop a token onto the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Function to check if a column is valid for dropping a token
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Function to find the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Function to print the game board (for debugging)
def print_board(board):
    print(np.flip(board, 0))

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.circle(screen, RED if board[r][c] == 1 else YELLOW if board[r][c] == 2 else BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

# Function to check for winning combinations
def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            
def restart_game():
    global board, game_over, turn
    board = create_board()
    game_over = False
    turn = 0

def menu_screen():
    screen.fill(BLACK)
    pvp_text = "1. Player vs Player"
    pvai_text = "2. Player vs AI"
    aivai_text = "3. AI vs AI"
    font = pygame.font.SysFont(None, 40)
    text_surface_pvp = font.render(pvp_text, True, BLUE)
    text_surface_pvai = font.render(pvai_text, True, BLUE)
    text_surface_aivai = font.render(aivai_text, True, BLUE)
    screen.blit(text_surface_pvp, (width // 2 - text_surface_pvp.get_width() // 2, height // 2 - 60))
    screen.blit(text_surface_pvai, (width // 2 - text_surface_pvai.get_width() // 2, height // 2))
    screen.blit(text_surface_aivai, (width // 2 - text_surface_aivai.get_width() // 2, height // 2 + 60))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return PVP
                elif event.key == pygame.K_2:
                    return PVAI
                elif event.key == pygame.K_3:
                    return AIVAI

# Initialize the game board
restart_game()
myfont = pygame.font.SysFont("monospace", 45)
player_scores = {1: 0, 2: 0}

# Main game loop
while True:
    # Display menu screen and get selected mode
    mode = menu_screen()

    # Main game loop for the selected mode
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED if turn == 0 else YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_valid_location(board, col):
                   # Drop a piece for the current player
                    row = get_next_open_row(board, col)
                    current_player = 1 if turn == 0 else 2
                    drop_piece(board, row, col, current_player)

                    # Check if the current player has won
                    if winning_move(board, current_player) or np.all(board != 0):
                        draw_board(board)
                        player_scores[current_player] += 1
                        screen.blit(myfont.render(f"Player {current_player} wins! P1: {player_scores[1]} P2: {player_scores[2]}" if winning_move(board, current_player) else "It's a tie!", 1, RED if current_player == 1 else YELLOW if winning_move(board, current_player) else BLUE), (40, 10))
                        game_over = True
                    # Print the updated board and toggle the turn if the game is not over
                    print_board(board)
                    if not game_over:
                        turn = (turn + 1) % 2
                else:
                    # Invalid move, don't change the turn
                    print("Invalid move!")
                pygame.display.update()

                if game_over:
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                                sys.exit()
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                # Restart the game
                                restart_game()
                                waiting = False      

        draw_board(board)
        screen.blit(myfont.render(f"Player {turn + 1}'s turn", 1, RED if turn == 0 else YELLOW), (40, 10))
        pygame.display.update()

    #TODO: Add Different modes of play (Player vs Player, Player vs AI, AI vs AI)
    #TODO: Add a difficulty setting for the AI
    #TODO: Add logic for AI player moves