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
piece_names = [
    "PawnWhite", "PawnBlack", "RookWhite", "RookBlack", "BishopWhite", "BishopBlack",
    "KnightWhite", "KnightBlack", "QueenWhite", "QueenBlack", "KingWhite", "KingBlack"
]
for name in piece_names:
    pieces[name] = pygame.image.load(f"{name}.png")
    pieces[name] = pygame.transform.scale(pieces[name], (SQUARE_SIZE, SQUARE_SIZE))
    pieces[name] = pygame.transform.rotozoom(pieces[name], 0, 0.8)

# Load move sound
move_sound = pygame.mixer.Sound("move.mp3")

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Board setup
board = [
    ["RookBlack", "KnightBlack", "BishopBlack", "QueenBlack", "KingBlack", "BishopBlack", "KnightBlack", "RookBlack"],
    ["PawnBlack"] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ["PawnWhite"] * 8,
    ["RookWhite", "KnightWhite", "BishopWhite", "QueenWhite", "KingWhite", "BishopWhite", "KnightWhite", "RookWhite"]
]

# Add global variables for scores and player names
player_scores = {"Player 1": 0, "Player 2": 0}
high_scores = []  # List of tuples (name, score)
player_names = ["Player 1", "Player 2"]

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

    buttons = ["Easy", "Med", "Hard"]
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

def ai_move(ai_color):
    def get_valid_moves(piece, row, col):
        moves = []
        if piece == f"Pawn{ai_color}":
            direction = 1 if ai_color == "Black" else -1
            start_row = 1 if ai_color == "Black" else 6
            next_row = row + direction
            if 0 <= next_row < ROWS and board[next_row][col] is None:
                moves.append((next_row, col))
            if row == start_row and board[row + direction][col] is None and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))
            # Pawn captures
            for dc in [-1, 1]:
                capture_row, capture_col = row + direction, col + dc
                if 0 <= capture_row < ROWS and 0 <= capture_col < COLS:
                    target = board[capture_row][capture_col]
                    if target and not target.endswith(ai_color):
                        moves.append((capture_row, capture_col))
        elif piece == f"Rook{ai_color}":
            for i in range(1, ROWS):
                if row + i < ROWS and (board[row + i][col] is None or (board[row + i][col] and not board[row + i][col].endswith(ai_color))):
                    moves.append((row + i, col))
                    if board[row + i][col] is not None:
                        break
                else:
                    break
            for i in range(1, ROWS):
                if row - i >= 0 and (board[row - i][col] is None or (board[row - i][col] and not board[row - i][col].endswith(ai_color))):
                    moves.append((row - i, col))
                    if board[row - i][col] is not None:
                        break
                else:
                    break
            for i in range(1, COLS):
                if col + i < COLS and (board[row][col + i] is None or (board[row][col + i] and not board[row][col + i].endswith(ai_color))):
                    moves.append((row, col + i))
                    if board[row][col + i] is not None:
                        break
                else:
                    break
            for i in range(1, COLS):
                if col - i >= 0 and (board[row][col - i] is None or (board[row][col - i] and not board[row][col - i].endswith(ai_color))):
                    moves.append((row, col - i))
                    if board[row][col - i] is not None:
                        break
                else:
                    break
        elif piece == f"Knight{ai_color}":
            knight_moves = [
                (row + 2, col + 1), (row + 2, col - 1),
                (row - 2, col + 1), (row - 2, col - 1),
                (row + 1, col + 2), (row + 1, col - 2),
                (row - 1, col + 2), (row - 1, col - 2)
            ]
            for r, c in knight_moves:
                if 0 <= r < ROWS and 0 <= c < COLS and (board[r][c] is None or (board[r][c] and not board[r][c].endswith(ai_color))):
                    moves.append((r, c))
        elif piece == f"Bishop{ai_color}":
            for i in range(1, ROWS):
                if row + i < ROWS and col + i < COLS and (board[row + i][col + i] is None or (board[row + i][col + i] and not board[row + i][col + i].endswith(ai_color))):
                    moves.append((row + i, col + i))
                    if board[row + i][col + i] is not None:
                        break
                else:
                    break
            for i in range(1, ROWS):
                if row + i < ROWS and col - i >= 0 and (board[row + i][col - i] is None or (board[row + i][col - i] and not board[row + i][col - i].endswith(ai_color))):
                    moves.append((row + i, col - i))
                    if board[row + i][col - i] is not None:
                        break
                else:
                    break
            for i in range(1, ROWS):
                if row - i >= 0 and col + i < COLS and (board[row - i][col + i] is None or (board[row - i][col + i] and not board[row - i][col + i].endswith(ai_color))):
                    moves.append((row - i, col + i))
                    if board[row - i][col + i] is not None:
                        break
                else:
                    break
            for i in range(1, ROWS):
                if row - i >= 0 and col - i >= 0 and (board[row - i][col - i] is None or (board[row - i][col - i] and not board[row - i][col - i].endswith(ai_color))):
                    moves.append((row - i, col - i))
                    if board[row - i][col - i] is not None:
                        break
                else:
                    break
        elif piece == f"Queen{ai_color}":
            moves.extend(get_valid_moves(f"Rook{ai_color}", row, col))
            moves.extend(get_valid_moves(f"Bishop{ai_color}", row, col))
        elif piece == f"King{ai_color}":
            king_moves = [
                (row + 1, col), (row - 1, col),
                (row, col + 1), (row, col - 1),
                (row + 1, col + 1), (row + 1, col - 1),
                (row - 1, col + 1), (row - 1, col - 1)
            ]
            for r, c in king_moves:
                if 0 <= r < ROWS and 0 <= c < COLS and (board[r][c] is None or (board[r][c] and not board[r][c].endswith(ai_color))):
                    moves.append((r, c))
        return moves

    def piece_value(piece):
        if not piece:
            return 0
        if 'King' in piece:
            return 1000
        if 'Queen' in piece:
            return 9
        if 'Rook' in piece:
            return 5
        if 'Bishop' in piece or 'Knight' in piece:
            return 3
        if 'Pawn' in piece:
            return 1
        return 0

    def is_checkmate_for(color):
        # Simple check: is king missing?
        for row in board:
            for piece in row:
                if piece == f'King{color}':
                    return False
        return True

    best_score = -float('inf')
    best_move = None
    ai_pieces = [(r, c) for r in range(ROWS) for c in range(COLS) if board[r][c] and board[r][c].endswith(ai_color)]
    for row, col in ai_pieces:
        piece = board[row][col]
        valid_moves = get_valid_moves(piece, row, col)
        for move_row, move_col in valid_moves:
            captured = board[move_row][move_col]
            # Simulate move
            temp = board[move_row][move_col]
            board[move_row][move_col] = board[row][col]
            board[row][col] = None
            score = piece_value(captured)
            # Check for checkmate
            opponent_color = "White" if ai_color == "Black" else "Black"
            if is_checkmate_for(opponent_color):
                score += 10000
            # Undo move
            board[row][col] = board[move_row][move_col]
            board[move_row][move_col] = temp
            if score > best_score:
                best_score = score
                best_move = (row, col, move_row, move_col)
    if best_move:
        row, col, move_row, move_col = best_move
        board[move_row][move_col] = board[row][col]
        board[row][col] = None
        move_sound.play()  # Play sound for AI move

