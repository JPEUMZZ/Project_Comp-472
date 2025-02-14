import math
import copy
import time
import argparse
from game_io import get_game_parameters, save_game_trace

class MiniChess:
    def __init__(self):
        self.game_parameters = get_game_parameters()
        print(f"Loaded Game Parameters: {self.game_parameters}")
        self.current_game_state = self.init_board()
        self.initial_board = [row.copy() for row in self.current_game_state["board"]]
        self.totalMoves = 0
        self.turnNumber = 0  # Counter for draw condition
        self.moves_log = []
        self.board_snapshots = []

    def init_board(self):
        state = {
            "board": [
                ['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']
            ],
            "turn": 'white',
        }
        return state

    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6 - i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print("\n     A   B   C   D   E\n")

    def valid_moves(self, game_state):
        valid_moves = []
        board = game_state["board"]
        turn = game_state["turn"]

        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece == '.':
                    continue

                if (turn == 'white' and piece[0] == 'w') or (turn == 'black' and piece[0] == 'b'):
                    if piece[1] == 'K':
                        moves = self.king_moves(row, col)
                    elif piece[1] == 'Q':
                        moves = self.queen_moves(row, col, board)
                    elif piece[1] == 'B':
                        moves = self.bishop_moves(row, col, board)
                    elif piece[1] == 'N':
                        moves = self.knight_moves(row, col)
                    elif piece[1] == 'p':
                        moves = self.pawn_moves(row, col, turn, game_state)

                    for move in moves:
                        end_row, end_col = move
                        if 0 <= end_row < 5 and 0 <= end_col < 5:
                            target_piece = board[end_row][end_col]
                            if target_piece == '.' or target_piece[0] != piece[0]:  # No same-color captures
                                valid_moves.append(((row, col), (end_row, end_col)))

        return valid_moves

    def king_moves(self, row, col):
        moves = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1), (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
        ]
        return moves

    def queen_moves(self, row, col, board):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 5 and 0 <= c < 5:
                if board[r][c] == '.':
                    moves.append((r, c))
                else:
                    if board[r][c][0] != board[row][col][0]:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        return moves

    def bishop_moves(self, row, col, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 5 and 0 <= c < 5:
                if board[r][c] == '.':
                    moves.append((r, c))
                else:
                    if board[r][c][0] != board[row][col][0]:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        return moves

    def knight_moves(self, row, col):
        return [
            (row - 2, col - 1), (row - 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2),
            (row + 2, col - 1), (row + 2, col + 1)
        ]

    def pawn_moves(self, row, col, turn, game_state):
        moves = []
        board = game_state["board"]
        direction = -1 if turn == 'white' else 1

        if 0 <= row + direction < 5:
            if board[row + direction][col] == '.':
                moves.append((row + direction, col))

            for dc in [-1, 1]:
                if 0 <= col + dc < 5 and board[row + direction][col + dc] != '.' and board[row + direction][col + dc][0] != turn[0]:
                    moves.append((row + direction, col + dc))

        return moves
    
    def get_board_string(self, board):
        """Format the board as a string (for saving to trace)."""
        return "\n".join(" ".join(piece.rjust(3) for piece in row) for row in board)

    def make_move(self, game_state, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        target_piece = game_state["board"][end_row][end_col]

        if target_piece in ["bK","wK"]:
            winner = game_state['turn'].capitalize()
            print(f"Game Over! {winner} wins by capturing the King.")
            save_game_trace(self.game_parameters, self.moves_log, f"{winner} (King Capture)", self.initial_board, self.board_snapshots)
            exit(0)

        # Maintain turnNumber only for capture-based draw rule
        if target_piece != '.':
            self.turnNumber = 0
        else:
            self.turnNumber += 1

        self.totalMoves += 1


        if self.turnNumber >= 10:
            print("Game Over! It's a draw (10 turns without a capture).")
            save_game_trace(self.game_parameters, self.moves_log, "Draw (10 Turns No Capture)", self.initial_board, self.board_snapshots)
            exit(0)


        #pawn promotion
        if piece in ["wp", "bp"] and ((piece == "wp" and end_row == 0) or (piece == "bp" and end_row == 4)):
            piece = piece[0] + "Q"

        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state

    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5 - int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5 - int(end[1]), ord(end[0].upper()) - ord('A'))
            return start, end
        except:
            return None

    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        self.board_snapshots.append(f"Turn 0 (White):\n{self.get_board_string(self.current_game_state['board'])}\n")

        while True:
            self.display_board(self.current_game_state)
            currentPlayer = self.current_game_state['turn'].capitalize()
            move = input(f"{currentPlayer} to move: ")

            if move.lower() == 'exit':
                print("Game exited.")
                break

            parsed_move = self.parse_input(move)
            if not parsed_move or parsed_move not in self.valid_moves(self.current_game_state):
                print("Invalid move. Try again.")
                continue

        
            self.moves_log.append(f"Turn {self.totalMoves + 1} ({currentPlayer}): {move}")
            self.make_move(self.current_game_state, parsed_move)

            self.board_snapshots.append(f"Turn {self.totalMoves} ({currentPlayer}):\n{self.get_board_string(self.current_game_state['board'])}\n")

            print(f"DEBUG: Total Moves: {self.totalMoves}, Max Turns: {self.game_parameters['max_turns']}")
            print(f"DEBUG: Turn Number: {self.turnNumber} (For Capture Condition)")

            if self.totalMoves >= self.game_parameters['max_turns']:
                print("Game Over! Reached maximum moves.")
                save_game_trace(self.game_parameters, self.moves_log, "Draw (Max Moves Reached)", self.initial_board, self.board_snapshots)
                break



if __name__ == "__main__":
    game = MiniChess()
    game.play()
