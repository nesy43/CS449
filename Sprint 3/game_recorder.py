import json
from pathlib import Path

from board import create_board
from moves import get_valid_moves, make_move


FORMAT_VERSION = 1


def save_game(filename, board_type, size, moves):
    """ Save a game to a JSON file, allow the user to name the file"""
    data = {
        "format": "peg-solitaire-replay",
        "version": FORMAT_VERSION,
        "board_type": board_type,
        "size": size,
        "moves": [list(move) for move in moves]
    }

    path = Path(filename)

    with path.open("w", encoding="utf-8") as output:
        json.dump(data, output, indent=2)
        output.write("\n")

    return path


def load_game(filename):
    """Load and validate a saved game file."""

    with Path(filename).open("r", encoding="utf-8") as source:
        data = json.load(source)

    required = {
        "format",
        "version",
        "board_type",
        "size",
        "moves"
    }

    if not isinstance(data, dict):
        raise ValueError("Invalid replay file.")

    if not required.issubset(data):
        raise ValueError("Replay file is missing required fields.")

    if data["format"] != "peg-solitaire-replay":
        raise ValueError("This is not a Peg Solitaire replay file.")

    if data["version"] != FORMAT_VERSION:
        raise ValueError("Unsupported replay file version.")

    if not isinstance(data["moves"], list):
        raise ValueError("Replay moves must be a list.")

    return data


def replay_game(filename, on_move=None):
    """ Take the game from the loaded file and play it out """

    from copy import deepcopy

    data = load_game(filename)

    board = create_board(
        data["board_type"],
        data["size"]
    )

    history = []

    for number, raw_move in enumerate(data["moves"], start=1):

        if not isinstance(raw_move, list) or len(raw_move) != 4:
            raise ValueError(
                f"Invalid move format at move {number}."
            )

        move = tuple(raw_move)

        legal_moves = get_valid_moves(
            board,
            data["board_type"]
        )

        if move not in legal_moves:
            raise ValueError(
                f"Recorded move {number} is not legal: {move}"
            )

        if not make_move(board, data["board_type"], move):
            raise ValueError(
                f"Could not apply recorded move {number}."
            )

        history.append(move)

        if on_move is not None:
            on_move(deepcopy(board), move, number)

    return board, history
