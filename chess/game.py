import pygame
from pygame.locals import *
import chess

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (205, 133, 63)
BEIGE = (245, 245, 220)

# Load piece images
PIECES = {
    'r': pygame.image.load('images/black_rook.png'),
    'n': pygame.image.load('images/black_knight.png'),
    'b': pygame.image.load('images/black_bishop.png'),
    'q': pygame.image.load('images/black_queen.png'),
    'k': pygame.image.load('images/black_king.png'),
    'p': pygame.image.load('images/black_pawn.png'),
    'R': pygame.image.load('images/white_rook.png'),
    'N': pygame.image.load('images/white_knight.png'),
    'B': pygame.image.load('images/white_bishop.png'),
    'Q': pygame.image.load('images/white_queen.png'),
    'K': pygame.image.load('images/white_king.png'),
    'P': pygame.image.load('images/white_pawn.png')
}

class Game:
    def __init__(self):
        self.board = chess.Board()
        self.selected_square = None
        self.move_made = False
    
    def make_move(self, move):
        if move in self.board.legal_moves:
            self.board.push(move)
            self.move_made = True
            self.selected_square = None
    
    def get_legal_moves(self):
        return list(self.board.legal_moves)

def draw_board(win):
    colors = [BEIGE, BROWN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(win, color, (col * 100, row * 100, 100, 100))

def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // 100
    row = mouse_pos[1] // 100
    return chess.square(col, 7 - row)

def draw_pieces(win, board):
    pieces = board.fen().split()[0].replace('/', '')
    for i, piece in enumerate(pieces):
        if piece.isdigit():
            continue
        row = i // 8
        col = i % 8
        win.blit(PIECES[piece], (col * 100, (7 - row) * 100))

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                square = get_square_under_mouse()
                if game.selected_square is None:
                    if game.board.piece_at(square):
                        game.selected_square = square
                else:
                    move = chess.Move(game.selected_square, square)
                    game.make_move(move)
                    game.selected_square = None
        
        draw_board(WIN)
        draw_pieces(WIN, game.board)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
