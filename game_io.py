import argparse
import os
import sys
from io import StringIO

def get_game_parameters():
    parser = argparse.ArgumentParser(description="Mini Chess Game Description")
    parser.add_argument("-t", "--time", type=int, required=True, help="Maximum time allowed per move (in seconds)")
    parser.add_argument("-m", "--max_turns", type=int, required=True, help="Maximum number of turns before forced end")
    parser.add_argument("-a", "--alpha_beta", type=bool, required=True, help="Use alpha-beta pruning? (True/False)")
    parser.add_argument("-p", "--play_mode", type=str, choices=["H-H", "H-AI", "AI-H", "AI-AI"], required=True,
                        help='Play mode: "H-H" (Human vs. Human), "H-AI" (Human vs. AI), etc.')
    parser.add_argument("-e", "--heuristic", type=str, choices=["e0", "e1", "e2"], required=False, default="e0",
                        help="Heuristic function to use: e0, e1, or e2")

    args = parser.parse_args()

    if args.max_turns is None or args.time is None:
        raise ValueError("Missing required parameters: 'max_turns' or 'time'. Ensure arguments are passed correctly.")

    print(f"Game parameters loaded: time={args.time}, max_turns={args.max_turns}, alpha_beta={args.alpha_beta}, play_mode={args.play_mode}, heuristic={args.heuristic}")

    return {
        "time_limit": args.time,
        "max_turns": args.max_turns,
        "alpha_beta": args.alpha_beta,
        "play_mode": args.play_mode,
        "heuristic": args.heuristic,
        "initial_board": [],
    }

def save_game_trace(game_parameters, moves_log, winner, initial_board=None, board_snapshots=None, ai_statistics=None):
    output_folder = "game_traces"
    os.makedirs(output_folder, exist_ok=True)

    filename = f"{output_folder}/gameTrace-{game_parameters['alpha_beta']}-{game_parameters['time_limit']}-{game_parameters['max_turns']}.txt"

    try:
        with open(filename, "w") as f:
            f.write("Game Parameters:\n")
            f.write(f"Timeout: {game_parameters['time_limit']} sec\n")
            f.write(f"Max Turns: {game_parameters['max_turns']}\n")
            f.write(f"Alpha-Beta Pruning: {game_parameters['alpha_beta']}\n")
            f.write(f"Play Mode: {game_parameters['play_mode']}\n")
            f.write(f"Heuristic: {game_parameters['heuristic']}\n\n")

            # Record Initial Board
            f.write("Initial Board Configuration:\n")
            if initial_board:
                for row in initial_board:
                    f.write(' '.join(row) + '\n')
            else:
                f.write("[Initial board not recorded]\n")

            # Record Each Turn’s Board Configuration
            if board_snapshots:
                f.write("\nBoard Configuration After Each Move:\n")
                for snapshot in board_snapshots:
                    f.write(snapshot + "\n")

            # Record Moves
            f.write("\nGame Moves:\n")
            for move_entry in moves_log:
                f.write(move_entry + "\n")

            # If AI statistics are available, save cumulative statistics
            if ai_statistics:
                f.write("\nCumulative AI Statistics:\n")
                f.write(f"Cumulative states explored: {ai_statistics['states_explored']}\n")
                f.write(f"Cumulative states explored by depth: {ai_statistics['states_by_depth']}\n")
                f.write(f"Cumulative % states explored by depth: {ai_statistics['states_by_depth_percent']}\n")
                f.write(f"Average branching factor: {ai_statistics['avg_branching']:.2f}\n")

            # Record Winner
            f.write(f"\nGame Over!\nWinner: {winner} (after {len(moves_log)} turns)\n")

            print(f"Game trace successfully saved to: {filename}")

    except Exception as e:
        print(f"Failed to save game trace: {e}")
