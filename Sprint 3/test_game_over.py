import unittest

from board import BLOCK, PEG, EMPTY, create_board, count_pegs
from game_over import is_game_over, is_winner, get_game_result


def empty_test_board(size=7):
    """Create a board with all cells blocked."""
    return [[BLOCK for _ in range(size)] for _ in range(size)]


class TestIsGameOver(unittest.TestCase):

    def test_game_over_when_no_moves_are_available(self):
        board = empty_test_board()
        board[3][3] = PEG

        self.assertTrue(is_game_over(board, "english"))

    def test_game_not_over_when_a_valid_move_exists(self):
        board = empty_test_board()
        board[3][1] = PEG
        board[3][2] = PEG
        board[3][3] = EMPTY

        self.assertFalse(is_game_over(board, "english"))

    def test_game_over_with_one_peg(self):
        board = empty_test_board()
        board[3][3] = PEG

        self.assertTrue(is_game_over(board, "english"))

    def test_game_over_with_no_pegs(self):
        board = empty_test_board()

        self.assertTrue(is_game_over(board, "english"))

    def test_hexagon_diagonal_move_prevents_game_over(self):
        board = empty_test_board()
        board[1][1] = PEG
        board[2][2] = PEG
        board[3][3] = EMPTY

        self.assertFalse(is_game_over(board, "hexagon"))

    def test_hexagon_game_over_when_no_diagonal_or_other_moves_exist(self):
        board = empty_test_board()
        board[3][3] = PEG

        self.assertTrue(is_game_over(board, "hexagon"))


class TestIsWinner(unittest.TestCase):

    def test_one_peg_is_a_win(self):
        board = empty_test_board()
        board[3][3] = PEG

        self.assertTrue(is_winner(board))

    def test_multiple_pegs_are_not_a_win(self):
        board = empty_test_board()
        board[3][3] = PEG
        board[3][4] = PEG

        self.assertFalse(is_winner(board))

    def test_no_pegs_are_not_a_win(self):
        board = empty_test_board()

        self.assertFalse(is_winner(board))

    def test_winner_does_not_depend_on_peg_location(self):
        board = empty_test_board()
        board[0][0] = PEG

        self.assertTrue(is_winner(board))


class TestGetGameResult(unittest.TestCase):

    def test_one_peg_and_no_moves_is_won(self):
        board = empty_test_board()
        board[3][3] = PEG

        result = get_game_result(board, "english")

        self.assertIn("won", result.lower())

    def test_multiple_pegs_and_no_moves_is_lost(self):
        board = empty_test_board()
        board[0][0] = PEG
        board[6][6] = PEG

        result = get_game_result(board, "english")

        self.assertIn("game over", result.lower())
        self.assertIn("No", result)

    def test_game_in_progress_is_not_over(self):
        board = empty_test_board()
        board[3][1] = PEG
        board[3][2] = PEG
        board[3][3] = EMPTY

        result = get_game_result(board, "english")

        self.assertIn("progress", result.lower())

    def test_hexagon_diagonal_move_keeps_game_in_progress(self):
        board = empty_test_board()
        board[1][1] = PEG
        board[2][2] = PEG
        board[3][3] = EMPTY

        result = get_game_result(board, "hexagon")

        self.assertIn("progress", result.lower())


class TestInitialBoards(unittest.TestCase):

    def test_initial_english_board_is_not_over(self):
        board = create_board("english", 7)

        self.assertFalse(is_game_over(board, "english"))

    def test_initial_diamond_board_is_not_over(self):
        board = create_board("diamond", 7)

        self.assertFalse(is_game_over(board, "diamond"))

    def test_initial_hexagon_board_is_not_over(self):
        board = create_board("hexagon", 7)

        self.assertFalse(is_game_over(board, "hexagon"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