def display_scores():
    font = pygame.font.Font(None, 30)
    y_offset = HEIGHT - 100
    # Remove player scores at the bottom left
    # Only display high scores at the bottom right
    high_scores_sorted = sorted(high_scores, key=lambda x: x[1], reverse=True)
    for i, (name, score) in enumerate(high_scores_sorted[:5]):
        text = font.render(f"{i+1}. {name}: {score}", True, WHITE)
        screen.blit(text, (WIDTH - 200, y_offset + i * 20))

def pause_game():
    paused = True
    font = pygame.font.Font(None, 40)
    text = font.render("Game Paused. Press 'P' to resume.", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

def rename_players():
    global player_names
    font = pygame.font.Font(None, 40)
    for i in range(2):
        name = ""
        while True:
            screen.fill(GRAY)
            text = font.render(f"Enter name for Player {i+1}:", True, BLACK)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 4))

            # Create a confirm button
            confirm_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
            pygame.draw.rect(screen, WHITE, confirm_button)
            confirm_text = font.render("Ok", True, BLACK)
            screen.blit(confirm_text, (confirm_button.x + 10, confirm_button.y + 10))

            # Display the current input name
            input_text = font.render(name, True, BLACK)
            screen.blit(input_text, (WIDTH // 2 - 150, HEIGHT // 3))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        player_names[i] = name if name else f"Player {i+1}"
                        return
                    else:
                        name += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_button.collidepoint(event.pos):
                        player_names[i] = name if name else f"Player {i+1}"
                        return

def is_king_mated(color):
    # Use correct piece names for king
    king_piece = f"King{color}"
    for row in board:
        for piece in row:
            if piece == king_piece:
                return False
    return True

def play_again_prompt():
    screen.fill(GRAY)
    font = pygame.font.Font(None, 40)
    text = font.render("Play Again?", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 4))

    buttons = ["Yes", "No"]
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
                for rect, choice in button_rects:
                    if rect.collidepoint(event.pos):
                        return choice == "Yes"

def chess_manual_screen():
    manual_text = [
        "Chess Manual:",
        "- Each player starts with 16 pieces: 8 pawns, 2 rooks,", 
        " 2 knights, 2 bishops, 1 queen, 1 king.",
        "- Pawns move forward 1 square (first move: 2 squares).", 
        " Capture diagonally.",
        "- Rooks move any number of squares horizontally", 
        " or vertically.",
        "- Knights move in an 'L' shape: 2 squares in one direction,",
        " then 1 square perpendicular.",
        "- Bishops move diagonally any number of squares.",
        "- Queen moves any number of squares in any direction.",
        "- King moves 1 square in any direction.",
        "- Check: King is under threat. Checkmate:",
        " King cannot escape threat.",
        "- Win by checkmating the opponent's king.",
        "- Press the button below to continue."
    ]
    screen.fill(GRAY)
    font = pygame.font.Font(None, 28)
    for i, line in enumerate(manual_text):
        text = font.render(line, True, BLACK)
        screen.blit(text, (40, 40 + i * 32))
    # Continue button
    button_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 100, 140, 50)
    pygame.draw.rect(screen, WHITE, button_rect)
    btn_font = pygame.font.Font(None, 36)
    btn_text = btn_font.render("Continue", True, BLACK)
    screen.blit(btn_text, (button_rect.x + 15, button_rect.y + 10))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return

