from moves import has_valid_moves
from board import count_pegs


def is_game_over(board, board_type):
    """Return True when no valid moves remain."""
    return not has_valid_moves(board, board_type)


def is_winner(board):
    """Return True when exactly one peg remains."""
    return count_pegs(board) == 1


def get_game_result(board, board_type):
    """Return a message describing the game's result."""
    if not is_game_over(board, board_type):
        return "Game is still in progress."

    if is_winner(board):
        return "Congratulations! You won!"

    return "Game over! No valid moves remain."
