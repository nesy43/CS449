BLOCK = " "
PEG = "P"
EMPTY = "."

BOARD_TYPES = {"english", "diamond", "hexagon"}


def is_valid_board(board_type, size):
    """Check whether the board type and size are supported."""
    if not isinstance(board_type, str):
        return False

    if not isinstance(size, int) or isinstance(size, bool):
        return False

    return (
        board_type in BOARD_TYPES
        and size >= 7
        and size % 2 == 1
    )


def create_board(board_type, size):
    """Create a peg solitaire board as a 2D matrix."""

    if not is_valid_board(board_type, size):
        raise ValueError("Invalid board type or size")

    # Start with a matrix containing only blocked cells.
    board = [
        [BLOCK for _ in range(size)]
        for _ in range(size)
    ]

    center = size // 2

    for row in range(size):
        for col in range(size):

            playable = False

            if board_type == "english":
                # Three-hole-wide horizontal and vertical arms.
                playable = (
                    abs(row - center) <= 1
                    or abs(col - center) <= 1
                )

            elif board_type == "diamond":
                # Manhattan distance from the center.
                playable = (
                    abs(row - center) + abs(col - center)
                    <= center
                )

            elif board_type == "hexagon":
                # DIstance from the center row
                distance = abs(row - center)

                start_col = max(0, distance - 1)
                end_col = size - start_col
                
                playable = (
                    start_col <= col < end_col
                )

            if playable:
                board[row][col] = PEG

    # Start with the center hole empty.
    board[center][center] = EMPTY

    return board


def print_board(board):
    """Display the matrix in the terminal."""
    for row in board:
        print(" ".join(row))


def count_pegs(board):
    """Return the number of pegs remaining on the board."""
    return sum(cell == PEG for row in board for cell in row)
