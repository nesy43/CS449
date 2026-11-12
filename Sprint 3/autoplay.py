import random
from copy import deepcopy

from moves import get_valid_moves, make_move
from game_over import is_game_over, is_winner


def autoplay_game(board, board_type, on_move=None,
                  chooser=None, max_moves=None):
    """ PLay a random move on the board until no moves are left on the board """

    current = deepcopy(board)
    history = []

    choose = chooser or random.choice

    while not is_game_over(current, board_type):

        if max_moves is not None and len(history) >= max_moves:
            break

        legal_moves = get_valid_moves(current, board_type)

        if not legal_moves:
            break

        move = choose(legal_moves)

        if move not in legal_moves:
            raise ValueError("The selected move is not legal.")

        if not make_move(current, board_type, move):
            raise RuntimeError("Could not apply a legal move.")

        move = tuple(move)
        history.append(move)

        if on_move is not None:
            on_move(deepcopy(current), move, len(history))

    return current, history


def autoplay_summary(final_board, board_type):
    """Return a message describing the autoplay result."""

    if is_winner(final_board):
        return "Autoplay finished: You won!"

    if is_game_over(final_board, board_type):
        return "Autoplay finished: No legal moves remain."

    return "Autoplay stopped before the game ended."
