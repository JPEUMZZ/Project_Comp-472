import math
import copy
import time
import argparse

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()
        self.turnNumber = 0

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
        valid_moves = self.valid_moves(game_state)
        return move in valid_moves

         

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
   
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
                    moves = self.queen_moves(row, col)
                elif piece[1] == 'B':  
                    moves = self.bishop_moves(row, col)
                elif piece[1] == 'N':  
                    moves = self.knight_moves(row, col)
                elif piece[1] == 'p':  
                    moves = self.pawn_moves(row, col, turn, game_state)

                
                for move in moves:
                    end_row, end_col = move
                    if 0 <= end_row < 5 and 0 <= end_col < 5:
                        target_piece = board[end_row][end_col]
                        if target_piece == '.' or (turn == 'white' and target_piece[0] == 'b') or (turn == 'black' and target_piece[0] == 'w'):
                            valid_moves.append(((row, col), (end_row, end_col)))

     return valid_moves                        
               
    def king_moves(self, row, col):
        moves = [
        (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
        (row, col - 1),(row, col + 1),(row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
        return moves
    
    def queen_moves(self, row, col):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),(0, 1),(1, -1),  (1, 0), (1, 1)]
        for direcRow, direcCol in directions:
            curentRow, curentCol = row + direcRow, col + direcCol
            while 0 <= curentRow < 5 and 0 <= curentCol < 5:
                moves.append((curentRow, curentCol))
                curentRow += direcRow
                curentCol += direcCol
        return moves

    def bishop_moves(self, row, col):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direcRow, direcCol in directions:
            curentRow, curentCol = row + direcRow, col + direcCol
            while 0 <= curentRow < 5 and 0 <= curentCol < 5:
                moves.append((curentRow, curentCol))
                curentRow += direcRow
                curentCol += direcCol
        return moves
 
    def knight_moves(self, row, col):
    
     moves = [
        (row - 2, col - 1), (row - 2, col + 1),
        (row - 1, col - 2), (row - 1, col + 2),
        (row + 1, col - 2), (row + 1, col + 2),
        (row + 2, col - 1), (row + 2, col + 1)
        ]
     return moves
    
    def pawn_moves(self, row, col, turn, game_state):
        moves = []
        board = game_state["board"]
        if turn == 'white':
            if row > 0:
                if board[row - 1][col] == '.':
                    moves.append((row - 1, col))

                if col > 0 and board[row - 1][col - 1] != '.' and board[row - 1][col - 1][0] == 'b':
                     moves.append((row - 1, col - 1))
                
                if col < 4 and board[row - 1][col + 1] != '.' and board[row - 1][col + 1][0] == 'b':
                    moves.append((row - 1, col + 1))
        else:  
            if row < 4:
                if board[row + 1][col] == '.':
                    moves.append((row + 1, col))  
                
                if col > 0 and board[row + 1][col - 1] != '.' and board[row + 1][col - 1][0] == 'w':
                    moves.append((row + 1, col - 1))

                if col < 4 and board[row + 1][col + 1] != '.' and board[row + 1][col + 1][0] == 'w':
                    moves.append((row + 1, col + 1))
        return moves

    def is_on_board(self, position):
     col, row = position[0], position[1]
     return  str(col) in 'ABCDE' and str(row) in '12345'
    
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
            currentPlayer = self.current_game_state['turn'].capitalize()
            move = input(f"{currentPlayer} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move) :
                print("Invalid move. Try again.")
                continue
            
            self.turnNumber += 1
            self.make_move(self.current_game_state, move)
            start, end = move
            startPosition = f"{chr(start[1] + ord('A'))}{5 - start[0]}"
            endPosition = f"{chr(end[1] + ord('A'))}{5 - end[0]}"
            print(f"Action taken: Move from {startPosition} to {endPosition}")
            print(f"Turn number: {self.turnNumber}")
            print(f"Player: {currentPlayer}")
            

if __name__ == "__main__":
    game = MiniChess()
    game.play()