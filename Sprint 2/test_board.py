import unittest

from board import BLOCK, PEG, EMPTY, is_valid_board, create_board


class TestBoardSizeValidation(unittest.TestCase):
    """Tests the supported board names and odd sizes starting at 7."""

    def test_supported_board_types_accept_size_seven(self):
        for board_type in ("english", "hexagon", "diamond"):
            with self.subTest(board_type=board_type):
                self.assertTrue(is_valid_board(board_type, 7))

    def test_odd_sizes_seven_and_above_are_valid(self):
        for size in (7, 9, 11, 13, 15, 17, 19):
            for board_type in ("english", "hexagon", "diamond"):
                with self.subTest(board_type=board_type, size=size):
                    self.assertTrue(is_valid_board(board_type, size))

    def test_sizes_below_seven_are_invalid(self):
        for size in (-1, 0, 1, 3, 5, 6):
            for board_type in ("english", "hexagon", "diamond"):
                with self.subTest(board_type=board_type, size=size):
                    self.assertFalse(is_valid_board(board_type, size))

    def test_even_sizes_are_invalid(self):
        for size in (8, 10, 12, 14, 20):
            for board_type in ("english", "hexagon", "diamond"):
                with self.subTest(board_type=board_type, size=size):
                    self.assertFalse(is_valid_board(board_type, size))

    def test_unknown_board_type_is_invalid(self):
        for board_type in ("square", "octagon", "", "triangle"):
            with self.subTest(board_type=board_type):
                self.assertFalse(is_valid_board(board_type, 7))

    def test_invalid_size_types_are_rejected(self):
        for size in ("7", 7.0, None, True):
            with self.subTest(size=size):
                self.assertFalse(is_valid_board("english", size))


class TestBoardCreation(unittest.TestCase):
    """Tests dimensions, center hole, and playable-cell shape for each board."""

    BOARD_TYPES = ("english", "hexagon", "diamond")

    def test_each_board_is_a_square_matrix_of_requested_size(self):
        for board_type in self.BOARD_TYPES:
            for size in (7, 9, 11):
                with self.subTest(board_type=board_type, size=size):
                    board = create_board(board_type, size)
                    self.assertEqual(len(board), size)
                    self.assertTrue(all(len(row) == size for row in board))

    def test_center_hole_starts_empty(self):
        for board_type in self.BOARD_TYPES:
            for size in (7, 9, 11):
                with self.subTest(board_type=board_type, size=size):
                    board = create_board(board_type, size)
                    center = size // 2
                    self.assertEqual(board[center][center], EMPTY)

    def test_all_cells_use_expected_symbols(self):
        allowed = {BLOCK, PEG, EMPTY}
        for board_type in self.BOARD_TYPES:
            board = create_board(board_type, 7)
            with self.subTest(board_type=board_type):
                self.assertTrue(all(cell in allowed for row in board for cell in row))

    def test_only_center_playable_hole_is_empty_initially(self):
        for board_type in self.BOARD_TYPES:
            board = create_board(board_type, 7)
            center = len(board) // 2
            empty_positions = [
                (r, c)
                for r, row in enumerate(board)
                for c, cell in enumerate(row)
                if cell == EMPTY
            ]
            self.assertEqual(empty_positions, [(center, center)])

    def test_english_board_has_three_wide_cross_arms(self):
        board = create_board("english", 7)
        # The top and bottom rows have three playable cells.
        self.assertEqual(sum(cell != BLOCK for cell in board[0]), 3)
        self.assertEqual(sum(cell != BLOCK for cell in board[-1]), 3)
        # Every cell in the middle row is playable.
        self.assertEqual(sum(cell != BLOCK for cell in board[3]), 7)
        # Middle column is playable in every row.
        self.assertTrue(all(board[row][3] != BLOCK for row in range(7)))

    def test_diamond_row_widths_for_size_seven(self):
        board = create_board("diamond", 7)
        widths = [sum(cell != BLOCK for cell in row) for row in board]
        self.assertEqual(widths, [1, 3, 5, 7, 5, 3, 1])

    def test_hexagon_row_widths_for_size_seven(self):
        board = create_board("hexagon", 7)
        widths = [sum(cell != BLOCK for cell in row) for row in board]
        self.assertEqual(widths, [3, 5, 7, 7, 7, 5, 3])

    def test_diamond_and_hexagon_are_not_same_shape(self):
        diamond = create_board("diamond", 7)
        hexagon = create_board("hexagon", 7)
        diamond_cells = sum(cell != BLOCK for row in diamond for cell in row)
        hexagon_cells = sum(cell != BLOCK for row in hexagon for cell in row)
        self.assertNotEqual(diamond_cells, hexagon_cells)

    def test_larger_sizes_expand_symmetrically(self):
        for board_type in self.BOARD_TYPES:
            for size in (9, 11, 13):
                with self.subTest(board_type=board_type, size=size):
                    board = create_board(board_type, size)
                    widths = [sum(cell != BLOCK for cell in row) for row in board]
                    self.assertEqual(widths, list(reversed(widths)))


class TestInvalidBoardCreation(unittest.TestCase):
    def test_invalid_board_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_board("octagon", 7)

    def test_even_size_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_board("english", 8)

    def test_size_below_seven_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_board("diamond", 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)

