import math
import copy
import time
import argparse

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {
                "board": 
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                }
        return state

    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    """
    Check if the move is valid    
    
    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move which we check the validity of ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing the validity of the move
    """
   def is_valid_move(self, game_state, move):
    start, end = move
    start_row, start_col = start
    end_row, end_col = end

    # Board boundaries check
    if not (0 <= start_row < 5 and 0 <= start_col < 5 and 0 <= end_row < 5 and 0 <= end_col < 5):
        return False

    # Turn and piece ownership check
    piece = game_state["board"][start_row][start_col]
    if not piece or (game_state["turn"] == "white" and piece[0] != 'w') or (game_state["turn"] == "black" and piece[0] != 'b'):
        return False

    # Target square check (can't capture own piece)
    target = game_state["board"][end_row][end_col]
    if target and target[0] == piece[0]:
        return False

    # Movement rules based on piece type
    piece_type = piece[1]
    if piece_type == 'K':  # King
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1
    elif piece_type == 'Q':  # Queen
        return self.is_valid_queen_move(start, end, game_state)
    elif piece_type == 'B':  # Bishop
        return self.is_valid_bishop_move(start, end, game_state)
    elif piece_type == 'N':  # Knight
        return self.is_valid_knight_move(start, end)
    elif piece_type == 'p':  # Pawn
        return self.is_valid_pawn_move(piece[0], start, end, game_state)
    
    return False

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
def is_valid_queen_move(self, start, end, game_state):
    return self.is_valid_rook_move(start, end, game_state) or self.is_valid_bishop_move(start, end, game_state)
def is_valid_bishop_move(self, start, end, game_state):
    start_row, start_col = start
    end_row, end_col = end
    if abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal
        return not self.is_path_blocked(start, end, game_state)
    return False
def is_valid_knight_move(self, start, end):
    start_row, start_col = start
    end_row, end_col = end
    return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)
def is_valid_pawn_move(self, color, start, end, game_state):
    start_row, start_col = start
    end_row, end_col = end
    direction = 1 if color == 'w' else -1  # White moves up, Black moves down
    target = game_state["board"][end_row][end_col]

    # Forward move
    if end_col == start_col and not target:
        return end_row - start_row == direction

    # Diagonal capture
    if abs(end_col - start_col) == 1 and target and target[0] != color:
        return end_row - start_row == direction

    return False
def is_path_blocked(self, start, end, game_state):
    start_row, start_col = start
    end_row, end_col = end
    row_step = 1 if end_row > start_row else -1 if end_row < start_row else 0
    col_step = 1 if end_col > start_col else -1 if end_col < start_col else 0

    current_row, current_col = start_row + row_step, start_col + col_step
    while (current_row, current_col) != (end_row, end_col):
        if game_state["board"][current_row][current_col] != '.':
            return True
        current_row += row_step
        current_col += col_step

    return False
def valid_moves(self, game_state):
    moves = []
    for row in range(5):
        for col in range(5):
            piece = game_state["board"][row][col]
            if piece and ((game_state["turn"] == "white" and piece[0] == 'w') or (game_state["turn"] == "black" and piece[0] == 'b')):
                for end_row in range(5):
                    for end_col in range(5):
                        move = ((row, col), (end_row, end_col))
                        if self.is_valid_move(game_state, move):
                            moves.append(move)
    return moves


    """
    Modify to board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start = move[0]
        end = move[1]
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state

    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        while True:
            self.display_board(self.current_game_state)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                print("Invalid move. Try again.")
                continue

            self.make_move(self.current_game_state, move)

if __name__ == "__main__":
    game = MiniChess()
    game.play()