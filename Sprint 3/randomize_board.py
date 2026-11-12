import random
from copy import deepcopy

from board import create_board
from moves import get_valid_moves, make_move

def randomize_existing_board(board, board_type, steps=5, seed=None):
    """ Take the existing board and perform random moves on it to create a random state """
    if steps is not None and (
        not isinstance(steps, int) or isinstance(steps, bool) or steps < 0
    ):
        raise ValueError("Steps must be a non-negative integer or None.")

    rng = random.Random(seed)
    result = deepcopy(board)
    history = []

    if steps is None:
        initial_moves = get_valid_moves(result, board_type)
        steps = rng.randint(1, len(initial_moves)) if initial_moves else 0

    for _ in range(steps):
        legal_moves = get_valid_moves(result, board_type)
        if not legal_moves:
            break

        move = tuple(rng.choice(legal_moves))
        if not make_move(result, board_type, move):
            raise RuntimeError("Could not apply a legal move.")
        history.append(move)

    return result, history
