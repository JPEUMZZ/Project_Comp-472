import argparse

def get_game_parameters():
    parser= argparse.ArgumentParser(description="Mini Chess Game Description")
    parser.add_argument("-t", "--time", type=int, required=True, help="Maxium time allowed per move (in seconds)" )
    parser.add_argument("-m", "--max_turns", type=int, required=True, help="Maximum number of turns before forced end")
    parser.add_argument("-a", "--alpha_beta", type=bool, required=True, help="Use alpha-beta pruning? (True/False)")
    parser.add_argument("-p", "--play_mode", type=str, choices=["H-H", "H-AI", "AI-H", "AI-AI"], required=True, help='Play mode: "H-H" (Human vs. Human), "H-AI"(Human vs. AI), etc.')

    args=parser.parse_args()

def save_game_trace(game_parameters, moves_log, winner):
    filename = f"gameTrace-{game_parameters['alpha_beta']}-{game_parameters['time_limit']}-{game_parameters['max_turns']}.txt"

    with open(filename, "w") as f:
        f.write(f"Game Parameters:\n")
        f.write(f"Timeout: {game_parameters['time_limit']} sec\n")
        f.write(f"Max Turns: {game_parameters['max_turns']}\n")
        f.write(f"Alpha-Beta Pruning: {game_parameters['alpha_beta']}\n")
        f.write(f"Play Mode: {game_parameters['play_mode']}\n\n")
        
        f.write("Game Moves:\n")
        for turn, move in enumerate(moves_log, start=1):
            f.write(f"Turn {turn}: {move}\n")
        
        f.write("\nGame Over!\n")
        f.write(f"Winner: {winner}\n")