import unittest

from board import BLOCK, PEG, EMPTY, count_pegs
from moves import get_valid_moves, has_valid_moves, make_move


def empty_test_board(size=7):
    """Create a board with all cells blocked."""
    return [[BLOCK for _ in range(size)] for _ in range(size)]


def setup_jump(board, source, middle, target):
    """Set up a jump with a peg, a peg to jump over, and an empty target."""
    sr, sc = source
    mr, mc = middle
    tr, tc = target

    board[sr][sc] = PEG
    board[mr][mc] = PEG
    board[tr][tc] = EMPTY

    return (sr, sc, tr, tc)


class TestValidMoves(unittest.TestCase):

    def test_horizontal_move_english(self):
        board = empty_test_board()
        move = setup_jump(board, (3, 1), (3, 2), (3, 3))

        self.assertIn(move, get_valid_moves(board, "english"))

    def test_horizontal_move_diamond(self):
        board = empty_test_board()
        move = setup_jump(board, (3, 1), (3, 2), (3, 3))

        self.assertIn(move, get_valid_moves(board, "diamond"))

    def test_horizontal_move_hexagon(self):
        board = empty_test_board()
        move = setup_jump(board, (3, 1), (3, 2), (3, 3))

        self.assertIn(move, get_valid_moves(board, "hexagon"))

    def test_vertical_move(self):
        board = empty_test_board()
        move = setup_jump(board, (1, 3), (2, 3), (3, 3))

        for board_type in ("english", "diamond", "hexagon"):
            with self.subTest(board_type=board_type):
                self.assertIn(
                    move,
                    get_valid_moves(board, board_type)
                )

    def test_hexagon_allows_down_right_diagonal(self):
        board = empty_test_board()
        move = setup_jump(board, (1, 1), (2, 2), (3, 3))

        self.assertIn(move, get_valid_moves(board, "hexagon"))

    def test_hexagon_allows_all_four_diagonal_directions(self):
        directions = [
            (-1, -1),  # Up-left
            (-1, 1),   # Up-right
            (1, -1),   # Down-left
            (1, 1),    # Down-right
        ]

        for dr, dc in directions:
            with self.subTest(direction=(dr, dc)):
                board = empty_test_board()

                source = (3, 3)
                middle = (3 + dr, 3 + dc)
                target = (3 + 2 * dr, 3 + 2 * dc)

                move = setup_jump(board, source, middle, target)

                self.assertIn(
                    move,
                    get_valid_moves(board, "hexagon")
                )

    def test_english_rejects_diagonal_move(self):
        board = empty_test_board()
        move = setup_jump(board, (1, 1), (2, 2), (3, 3))

        self.assertNotIn(move, get_valid_moves(board, "english"))

    def test_diamond_rejects_diagonal_move(self):
        board = empty_test_board()
        move = setup_jump(board, (1, 1), (2, 2), (3, 3))

        self.assertNotIn(move, get_valid_moves(board, "diamond"))

    def test_jump_must_be_exactly_two_cells(self):
        board = empty_test_board()
        board[3][1] = PEG
        board[3][2] = PEG
        board[3][4] = EMPTY

        move = (3, 1, 3, 4)

        self.assertNotIn(move, get_valid_moves(board, "hexagon"))

    def test_middle_cell_must_contain_peg(self):
        board = empty_test_board()
        board[3][1] = PEG
        board[3][2] = EMPTY
        board[3][3] = EMPTY

        move = (3, 1, 3, 3)

        self.assertNotIn(move, get_valid_moves(board, "english"))

    def test_destination_must_be_empty(self):
        board = empty_test_board()
        board[3][1] = PEG
        board[3][2] = PEG
        board[3][3] = PEG

        move = (3, 1, 3, 3)

        self.assertNotIn(move, get_valid_moves(board, "english"))

    def test_source_must_contain_peg(self):
        board = empty_test_board()
        board[3][1] = EMPTY
        board[3][2] = PEG
        board[3][3] = EMPTY

        move = (3, 1, 3, 3)

        self.assertNotIn(move, get_valid_moves(board, "english"))

    def test_move_outside_board_is_invalid(self):
        board = empty_test_board()
        board[0][0] = PEG
        board[0][1] = PEG

        move = (0, 0, 0, 2)

        self.assertNotIn(move, get_valid_moves(board, "hexagon"))


class TestMakeMove(unittest.TestCase):

    def test_successful_move_updates_cells(self):
        board = empty_test_board()
        move = setup_jump(board, (3, 1), (3, 2), (3, 3))

        result = make_move(board, "english", move)

        self.assertTrue(result)
        self.assertEqual(board[3][1], EMPTY)
        self.assertEqual(board[3][2], EMPTY)
        self.assertEqual(board[3][3], PEG)

    def test_successful_move_removes_one_peg(self):
        board = empty_test_board()
        move = setup_jump(board, (3, 1), (3, 2), (3, 3))

        pegs_before = count_pegs(board)

        make_move(board, "english", move)

        self.assertEqual(count_pegs(board), pegs_before - 1)

    def test_diagonal_hexagon_move_updates_cells(self):
        board = empty_test_board()
        move = setup_jump(board, (1, 1), (2, 2), (3, 3))

        result = make_move(board, "hexagon", move)

        self.assertTrue(result)
        self.assertEqual(board[1][1], EMPTY)
        self.assertEqual(board[2][2], EMPTY)
        self.assertEqual(board[3][3], PEG)

    def test_diagonal_hexagon_move_removes_one_peg(self):
        board = empty_test_board()
        move = setup_jump(board, (1, 1), (2, 2), (3, 3))

        pegs_before = count_pegs(board)

        make_move(board, "hexagon", move)

        self.assertEqual(count_pegs(board), pegs_before - 1)

    def test_invalid_move_does_not_change_board(self):
        board = empty_test_board()
        board[3][1] = PEG
        board[3][2] = EMPTY
        board[3][3] = EMPTY

        original_board = [row[:] for row in board]

        result = make_move(board, "english", (3, 1, 3, 3))

        self.assertFalse(result)
        self.assertEqual(board, original_board)

    def test_english_rejects_diagonal_move_execution(self):
        board = empty_test_board()
        move = setup_jump(board, (1, 1), (2, 2), (3, 3))

        result = make_move(board, "english", move)

        self.assertFalse(result)

    def test_diamond_rejects_diagonal_move_execution(self):
        board = empty_test_board()
        move = setup_jump(board, (1, 1), (2, 2), (3, 3))

        result = make_move(board, "diamond", move)

        self.assertFalse(result)


class TestMoveAvailability(unittest.TestCase):

    def test_has_valid_moves_returns_true(self):
        board = empty_test_board()
        setup_jump(board, (3, 1), (3, 2), (3, 3))

        self.assertTrue(has_valid_moves(board, "english"))

    def test_has_valid_moves_returns_false(self):
        board = empty_test_board()
        board[3][3] = PEG

        self.assertFalse(has_valid_moves(board, "english"))

    def test_hexagon_diagonal_counts_as_available_move(self):
        board = empty_test_board()
        setup_jump(board, (1, 1), (2, 2), (3, 3))

        self.assertTrue(has_valid_moves(board, "hexagon"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
