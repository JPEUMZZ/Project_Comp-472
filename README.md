# Mini chess
Mini Chess is a simplified 2-player chess variant played on a 5×5 board. The game is inspired by standard chess but features a reduced number of pieces and simplified rules. The objective is to capture the opponent's king.
Each player (White and Black) has 6 pieces:

### King (K): Moves 1 square in any direction. Capturing the opponent's King wins the game.

### Queen (Q): Moves any number of squares in any direction.

### Bishop (B): Moves diagonally until blocked.

### Knight (N): Moves in an L-shape (2 squares in one direction + 1 perpendicular).

### Pawns (p): Each player has 2 pawns. They move 1 square forward and capture diagonally. Pawns promote to a Queen upon reaching the last row.

# Initial Board Setup

| 5  | bK  | bQ  | bB  | bN  | .  |
|----|----|----|----|----|----|
| 4  | .  | .  | bp | bp | .  |
| 3  | .  | .  | .  | .  | .  |
| 2  | .  | wp | wp | .  | .  |
| 1  | wN  | wB  | wQ  | wK  | .  |
|    | A  | B  | C  | D  | E  |

# Game rules
Each turn, a player moves one piece.

Capturing occurs when a piece moves onto an opponent's piece.

Kings can move into check and be captured.

No check/checkmate rules (game ends when a King is captured).

No castling, en passant, or pawn double-moves.

The game follows a 10-move draw rule (if no piece is captured in 10 turns, it's a draw).

# Winning and Draw Conditions

### Win: 
Capturing the opponent's King.

### Draw:
10 turns without a capture. Max move limit reached (if implemented in game parameters).

Features Implemented

# Game Mechanics

Board Initialization

Turn-Based Move System

Move Validation (per piece type)

King Capture Detection (Winning Condition)

Pawn Promotion (to Queen)

Draw Condition (10 moves without capture)

Move Logging & Board Snapshots (for game trace)

# Code Enhancements

Fixed bishop and queen moves to prevent jumping over pieces.

Ensured valid captures (no capturing same-color pieces).

Added automatic game termination upon King capture.

Refactored pawn promotion logic to correctly transform a pawn into a Queen.

# How to Play

To run the game, input this command in your terminal:

python MiniChessSkeletonCode.py -t (time) -m (# of turns) -a (True or false) -p (play mode)

so an example of this would be:

python MiniChessSkeletonCode.py -t 5 -m 100 -a False -p H-H

The command above means that the time given for each move is 5 seconds only, there is a maximum of 100 moves, alpha-beta is set to false and the play mode is Human vs. Human.

Once the game starts, you can run and enter moves in algebraic notation (e.g., B2 B3).

During the game:

White goes first.

Moves are input as start_position end_position (e.g., C4 C3).

Type exit to quit.

# Group Members
### Mengqi Tong: 
- Game rules and move validation: 
- Implemented King capture logic. The game ends immediately when a King is taken.
- Added pawn promotion. Pawns reaching the last row are automatically converted to a Queen.
- Implemented a 10-turn draw rule. If no capture happens in 10 moves, the game ends in a draw.
- Implemented The Heuristic e1.
- Updated ai_move function.
### Thaneekan Thankarajah:
- Implemented input parameters for the game such as timeout options, maximum amount of turns, play mode, etc.
- Trace file:
- Captured every turn by players in the proper sequence of time. 
- Board initialization and capture. The resulting trace file captures the board's appearance at the moment of each turn.
- A recap of who won the game and in how many turns.
### Junior Peumi:
- Implement movement rules for each piece
- Implement move validation
