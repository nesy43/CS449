
from board import PEG, EMPTY

ORTHOGONAL_DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

DIAGONAL_DIRECTIONS = [
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]


def get_directions(board_type):
    """Return the allowed jump directions for a board type."""
    if board_type.lower() == "hexagon":
        return ORTHOGONAL_DIRECTIONS + DIAGONAL_DIRECTIONS

    return ORTHOGONAL_DIRECTIONS


def get_valid_moves(board, board_type):
    """
    Return all legal moves as tuples:
    (start_row, start_col, end_row, end_col).
    """
    moves = []
    size = len(board)
    directions = get_directions(board_type)

    for row in range(size):
        for col in range(size):
            if board[row][col] != PEG:
                continue

            for dr, dc in directions:
                middle_row = row + dr
                middle_col = col + dc
                target_row = row + 2 * dr
                target_col = col + 2 * dc

                if not (
                    0 <= middle_row < size
                    and 0 <= middle_col < size
                    and 0 <= target_row < size
                    and 0 <= target_col < size
                ):
                    continue

                if board[middle_row][middle_col] != PEG:
                    continue

                if board[target_row][target_col] != EMPTY:
                    continue

                moves.append(
                    (row, col, target_row, target_col)
                )

    return moves


def has_valid_moves(board, board_type):
    """Return True if at least one legal move remains."""
    return bool(get_valid_moves(board, board_type))


def make_move(board, board_type, move):
    """Execute a legal move. Return True if successful."""
    if move not in get_valid_moves(board, board_type):
        return False

    start_row, start_col, end_row, end_col = move

    middle_row = (start_row + end_row) // 2
    middle_col = (start_col + end_col) // 2

    board[start_row][start_col] = EMPTY
    board[middle_row][middle_col] = EMPTY
    board[end_row][end_col] = PEG

    return True
