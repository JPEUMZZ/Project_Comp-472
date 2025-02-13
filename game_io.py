import argparse
import os

def get_game_parameters():
    parser = argparse.ArgumentParser(description="Mini Chess Game Description")
    parser.add_argument("-t", "--time", type=int, required=True, help="Maximum time allowed per move (in seconds)")
    parser.add_argument("-m", "--max_turns", type=int, required=True, help="Maximum number of turns before forced end")
    parser.add_argument("-a", "--alpha_beta", type=bool, required=True, help="Use alpha-beta pruning? (True/False)")
    parser.add_argument("-p", "--play_mode", type=str, choices=["H-H", "H-AI", "AI-H", "AI-AI"], required=True,
                        help='Play mode: "H-H" (Human vs. Human), "H-AI" (Human vs. AI), etc.')

    args = parser.parse_args()
    
    # Validate parsed arguments to prevent None issues
    if args.max_turns is None or args.time is None:
        raise ValueError("Missing required parameters: 'max_turns' or 'time'. Ensure arguments are passed correctly.")

    print(f"Game parameters loaded: time={args.time}, max_turns={args.max_turns}, alpha_beta={args.alpha_beta}, play_mode={args.play_mode}")

    return {
        "time_limit": args.time,
        "max_turns": args.max_turns,
        "alpha_beta": args.alpha_beta,
        "play_mode": args.play_mode
    }

def save_game_trace(game_parameters, moves_log, winner):
    output_folder = "game_traces"
    os.makedirs(output_folder, exist_ok=True)

    filename = f"{output_folder}/gameTrace-{game_parameters['alpha_beta']}-{game_parameters['time_limit']}-{game_parameters['max_turns']}.txt"
    
    try:
        with open(filename, "w") as f:
            f.write("Game Parameters:\n")
            f.write(f"Timeout: {game_parameters['time_limit']} sec\n")
            f.write(f"Max Turns: {game_parameters['max_turns']}\n")
            f.write(f"Alpha-Beta Pruning: {game_parameters['alpha_beta']}\n")
            f.write(f"Play Mode: {game_parameters['play_mode']}\n\n")

            f.write("Game Moves:\n")
            for turn, move in enumerate(moves_log, start=1):
                f.write(f"Turn {turn}: {move}\n")

            f.write("\nGame Over!\n")
            f.write(f"Winner: {winner}\n")

        print(f"Game trace successfully saved to: {filename}")
    except Exception as e:
        print(f"Failed to save game trace: {e}")