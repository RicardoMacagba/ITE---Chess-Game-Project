import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700  # Extra space for UI
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BROWN = (184, 139, 74)
LIGHT_BROWN = (227, 193, 111)

# Load piece images
pieces = {}
piece_names = ["PawnTextWhite", "PawnTextBlack", "RookTextWhite", "RookTextBlack", "BishopTextWhite", "BishopTextBlack", 
               "KnightTextWhite", "KnightTextBlack", "QueenTextWhite", "QueenTextBlack", "KingTextWhite", "KingTextBlack"]
for name in piece_names:
    pieces[name] = pygame.image.load(f"{name}.png")
    pieces[name] = pygame.transform.scale(pieces[name], (SQUARE_SIZE, SQUARE_SIZE))
    pieces[name] = pygame.transform.rotozoom(pieces[name], 0, 0.8)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Board setup
board = [
    ["RookTextBlack", "KnightTextBlack", "BishopTextBlack", "QueenTextBlack", "KingTextBlack", "BishopTextBlack", "KnightTextBlack", "RookTextBlack"],
    ["PawnTextBlack"] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ["PawnTextWhite"] * 8,
    ["RookTextWhite", "KnightTextWhite", "BishopTextWhite", "QueenTextWhite", "KingTextWhite", "BishopTextWhite", "KnightTextWhite", "RookTextWhite"]
]

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece:
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def welcome_screen():
    screen.fill(GRAY)
    font = pygame.font.Font(None, 40)
    text = font.render("Choose Difficulty", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 4))

    buttons = ["Easy", "Medium", "Hard"]
    button_rects = []
    for i, btn in enumerate(buttons):
        rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 3 + i * 70, 100, 50)
        button_rects.append((rect, btn))
        pygame.draw.rect(screen, WHITE, rect)
        text = font.render(btn, True, BLACK)
        screen.blit(text, (rect.x + 20, rect.y + 10))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, difficulty in button_rects:
                    if rect.collidepoint(event.pos):
                        return difficulty

def choose_color_screen():
    screen.fill(GRAY)
    font = pygame.font.Font(None, 40)
    text = font.render("Choose Your Color", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 4))

    buttons = ["White", "Black"]
    button_rects = []
    for i, btn in enumerate(buttons):
        rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 3 + i * 70, 100, 50)
        button_rects.append((rect, btn))
        pygame.draw.rect(screen, WHITE, rect)
        text = font.render(btn, True, BLACK)
        screen.blit(text, (rect.x + 20, rect.y + 10))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, color in button_rects:
                    if rect.collidepoint(event.pos):
                        return color

def ai_move():
    # Simple AI that randomly moves a piece
    while True:
        ai_pieces = [(r, c) for r in range(ROWS) for c in range(COLS) if board[r][c] and "Black" in board[r][c]]
        if not ai_pieces:
            return
        piece_pos = random.choice(ai_pieces)
        row, col = piece_pos
        move_row, move_col = row + 1, col
        if 0 <= move_row < ROWS and board[move_row][move_col] is None:
            board[move_row][move_col] = board[row][col]
            board[row][col] = None
            break

def main():
    difficulty = welcome_screen()
    player_color = choose_color_screen()
    ai_color = "Black" if player_color == "White" else "White"
    print(f"Game started with {difficulty} difficulty, Player: {player_color}, AI: {ai_color}")
    
    selected_piece = None
    running = True
    player_turn = player_color == "White"
    
    while running:
        screen.fill(BLACK)
        draw_board()
        
        pygame.display.update()
        
        if not player_turn:
            pygame.time.delay(500)
            ai_move()
            player_turn = True
            continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                if 0 <= row < 8 and 0 <= col < 8:
                    if selected_piece:
                        board[row][col] = board[selected_piece[0]][selected_piece[1]]
                        board[selected_piece[0]][selected_piece[1]] = None
                        player_turn = False
                        selected_piece = None
                    else:
                        if board[row][col] and player_color in board[row][col]:
                            selected_piece = (row, col)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
