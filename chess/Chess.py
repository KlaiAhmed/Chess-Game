import pygame
from pygame.locals import *
import chess

pygame.init()

infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h

WINDOW_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) - 100  
SQUARE_SIZE = WINDOW_SIZE // 8
WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
pygame.display.set_caption('Chess')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (205, 133, 63)
BEIGE = (245, 245, 220)
GREY = (192, 192, 192)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0, 128)

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
WOOD_TEXTURE = pygame.transform.smoothscale(pygame.image.load('images/wood_texture.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_board(win, offset_x, offset_y, selected_square):
    colors = [BEIGE, BROWN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            rect = pygame.Rect(offset_x + col * SQUARE_SIZE, offset_y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, color, rect)
            if selected_square is not None and chess.square_file(selected_square) == col and chess.square_rank(selected_square) == 7 - row:
                pygame.draw.rect(win, YELLOW, rect, 0)

def draw_pieces(win, board, offset_x, offset_y):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_image = PIECES[piece.symbol()]
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            win.blit(piece_image, (offset_x + col * SQUARE_SIZE + 10, offset_y + row * SQUARE_SIZE + 10))

def draw_possible_moves(win, moves, offset_x, offset_y):
    for move in moves:
        col = chess.square_file(move.to_square)
        row = 7 - chess.square_rank(move.to_square)
        pygame.draw.circle(win, GREY, (offset_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, offset_y + row * SQUARE_SIZE + SQUARE_SIZE // 2), 20)

def get_square_under_mouse(offset_x, offset_y):
    mouse_pos = pygame.mouse.get_pos()
    col = (mouse_pos[0] - offset_x) // SQUARE_SIZE
    row = (mouse_pos[1] - offset_y) // SQUARE_SIZE
    if 0 <= col < 8 and 0 <= row < 8:
        return chess.square(col, 7 - row)
    return None

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

    def handle_pawn_promotion(self, move):
        if self.board.piece_at(move.from_square).piece_type == chess.PAWN:
            if chess.square_rank(move.to_square) in [0, 7]:
                self.board.push(move)
                self.promote_pawn(move.to_square)
                return True
        return False

    def promote_pawn(self, square):
        running = True
        piece_type = chess.QUEEN
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    piece_type = self.get_selected_piece_type(mouse_pos, square)
                    if piece_type:
                        running = False

            WIN.blit(WOOD_TEXTURE, (0, 0))
            offset_x = (WIN.get_width() - WINDOW_SIZE) // 2
            offset_y = (WIN.get_height() - WINDOW_SIZE) // 2
            draw_board(WIN, offset_x, offset_y, self.selected_square)
            draw_pieces(WIN, self.board, offset_x, offset_y)
            self.draw_promotion_selection(WIN, square, offset_x, offset_y)
            pygame.display.update()

        self.board.set_piece_at(square, chess.Piece(piece_type, self.board.turn))

    def draw_promotion_selection(self, win, square, offset_x, offset_y):
        options = ['Q', 'R', 'B', 'N']
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        for i, piece in enumerate(options):
            piece_image = PIECES[piece if self.board.turn == chess.WHITE else piece.lower()]
            win.blit(piece_image, (offset_x + col * SQUARE_SIZE + 10, offset_y + (row + i + 1) * SQUARE_SIZE + 10))

    def get_selected_piece_type(self, mouse_pos, square):
        x, y = mouse_pos
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        if (col * SQUARE_SIZE + 10 <= x <= (col + 1) * SQUARE_SIZE - 10):
            for i in range(4):
                if (row + i + 1) * SQUARE_SIZE + 10 <= y <= (row + i + 2) * SQUARE_SIZE - 10:
                    return options[i]
        return None

    def is_game_over(self):
        return self.board.is_checkmate() or self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves() or self.board.is_fivefold_repetition()

    def get_winner(self):
        if self.board.is_checkmate():
            return "White wins" if self.board.turn == chess.BLACK else "Black wins"
        return "Draw"

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    font = pygame.font.SysFont("Arial", 48)

    while run:
        clock.tick(60)
        offset_x = (WIN.get_width() - WINDOW_SIZE) // 2
        offset_y = (WIN.get_height() - WINDOW_SIZE) // 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN and not game.is_game_over():
                square = get_square_under_mouse(offset_x, offset_y)
                if square is not None:
                    if game.selected_square is not None and square in [move.to_square for move in game.possible_moves]:
                        move = chess.Move(game.selected_square, square)
                        if not game.handle_pawn_promotion(move):
                            game.make_move(move)
                    else:
                        game.select_square(square)

        WIN.blit(WOOD_TEXTURE, (0, 0))
        draw_board(WIN, offset_x, offset_y, game.selected_square)
        draw_pieces(WIN, game.board, offset_x, offset_y)
        draw_possible_moves(WIN, game.possible_moves, offset_x, offset_y)
        
        if game.is_game_over():
            text = font.render(game.get_winner(), True, BLUE)
            WIN.blit(text, (WIN.get_width() // 2 - text.get_width() // 2, WIN.get_height() // 2 - text.get_height() // 2))
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
