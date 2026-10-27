from board import create_board, print_board, count_pegs
from moves import get_valid_moves, make_move
from game_over import is_game_over, get_game_result


def get_board_type():
    """Ask the player to select a board type."""
    while True:
        board_type = input(
            "Choose a board type (english, diamond, hexagon): "
        ).strip().lower()

        if board_type in {"english", "diamond", "hexagon"}:
            return board_type

        print("Invalid board type. Please try again.")


def get_board_size():
    """Ask for an odd board size of at least 7."""
    while True:
        try:
            size = int(input("Choose a board size (7 or larger, odd): "))

            if size >= 7 and size % 2 == 1:
                return size

            print("Size must be an odd number of at least 7.")

        except ValueError:
            print("Please enter a valid integer.")


def get_player_move(board, board_type):
    """Display legal moves and ask the player to choose one."""
    valid_moves = get_valid_moves(board, board_type)

    print("\nAvailable moves:")

    for index, move in enumerate(valid_moves, start=1):
        start_row, start_col, end_row, end_col = move
        print(
            f"{index}. ({start_row}, {start_col}) "
            f"-> ({end_row}, {end_col})"
        )

    while True:
        choice = input(
            "\nEnter a move number, or 'q' to quit: "
        ).strip().lower()

        if choice == "q":
            return None

        try:
            choice = int(choice)

            if 1 <= choice <= len(valid_moves):
                return valid_moves[choice - 1]

            print(f"Choose a number between 1 and {len(valid_moves)}.")

        except ValueError:
            print("Invalid input. Enter a move number or 'q'.")


def play_game():
    """Start and run one game session."""
    board_type = get_board_type()
    size = get_board_size()

    board = create_board(board_type, size)

    print("\nStarting board:")
    print_board(board)
    print(f"\nStarting pegs: {count_pegs(board)}")

    while not is_game_over(board, board_type):
        move = get_player_move(board, board_type)

        if move is None:
            print("\nGame session ended by player.")
            return

        make_move(board, board_type, move)

        print("\nBoard after move:")
        print_board(board)
        print(f"Remaining pegs: {count_pegs(board)}")

    print("\n" + get_game_result(board, board_type))


def start_game():
    """Provide the restart and quit menu."""
    print("Welcome to Peg Solitaire!")

    while True:
        play_game()

        print("\nWhat would you like to do?")
        print("1. Restart game")
        print("2. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\nStarting a new game...\n")
        elif choice == "2":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Starting a new game...\n")
