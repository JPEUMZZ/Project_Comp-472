import math
import copy
import time
import argparse
import threading
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
        
        # AI statistics
        self.states_explored = 0
        self.states_by_depth = {}
        self.total_branching_factor = 0
        self.total_branching_samples = 0

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
        new_state = copy.deepcopy(game_state)
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        piece = new_state["board"][start_row][start_col]
        target_piece = new_state["board"][end_row][end_col]

        # Check for win condition (king captured)
        if target_piece in ["bK", "wK"]:
            return new_state, True, new_state["turn"].capitalize()

        # Pawn promotion
        if piece in ["wp", "bp"] and ((piece == "wp" and end_row == 0) or (piece == "bp" and end_row == 4)):
            piece = piece[0] + "Q"

        new_state["board"][start_row][start_col] = '.'
        new_state["board"][end_row][end_col] = piece
        new_state["turn"] = "black" if new_state["turn"] == "white" else "white"

        return new_state, False, None

    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5 - int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5 - int(end[1]), ord(end[0].upper()) - ord('A'))
            return start, end
        except:
            return None

    def coordinate_to_string(self, coord):
        row, col = coord
        return f"{chr(col + ord('A'))}{5 - row}"

    def e0_heuristic(self, game_state):
        """
        Implements the e0 heuristic:
        e0 = (#wp + 3 · #wB + 3 · #wN + 9 · #wQ + 999 · wK) - (#bp + 3 · #bB + 3 · #bN + 9 · #bQ + 999 · bK)
        """
        board = game_state["board"]
        
        # Initialize counters for each piece
        piece_counts = {
            'wp': 0, 'wB': 0, 'wN': 0, 'wQ': 0, 'wK': 0,
            'bp': 0, 'bB': 0, 'bN': 0, 'bQ': 0, 'bK': 0
        }
        
        # Count pieces on the board
        for row in board:
            for piece in row:
                if piece in piece_counts:
                    piece_counts[piece] += 1
        
        # Calculate heuristic value
        white_value = (piece_counts['wp'] + 
                       3 * piece_counts['wB'] + 
                       3 * piece_counts['wN'] + 
                       9 * piece_counts['wQ'] + 
                       999 * piece_counts['wK'])
        
        black_value = (piece_counts['bp'] + 
                       3 * piece_counts['bB'] + 
                       3 * piece_counts['bN'] + 
                       9 * piece_counts['bQ'] + 
                       999 * piece_counts['bK'])
        
        return white_value - black_value
		
    def e1_heuristic(self, game_state):
        """
        e1 = e0 + positional weighting
        Encourages central control and pawn advancement.
        """
        e0_value = self.e0_heuristic(game_state)
        board = game_state["board"]
        
        # Positional weight map (encourages central control)
        position_weights = [
            [ 3,  4,  5,  4,  3],
            [ 4,  6,  8,  6,  4],
            [ 5,  8, 10,  8,  5],
            [ 4,  6,  8,  6,  4],
            [ 3,  4,  5,  4,  3]
        ]
        
        position_score = 0
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece == '.':
                    continue
                
                weight = position_weights[row][col]
                if piece[0] == 'w':
                    position_score += weight
                elif piece[0] == 'b':
                    position_score -= weight
        
        return e0_value + position_score
		
    def e2_heuristic(self, game_state):
        """
        Faster e2 heuristic: Simplified material + positional evaluation.
        """
        e0_value = self.e0_heuristic(game_state)
        board = game_state["board"]
        
        position_score = 0
        
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece == '.':
                    continue
                
                piece_type = piece[1]
                owner = 1 if piece[0] == 'w' else -1  # White: +1, Black: -1
                
                # Simple positional scoring
                if piece_type == 'K':  # King prefers edges
                    position_score += owner * (1 if row in [0, 4] or col in [0, 4] else -1)
                elif piece_type == 'p':  # Pawns prefer advancing but avoid last row
                    position_score += owner * (row if piece[0] == 'w' else (4 - row))
                elif piece_type in ['N', 'B']:  # Knights/Bishops prefer the center
                    position_score += owner * (2 - abs(2 - row) - abs(2 - col))
                elif piece_type == 'Q':  # Queen prefers mobility
                    position_score += owner * (5 - abs(2 - row) - abs(2 - col))
        
        return e0_value + position_score
		
    def minimax(self, game_state, depth, max_depth, maximizing_player, alpha=float('-inf'), beta=float('inf'), use_alpha_beta=True, start_time=None, max_time=None):
        # Track states explored
        self.states_explored += 1
        if depth not in self.states_by_depth:
            self.states_by_depth[depth] = 0
        self.states_by_depth[depth] += 1
        
        # Check if we've run out of time
        if start_time and max_time and time.time() - start_time > max_time:
            return None, None, True  # Time's up
        
        # Terminal conditions: depth reached or game over
        if depth == max_depth:
            return self.e0_heuristic(game_state), None, False
        
        valid_moves = self.valid_moves(game_state)
        
        # Add to branching factor statistics
        if depth > 0:  # Don't count root node
            self.total_branching_factor += len(valid_moves)
            self.total_branching_samples += 1
        
        # If no valid moves or game is over
        if not valid_moves:
            return self.e0_heuristic(game_state), None, False
        
        best_move = None
        time_up = False
        
        if maximizing_player:
            best_value = float('-inf')
            for move in valid_moves:
                new_state, game_over, winner = self.make_move(game_state, move)
                
                # If game is over due to king capture
                if game_over:
                    return 1000 if winner == 'White' else -1000, move, False
                
                value, _, time_exceeded = self.minimax(new_state, depth + 1, max_depth, False, alpha, beta, use_alpha_beta, start_time, max_time)
                
                if time_exceeded:
                    return None, None, True #stop searching immediately
                
                if value > best_value:
                    best_value = value
                    best_move = move
                
                if use_alpha_beta:
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
        else:
            best_value = float('inf')
            for move in valid_moves:
                #timeout check as well in moves loop
                if time.time() - start_time > max_time:
                    return None, None, True #stops searching immediately
                
                new_state, game_over, winner = self.make_move(game_state, move)
                
                # If game is over due to king capture
                if game_over:
                    return -1000 if winner == 'Black' else 1000, move, False
                
                value, _, time_exceeded = self.minimax(new_state, depth + 1, max_depth, True, alpha, beta, use_alpha_beta, start_time, max_time)
                
                if time_exceeded:
                    return None, None, True # stops searching immediately
                
                if value < best_value:
                    best_value = value
                    best_move = move
                
                if use_alpha_beta:
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
        
        return best_value, best_move, time_up

    def get_ai_move(self, game_state):
        # Reset statistics for this move
        self.states_explored = 0
        self.states_by_depth = {}
        
        start_time = time.time()
        max_time = self.game_parameters["time_limit"]
        use_alpha_beta = self.game_parameters["alpha_beta"]
        heuristic_choice = self.game_parameters.get("heuristic", "e0")
        
        best_score = None
        best_move = None
        current_depth = 1
        
        heuristic_function = self.e0_heuristic if heuristic_choice == "e0" else self.e1_heuristic
        
        # Iterative deepening
        while True:
            # Reset state counting for this depth
            self.states_explored = 0
            self.states_by_depth = {}
            self.total_branching_factor = 0
            self.total_branching_samples = 0
            
            # Start with the initial search
            is_maximizing = game_state["turn"] == "white"
            score, move, time_exceeded = self.minimax(
                game_state, 
                0, 
                current_depth, 
                is_maximizing, 
                float('-inf'),
                float('inf'),
                use_alpha_beta, 
                start_time, 
                max_time
            )
            
            if time_exceeded:
                break
            
            best_score = score
            best_move = move
            
            # If we've reached a terminal state or running out of time
            if time.time() - start_time > max_time * 0.8:
                break
                
            current_depth += 1
        
        # Calculate average branching factor
        avg_branching = self.total_branching_factor / max(1, self.total_branching_samples)
        
        # Prepare statistics for output
        search_time = time.time() - start_time
        heuristic_score = heuristic_function(game_state)
        
        stats = {
            "score": best_score,
            "time": search_time,
            "depth": current_depth - 1,
            "states_explored": self.states_explored,
            "states_by_depth": self.states_by_depth,
            "avg_branching": avg_branching,
            "heuristic_score": heuristic_score
        }
        
        if best_move:
            start_str = self.coordinate_to_string(best_move[0])
            end_str = self.coordinate_to_string(best_move[1])
            move_str = f"{start_str} {end_str}"
            return move_str, stats
        else:
            # If no move was found, select a random valid move
            valid_moves = self.valid_moves(game_state)
            if valid_moves:
                move = valid_moves[0]
                start_str = self.coordinate_to_string(move[0])
                end_str = self.coordinate_to_string(move[1])
                move_str = f"{start_str} {end_str}"
                return move_str, stats
            return None, stats
    
    def init_game_parameters(self):
        """
        Allows user to select heuristic and set other game parameters before starting the game.
        """
        print("Select AI heuristic (e0 = Material, e1 = Material + Position):")
        heuristic_choice = input("Enter 'e0' or 'e1': ").strip()
        if heuristic_choice not in ["e0", "e1"]:
            heuristic_choice = "e0"  # Default to e0 if invalid input
        
        self.game_parameters["heuristic"] = heuristic_choice
        print(f"Using heuristic: {heuristic_choice}")

    def execute_move(self, move_str, ai_stats=None):
        parsed_move = self.parse_input(move_str)
        start, end = parsed_move
        start_row, start_col = start
        end_row, end_col = end
        piece = self.current_game_state["board"][start_row][start_col]
        target_piece = self.current_game_state["board"][end_row][end_col]
    
        currentPlayer = self.current_game_state['turn'].capitalize()
    
        # Handle king capture win condition
        if target_piece in ["bK", "wK"]:
            winner = currentPlayer
            print(f"Game Over! {winner} wins by capturing the King.")
            self.moves_log.append(f"Turn {self.totalMoves + 1} ({currentPlayer}): move from {move_str}")
            save_game_trace(self.game_parameters, self.moves_log, f"{winner} (King Capture)", self.initial_board, self.board_snapshots)
            return True  # Game over

        # Track turn for draw condition (reset if capture occurs, increment otherwise)
        if target_piece != '.':
            self.turnNumber = 0
        else:
            self.turnNumber += 1

        # Increment total moves (done **after** checking draw condition)
        self.totalMoves += 1

        # Check for draw (no captures in 10 turns)
        if self.turnNumber >= 20:  # 10 turns = 20 moves (white + black)
            print("Game Over! It's a draw (10 turns without a capture).")
            save_game_trace(self.game_parameters, self.moves_log, "Draw (10 Turns No Capture)", self.initial_board, self.board_snapshots)
            return True  # Game over

        # Pawn promotion
        if piece in ["wp", "bp"] and ((piece == "wp" and end_row == 0) or (piece == "bp" and end_row == 4)):
            piece = piece[0] + "Q"

        # Execute the move
        self.current_game_state["board"][start_row][start_col] = '.'
        self.current_game_state["board"][end_row][end_col] = piece

        # Format move log correctly
        move_log = f"Turn {self.totalMoves} ({currentPlayer}): move from {move_str}"

        # If AI played the move, append relevant statistics
        if ai_stats:
            move_log += f" | time for this action: {ai_stats['time']:.3f} sec"
            move_log += f" | heuristic score: {ai_stats['heuristic_score']}"
            move_log += f" | alpha-beta search score: {ai_stats['score']}"

        # Save move logs and board snapshots
        self.moves_log.append(move_log)
        self.board_snapshots.append(f"Turn {self.totalMoves} ({currentPlayer}):\n{self.get_board_string(self.current_game_state['board'])}\n")

        # Switch turns
        self.current_game_state["turn"] = "black" if self.current_game_state["turn"] == "white" else "white"

        # Check for max turns
        if self.totalMoves >= self.game_parameters['max_turns']:
            print("Game Over! Reached maximum moves.")
            save_game_trace(self.game_parameters, self.moves_log, "Draw (Max Moves Reached)", self.initial_board, self.board_snapshots)
            return True  # Game over
        
        return False  # Game continues


    def format_states_by_depth(self):
        """Format the states explored by depth for display"""
        total = sum(self.states_by_depth.values())
        raw_data = []
        percentage_data = []
        
        for depth, count in sorted(self.states_by_depth.items()):
            # Format the count
            if count < 1000:
                count_str = str(count)
            elif count < 1000000:
                count_str = f"{count/1000:.1f}k"
            else:
                count_str = f"{count/1000000:.1f}M"
                
            raw_data.append(f"{depth}={count_str}")
            
            # Calculate and format the percentage
            percentage = (count / total) * 100
            percentage_data.append(f"{depth}={percentage:.1f}%")
            
        return " ".join(raw_data), " ".join(percentage_data)

    def format_total_states(self):
        """Format the total states explored for display"""
        if self.states_explored < 1000:
            return str(self.states_explored)
        elif self.states_explored < 1000000:
            return f"{self.states_explored/1000:.1f}k"
        else:
            return f"{self.states_explored/1000000:.1f}M"
        
    def timed_input(prompt, timeout):
        """Function to get input with timeout constraint from human player"""
        result=[None] # using a list to store input for thread

        def input_thread():
            result[0]=input(prompt) #store input in a list

        thread = threading.Thread(target=input_thread)
        thread.start()
        thread.join(timeout) #wait for input for the given time duration

        if thread.is_alive(): #if time runsout before input
            print("Time's up! You took too much time to make a move.")
            return None #timeout case
        return result[0]

    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        self.board_snapshots.append(f"Turn 0 (White):\n{self.get_board_string(self.current_game_state['board'])}\n")
        
        play_mode = self.game_parameters["play_mode"]
        white_is_ai = play_mode in ["AI-H", "AI-AI"]
        black_is_ai = play_mode in ["H-AI", "AI-AI"]
        
        time_limit =self.game_parameters["time_limit"] #read time limit from player input

        game_over = False
        
        while not game_over:
            self.display_board(self.current_game_state)
            currentPlayer = self.current_game_state['turn'].capitalize()
            print(f"{currentPlayer} to move:")
            
            # Determine if the current player is AI or human
            is_ai_turn = (self.current_game_state["turn"] == "white" and white_is_ai) or \
                          (self.current_game_state["turn"] == "black" and black_is_ai)
            
            if is_ai_turn:
                print("AI is thinking...")
                move_str, stats = self.get_ai_move(self.current_game_state)
                
                print(f"AI move: {move_str}")
                print(f"Time taken: {stats['time']:.3f} seconds")
                print(f"Depth reached: {stats['depth']}")
                print(f"Heuristic score: {stats['heuristic_score']}")
                print(f"Search score: {stats['score']}")
                
                # Format and display state exploration info
                total_states = self.format_total_states()
                states_by_depth, states_by_depth_percent = self.format_states_by_depth()
                
                print(f"States explored: {total_states}")
                print(f"States by depth: {states_by_depth}")
                print(f"States by depth (%): {states_by_depth_percent}")
                print(f"Average branching factor: {stats['avg_branching']:.2f}")
                
                game_over = self.execute_move(move_str)
            else:
                # Human turn
                move = self.timed_input("Enter your move (e.g. 'B2 B3') or type 'exit' to quit(You have {time_limit} seconds): ", time_limit)
                
                if move is None: #timeout occured
                    print (f"{currentPlayer} lost due to time expiration.")
                    winner = "Black" if currentPlayer == "White" else "White"
                    save_game_trace(self.game_parameters, self.moves_log, f"{winner} (Timeout)", self.initial_board, self.board_snapshots)
                    break #end the game


                if move.lower() == 'exit':
                    print("Game exited.")
                    break
                
                parsed_move = self.parse_input(move)
                if not parsed_move or parsed_move not in self.valid_moves(self.current_game_state):
                    print("Invalid move. Try again.")
                    continue
                
                game_over = self.execute_move(move)

if __name__ == "__main__":
    game = MiniChess()
    game.play()