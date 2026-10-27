import unittest

from board import BLOCK, PEG, EMPTY, create_board, is_valid_board, count_pegs


class TestCreateGame(unittest.TestCase):

    def test_create_english_game(self):
        board = create_board("english", 7)

        self.assertEqual(len(board), 7)
        self.assertTrue(all(len(row) == 7 for row in board))

    def test_create_diamond_game(self):
        board = create_board("diamond", 7)

        self.assertEqual(len(board), 7)
        self.assertTrue(all(len(row) == 7 for row in board))

    def test_create_hexagon_game(self):
        board = create_board("hexagon", 7)

        self.assertEqual(len(board), 7)
        self.assertTrue(all(len(row) == 7 for row in board))

    def test_game_starts_with_one_empty_playable_hole(self):
        for board_type in ("english", "diamond", "hexagon"):
            with self.subTest(board_type=board_type):
                board = create_board(board_type, 7)

                empty_cells = sum(
                    cell == EMPTY
                    for row in board
                    for cell in row
                )

                self.assertEqual(empty_cells, 1)

    def test_game_starts_with_pegs(self):
        for board_type in ("english", "diamond", "hexagon"):
            with self.subTest(board_type=board_type):
                board = create_board(board_type, 7)

                self.assertGreater(count_pegs(board), 0)

    def test_center_hole_starts_empty(self):
        for board_type in ("english", "diamond", "hexagon"):
            with self.subTest(board_type=board_type):
                board = create_board(board_type, 7)
                center = len(board) // 2

                self.assertEqual(board[center][center], EMPTY)

    def test_game_uses_only_valid_cell_symbols(self):
        allowed_symbols = {BLOCK, PEG, EMPTY}

        for board_type in ("english", "diamond", "hexagon"):
            with self.subTest(board_type=board_type):
                board = create_board(board_type, 7)

                for row in board:
                    for cell in row:
                        self.assertIn(cell, allowed_symbols)

    def test_larger_game_size(self):
        board = create_board("english", 9)

        self.assertEqual(len(board), 9)
        self.assertTrue(all(len(row) == 9 for row in board))

    def test_invalid_board_type_is_rejected(self):
        with self.assertRaises(ValueError):
            create_board("triangle", 7)

    def test_even_board_size_is_rejected(self):
        with self.assertRaises(ValueError):
            create_board("english", 8)

    def test_board_size_below_minimum_is_rejected(self):
        with self.assertRaises(ValueError):
            create_board("english", 5)

    def test_invalid_size_type_is_rejected(self):
        for size in ("7", 7.0, None, True):
            with self.subTest(size=size):
                with self.assertRaises((ValueError, TypeError)):
                    create_board("english", size)


if __name__ == "__main__":
    unittest.main(verbosity=2)