def main():
    initial_board = [
        ["RookBlack", "KnightBlack", "BishopBlack", "QueenBlack", "KingBlack", "BishopBlack", "KnightBlack", "RookBlack"],
        ["PawnBlack"] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        ["PawnWhite"] * 8,
        ["RookWhite", "KnightWhite", "BishopWhite", "QueenWhite", "KingWhite", "BishopWhite", "KnightWhite", "RookWhite"]
    ]
    global board
    chess_manual_screen()
    rename_players()
    difficulty = welcome_screen()
    player_color = choose_color_screen()
    ai_color = "Black" if player_color == "White" else "White"
    print(f"Game started with {difficulty} difficulty, Player: {player_names[0]} ({player_color}), AI: {player_names[1]} ({ai_color})")
    while True:
        board = [row[:] for row in initial_board]
        selected_piece = None
        running = True
        # AI always plays from the top (Black pieces), player always at the bottom (White pieces)
        if player_color == "White":
            player_turn = True
        else:
            # Player is Black, so AI (White) moves first
            player_turn = False
        winner = None  # Track winner

        # If player chose Black, let AI (White) make the first move
        if player_color == "Black":
            ai_color = "White"
            ai_move(ai_color)  # AI as White moves first
            player_turn = True

        while running:
            screen.fill(BLACK)
            draw_board()
            display_scores()  # Display high scores on the screen

            # Display player and AI names with their scores at the bottom left
            font = pygame.font.Font(None, 30)
            player_score = player_scores.get(player_names[0], 0)
            ai_score = player_scores.get(player_names[1], 0)
            player_text = font.render(f"{player_names[0]} (You): {player_score}", True, WHITE)
            ai_text = font.render(f"{player_names[1]} (AI): {ai_score}", True, WHITE)
            screen.blit(player_text, (10, HEIGHT - 60))
            screen.blit(ai_text, (10, HEIGHT - 30))

            # Display player color at the bottom center
            color_text = font.render(f"You are: {player_color}", True, WHITE)
            screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, HEIGHT - 30))

            # Check if the player's king is mated
            if is_king_mated(player_color):
                font = pygame.font.Font(None, 60)
                text = font.render("You Lose!", True, WHITE)
                screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
                pygame.display.update()
                pygame.time.delay(3000)
                running = False
                winner = player_names[1]  # AI wins
                continue

            # Check if the AI's king is mated
            if is_king_mated(ai_color):
                font = pygame.font.Font(None, 60)
                text = font.render("You Win!", True, WHITE)
                screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
                pygame.display.update()
                pygame.time.delay(3000)
                running = False
                winner = player_names[0]  # Player wins
                continue

            pygame.display.update()

            if not player_turn:
                pygame.time.delay(500)
                ai_move(ai_color)
                move_sound.play()  # Play sound for AI move
                player_turn = True
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause_game()  # Pause the game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    if 0 <= row < 8 and 0 <= col < 8:
                        if selected_piece:
                            board[row][col] = board[selected_piece[0]][selected_piece[1]]
                            board[selected_piece[0]][selected_piece[1]] = None
                            move_sound.play()  # Play sound for player move
                            player_turn = False
                            selected_piece = None
                        else:
                            if board[row][col] and player_color in board[row][col]:
                                selected_piece = (row, col)

        # Add a point to the winner before asking to play again
        if winner:
            player_scores[winner] = player_scores.get(winner, 0) + 1

        if not play_again_prompt():
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()