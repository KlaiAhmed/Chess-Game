import pygame
from pygame.locals import *
import chess

# Initialize Pygame
pygame.init()

# Get screen dimensions
infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h

# Set up the display
WINDOW_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) - 100  # Leave some space around the window
SQUARE_SIZE = WINDOW_SIZE // 8
WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
pygame.display.set_caption('Chess')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (205, 133, 63)
BEIGE = (245, 245, 220)
GREY = (192, 192, 192)
BLUE = (0, 0, 255)

# Load and scale piece images
PIECES = {
    'r': pygame.transform.smoothscale(pygame.image.load('images/black_rook.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'n': pygame.transform.smoothscale(pygame.image.load('images/black_knight.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'b': pygame.transform.smoothscale(pygame.image.load('images/black_bishop.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'q': pygame.transform.smoothscale(pygame.image.load('images/black_queen.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'k': pygame.transform.smoothscale(pygame.image.load('images/black_king.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'p': pygame.transform.smoothscale(pygame.image.load('images/black_pawn.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'R': pygame.transform.smoothscale(pygame.image.load('images/white_rook.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'N': pygame.transform.smoothscale(pygame.image.load('images/white_knight.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'B': pygame.transform.smoothscale(pygame.image.load('images/white_bishop.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'Q': pygame.transform.smoothscale(pygame.image.load('images/white_queen.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'K': pygame.transform.smoothscale(pygame.image.load('images/white_king.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
    'P': pygame.transform.smoothscale(pygame.image.load('images/white_pawn.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20)),
}

def draw_board(win):
    colors = [BEIGE, BROWN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = PIECES[piece.symbol()]
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            win.blit(piece_image, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10))

def draw_possible_moves(win, moves):
    for move in moves:
        col = chess.square_file(move.to_square)
        row = 7 - chess.square_rank(move.to_square)
        pygame.draw.circle(win, GREY, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 20)

def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    return chess.square(col, 7 - row)

class Game:
    def __init__(self):
        self.board = chess.Board()
        self.selected_square = None
        self.possible_moves = []

    def select_square(self, square):
        if self.selected_square == square:
            self.selected_square = None
            self.possible_moves = []
        else:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.possible_moves = [move for move in self.board.legal_moves if move.from_square == square]
            else:
                self.selected_square = None
                self.possible_moves = []

    def make_move(self, move):
        if move in self.possible_moves:
            self.board.push(move)
            self.selected_square = None
            self.possible_moves = []

    def is_game_over(self):
        return self.board.is_checkmate() or self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves() or self.board.is_fivefold_repetition()

    def get_winner(self):
        if self.board.is_checkmate():
            return "White wins!" if self.board.turn == chess.BLACK else "Black wins!"
        return "Draw!"

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    font = pygame.font.SysFont("Arial", 72)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN and not game.is_game_over():
                square = get_square_under_mouse()
                if game.selected_square is not None and square in [move.to_square for move in game.possible_moves]:
                    game.make_move(chess.Move(game.selected_square, square))
                else:
                    game.select_square(square)

        draw_board(WIN)
        draw_pieces(WIN, game.board)
        draw_possible_moves(WIN, game.possible_moves)
        
        if game.is_game_over():
            text = font.render(game.get_winner(), True, BLUE)
            WIN.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE // 2 - text.get_height() // 2))
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
