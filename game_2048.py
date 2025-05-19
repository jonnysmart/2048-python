"""
Project: 2048 Game Implementation
Language: Python 3.13.2
Library: Pygame
Author: Mulat Gebrehiwot Tesfay
UCO: 565129

Description:
-------------
This project implements the classic 2048 game using Python and the Pygame library.
The player combines numbered tiles on a 4x4 grid by moving them in four directions (up, down, left, right).
Tiles with the same value merge upon collision, doubling their value.
A new tile (2 or 4) appears after each valid move.
The player wins by creating a tile with the value 2048.
The game ends if no valid moves are possible.

Key Features:
-------------
- 4x4 game grid using a two-dimensional list.
- Tile movement and merging logic implemented per game rules.
- Win and loss conditions detection.
- Input handling for valid moves and error handling for invalid inputs.
- Graphical user interface built with Pygame.
- Restart, Continue, and Quit options after game conclusion.
"""

import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up window size and grid settings
WINDOW_SIZE = 400
GRID_SIZE = 4
TILE_SIZE = WINDOW_SIZE // GRID_SIZE

# Define colors (RGB)
BACKGROUND_COLOR = (173, 216, 230)
EMPTY_TILE_COLOR = (224, 255, 255)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Set up the screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('2048 Game')

# Set up fonts
font = pygame.font.SysFont("comicsansms", 40)
small_font = pygame.font.SysFont("comicsansms", 24)

# Game board initialization
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Game state flags
game_over = False
game_won = False
continue_after_win = False
invalid_key_pressed = False

def add_random_tile():
    """
    Add a new tile (2 or 4) at a random empty position on the board.
    """
    empty_tiles = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if grid[row][col] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        grid[row][col] = random.choice([2, 4])

def draw_board():
    """
    Render the current game board and game messages to the screen.
    """
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if value == 0:
                pygame.draw.rect(screen, EMPTY_TILE_COLOR, rect)
            else:
                pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), rect)
                text_surface = font.render(str(value), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    if game_won and not continue_after_win:
        line1 = small_font.render("You Win!", True, (255, 0, 0))
        line2 = small_font.render("Press R to Restart, Q to Quit, or C to Continue", True, (255, 0, 0))
        screen.blit(line1, (WINDOW_SIZE // 2 - line1.get_width() // 2, WINDOW_SIZE // 2 - 60))
        screen.blit(line2, (WINDOW_SIZE // 2 - line2.get_width() // 2, WINDOW_SIZE // 2 - 20))
    elif game_over:
        line1 = small_font.render("Game Over!", True, (255, 0, 0))
        line2 = small_font.render("Press R to Restart or Q to Quit", True, (255, 0, 0))
        screen.blit(line1, (WINDOW_SIZE // 2 - line1.get_width() // 2, WINDOW_SIZE // 2 - 40))
        screen.blit(line2, (WINDOW_SIZE // 2 - line2.get_width() // 2, WINDOW_SIZE // 2))
    elif invalid_key_pressed:
        msg = small_font.render("Invalid key! Use arrow keys.", True, (255, 0, 0))
        screen.blit(msg, (20, WINDOW_SIZE - 30))

    pygame.display.update()

def compress(row):
    """
    Shift all non-zero tiles in a row to the left, maintaining their order.
    """
    new_row = [num for num in row if num != 0]
    new_row += [0] * (GRID_SIZE - len(new_row))
    return new_row

def merge(row):
    """
    Merge adjacent tiles of the same value by doubling the first and zeroing the second.
    """
    for i in range(GRID_SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left():
    moved = False
    for i in range(GRID_SIZE):
        original = list(grid[i])
        row = compress(grid[i])
        row = merge(row)
        row = compress(row)
        grid[i] = row
        if grid[i] != original:
            moved = True
    return moved

def move_right():
    moved = False
    for i in range(GRID_SIZE):
        original = list(grid[i])
        row = list(reversed(grid[i]))
        row = compress(row)
        row = merge(row)
        row = compress(row)
        grid[i] = list(reversed(row))
        if grid[i] != original:
            moved = True
    return moved

def move_up():
    moved = False
    for col in range(GRID_SIZE):
        original = [grid[row][col] for row in range(GRID_SIZE)]
        column = compress(original)
        column = merge(column)
        column = compress(column)
        for row in range(GRID_SIZE):
            grid[row][col] = column[row]
        if [grid[row][col] for row in range(GRID_SIZE)] != original:
            moved = True
    return moved

def move_down():
    moved = False
    for col in range(GRID_SIZE):
        original = [grid[row][col] for row in range(GRID_SIZE)]
        column = list(reversed(original))
        column = compress(column)
        column = merge(column)
        column = compress(column)
        column = list(reversed(column))
        for row in range(GRID_SIZE):
            grid[row][col] = column[row]
        if [grid[row][col] for row in range(GRID_SIZE)] != original:
            moved = True
    return moved

def check_win():
    for row in grid:
        if 2048 in row:
            return True
    return False

def check_game_over():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return False
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return False
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return False
    return True

def reset_game():
    global grid, game_over, game_won, continue_after_win, invalid_key_pressed
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    add_random_tile()
    add_random_tile()
    game_over = False
    game_won = False
    continue_after_win = False
    invalid_key_pressed = False

# Initialize the board with two random tiles
add_random_tile()
add_random_tile()

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        # Handle window close event
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard input event
        if event.type == pygame.KEYDOWN:
            # Check if game is over or player has won and not chosen to continue
            if game_over or (game_won and not continue_after_win):
                if event.key == pygame.K_r:
                    # Restart the game if 'R' is pressed
                    reset_game()
                elif event.key == pygame.K_q:
                    # Quit the game if 'Q' is pressed
                    running = False
                elif event.key == pygame.K_c and game_won:
                    # Continue playing after winning if 'C' is pressed
                    continue_after_win = True
            else:
                moved = False
                invalid_key_pressed = False

                # Handle movement keys
                if event.key == pygame.K_LEFT:
                    moved = move_left()
                elif event.key == pygame.K_RIGHT:
                    moved = move_right()
                elif event.key == pygame.K_UP:
                    moved = move_up()
                elif event.key == pygame.K_DOWN:
                    moved = move_down()
                else:
                    # Handle invalid key press
                    invalid_key_pressed = True
                    print("Invalid key pressed! Use arrow keys.")

                # After a valid move, add a new random tile and check game state
                if moved:
                    add_random_tile()
                    if not game_won and check_win():
                        game_won = True
                    elif check_game_over():
                        game_over = True

    # Draw the updated game board and any messages
    draw_board()

pygame.quit()
sys.exit()
