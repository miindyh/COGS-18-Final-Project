"""
test_sudoku.py

This file has tests to make sure the Sudoku game in sudoku.py works correctly.
It uses Python's 'unittest' module to check different parts of the game.

What is tested:
1. load_puzzle: Checks that the board has 9 rows and 9 columns, and loads 'easy' if we type a wrong difficulty.
2. is_valid: Checks that we do not put duplicate numbers in the same row, column, or 3x3 box.
3. make_move: Checks that we can place numbers, cannot change locked start numbers, and cannot make bad moves.
4. is_solved: Checks that the game knows when the puzzle is completely finished.
5. Wrong Input Detection: Checks that the solver works and that players cannot make moves that make the game unsolvable later.
"""
## AI assisted code##
import unittest
from sudoku import SudokuBoard, load_puzzle


class TestLoadPuzzle(unittest.TestCase):
    """Tests for the load_puzzle function."""

    def test_returns_9_rows(self):
        """load_puzzle returns a grid with 9 rows."""
        puzzle = load_puzzle('easy')
        self.assertEqual(len(puzzle), 9)

    def test_each_row_has_9_columns(self):
        """Each row in the puzzle has 9 columns."""
        puzzle = load_puzzle('easy')
        self.assertEqual(len(puzzle[0]), 9)

    def test_unknown_difficulty_returns_easy(self):
        """load_puzzle falls back to easy if difficulty is not recognized."""
        puzzle = load_puzzle('unknown')
        self.assertEqual(len(puzzle), 9)


class TestIsValid(unittest.TestCase):
    """Tests for the is_valid method."""

    def setUp(self):
        # Create a fresh board before each test
        self.board = SudokuBoard(load_puzzle('easy'))

    def test_valid_move_returns_true(self):
        """is_valid returns True when a move is allowed."""
        self.assertTrue(self.board.is_valid(0, 2, 1))

    def test_number_in_same_row_returns_false(self):
        """is_valid returns False when the number is already in that row."""
        # Row 0 already has a 5
        self.assertFalse(self.board.is_valid(0, 2, 5))

    def test_number_in_same_column_returns_false(self):
        """is_valid returns False when the number is already in that column."""
        # Column 0 already has a 5
        self.assertFalse(self.board.is_valid(2, 0, 5))

    def test_number_in_same_box_returns_false(self):
        """is_valid returns False when the number is already in the 3x3 box."""
        # Top left box already has 5, 3, 6, 9, 8
        self.assertFalse(self.board.is_valid(0, 2, 9))


class TestMakeMove(unittest.TestCase):
    """Tests for the make_move method."""

    def setUp(self):
        self.board = SudokuBoard(load_puzzle('easy'))

    def test_valid_move_is_placed(self):
        """make_move places the number and returns True for a valid move."""
        result = self.board.make_move(0, 2, 4)
        self.assertTrue(result)
        self.assertEqual(self.board.grid[0][2], 4)

    def test_locked_cell_returns_false(self):
        """make_move returns False when trying to change a locked cell."""
        # Cell (0, 0) is 5 in the original puzzle - it is locked
        result = self.board.make_move(0, 0, 9)
        self.assertFalse(result)

    def test_invalid_move_returns_false(self):
        """make_move returns False when the move breaks Sudoku rules."""
        # 5 is already in row 0
        result = self.board.make_move(0, 2, 5)
        self.assertFalse(result)


class TestIsSolved(unittest.TestCase):
    """Tests for the is_solved method."""

    def test_unsolved_board_returns_false(self):
        """is_solved returns False when the board still has empty cells."""
        board = SudokuBoard(load_puzzle('easy'))
        self.assertFalse(board.is_solved())

    def test_solved_board_returns_true(self):
        """is_solved returns True when every cell is filled in."""
        solved_puzzle = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        board = SudokuBoard(solved_puzzle)
        self.assertTrue(board.is_solved())


class TestWrongInputDetection(unittest.TestCase):
    """Tests for wrong input detection using the Sudoku solver."""

    def test_solve_easy_puzzle(self):
        """The solver should pre-calculate the correct solution for easy difficulty."""
        board = SudokuBoard(load_puzzle('easy'))
        self.assertIsNotNone(board.solution)
        # Verify the solution is fully solved and valid
        self.assertTrue(board._solve(board.solution))

    def test_correct_move_accepted(self):
        """make_move should accept a correct move matching the pre-solved solution."""
        board = SudokuBoard(load_puzzle('easy'))
        correct_val = board.solution[0][2]
        self.assertTrue(board.make_move(0, 2, correct_val))
        self.assertEqual(board.grid[0][2], correct_val)

    def test_incorrect_locally_valid_move_rejected(self):
        """make_move should reject a locally valid but incorrect move."""
        board = SudokuBoard(load_puzzle('easy'))
        # Placing 1 at (0, 2) is locally valid under Sudoku constraints
        self.assertTrue(board.is_valid(0, 2, 1))
        # But correct solution has 4 in (0, 2), so 1 is incorrect
        self.assertNotEqual(board.solution[0][2], 1)
        # make_move should reject it
        self.assertFalse(board.make_move(0, 2, 1))
        self.assertEqual(board.grid[0][2], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    