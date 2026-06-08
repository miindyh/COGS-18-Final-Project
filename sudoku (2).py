"""
sudoku.py

A text-based Sudoku game module.
Contains functions and a class to run a playable Sudoku game.
"""

## AI assisted code##
def load_puzzle(difficulty='easy'):
    """
    Return a hardcoded Sudoku puzzle based on difficulty.

    Parameters
    ----------
    difficulty : str
        The difficulty level - 'easy', 'medium', or 'hard'.

    Returns
    -------
    list
        A 9x9 list of lists. 0 means the cell is empty.

    Examples
    --------
    >>> puzzle = load_puzzle('easy')
    >>> len(puzzle)
    9
    """
    easy = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    medium = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]

    hard = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]
    ]

    # Return the right puzzle based on difficulty
    if difficulty == 'easy':
        return easy
    elif difficulty == 'medium':
        return medium
    elif difficulty == 'hard':
        return hard
    else:
        print("Difficulty not found. Loading easy instead.")
        return easy


class SudokuBoard:
    """
    A class that stores the Sudoku board and handles game logic.

    Parameters
    ----------
    puzzle : list
        A 9x9 list of lists. 0 means the cell is empty.
    """

    def __init__(self, puzzle):
        # Save the original puzzle so we know which cells are locked
        self.original = [row[:] for row in puzzle]
        # This is the board the player edits
        self.grid = [row[:] for row in puzzle]
        # Pre-solve the puzzle to keep a reference solution for incorrect move detection
        temp_grid = [row[:] for row in puzzle]
        if self._solve(temp_grid):
            self.solution = temp_grid
        else:
            self.solution = None

    def _is_valid_in_grid(self, grid, row, col, num):
        """Helper to check if a number is valid in a specific grid copy (used by solver)."""
        # Check row
        if num in grid[row]:
            return False

        # Check column
        for r in range(9):
            if grid[r][col] == num:
                return False

        # Check box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if grid[r][c] == num:
                    return False

        return True

    def _solve(self, grid):
        """Helper to solve a grid copy in-place using backtracking. Returns True if solved."""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    for num in range(1, 10):
                        if self._is_valid_in_grid(grid, r, c, num):
                            grid[r][c] = num
                            if self._solve(grid):
                                return True
                            grid[r][c] = 0
                    return False
        return True

    def display(self):
        """
        Print the board so the player can see it.

        Examples
        --------
        >>> board = SudokuBoard(load_puzzle('easy'))
        >>> board.display()  # doctest: +SKIP
        """
        # Print column numbers across the top
        print("\n   1  2  3     4  5  6     7  8  9")
        print("  ---------   ---------   ---------")

        for i in range(9):
            row_display = str(i + 1) + " "

            for j in range(9):
                # Add a divider between each 3x3 box
                if j == 3 or j == 6:
                    row_display += " | "

                # Show a dot for empty cells
                # Show brackets around original numbers, plain for player's numbers
                if self.grid[i][j] == 0:
                    row_display += " . "
                elif self.original[i][j] != 0:
                    row_display += "[" + str(self.grid[i][j]) + "]"
                else:
                    row_display += " " + str(self.grid[i][j]) + " "

            print(row_display)

            # Add a divider row between each 3x3 box
            if i == 2 or i == 5:
                print("  ---------   ---------   ---------")

        print()

    def is_valid(self, row, col, num):
        """
        Check if a number can legally be placed at a given cell.

        Parameters
        ----------
        row : int
            Row index (0-8).
        col : int
            Column index (0-8).
        num : int
            The number to place (1-9).

        Returns
        -------
        bool
            True if the move is allowed, False if it breaks a rule.

        Examples
        --------
        >>> board = SudokuBoard(load_puzzle('easy'))
        >>> board.is_valid(0, 2, 1)
        True
        >>> board.is_valid(0, 2, 5)
        False
        """
        # Check if the number is already in the same row
        if num in self.grid[row]:
            return False

        # Check if the number is already in the same column
        for r in range(9):
            if self.grid[r][col] == num:
                return False

        # Check if the number is already in the same 3x3 box
        # Find the top-left corner of the box this cell belongs to
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3

        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.grid[r][c] == num:
                    return False

        # If none of the checks failed, the move is valid
        return True

    def make_move(self, row, col, num):
        """
        Place a number on the board if the move is valid.

        Parameters
        ----------
        row : int
            Row index (0-8).
        col : int
            Column index (0-8).
        num : int
            The number to place (1-9).

        Returns
        -------
        bool
            True if the number was placed, False if the move was rejected.

        Examples
        --------
        >>> board = SudokuBoard(load_puzzle('easy'))
        >>> board.make_move(0, 2, 1)
        True
        >>> board.make_move(0, 0, 9)
        False
        """
        # Don't allow changes to cells that came with the original puzzle
        if self.original[row][col] != 0:
            print("That cell is locked. You can only fill in empty cells.")
            return False

        # Don't allow moves that break Sudoku rules
        if not self.is_valid(row, col, num):
            print(f"{num} cannot go in row {row + 1}, col {col + 1}. Try again.")
            return False

        # Don't allow moves that lead to an unsolvable puzzle (deviating from correct solution)
        if self.solution and self.solution[row][col] != num:
            print(f"{num} cannot go in row {row + 1}, col {col + 1}. Try a different number!")
            return False

        # Place the number on the board
        self.grid[row][col] = num
        return True

    def is_solved(self):
        """
        Check if the puzzle is completely filled in.

        Returns
        -------
        bool
            True if all cells are filled, False if there are still empty cells.

        Examples
        --------
        >>> board = SudokuBoard(load_puzzle('easy'))
        >>> board.is_solved()
        False
        """
        for row in range(9):
            for col in range(9):
                # If any cell is still 0, the puzzle is not done
                if self.grid[row][col] == 0:
                    return False
        return True


def get_user_move():
    """
    Ask the player for their next move and keep asking until they give valid input.

    Returns
    -------
    tuple or None
        A tuple of (row, col, num) converted to 0-indexed, or None if the player quits.
    """
    while True:
        user_input = input("Enter row col number (e.g. 1 3 7), or q to quit: ").strip()

        # Let the player quit
        if user_input.lower() == 'q':
            return None

        # Split the input into parts
        parts = user_input.split()

        # Make sure they entered exactly 3 values
        if len(parts) != 3:
            print("Please enter three numbers separated by spaces. Example: 1 3 7")
            continue

        # Make sure all three values are actually numbers
        try:
            row = int(parts[0]) - 1  # convert to 0-indexed
            col = int(parts[1]) - 1  # convert to 0-indexed
            num = int(parts[2])
        except ValueError:
            print("Those don't look like numbers. Try again.")
            continue

        # Make sure the values are within the valid range
        if not (0 <= row <= 8 and 0 <= col <= 8 and 1 <= num <= 9):
            print("Row and column must be between 1 and 9. Number must be between 1 and 9.")
            continue

        return (row, col, num)


def play_game(difficulty='easy'):
    """
    Run the full Sudoku game from start to finish.

    Parameters
    ----------
    difficulty : str
        The difficulty level - 'easy', 'medium', or 'hard'.
    """
    print(f"\nStarting Sudoku - {difficulty} mode!")
    print("Enter your move as: row col number")
    print("Example: 1 3 7 means place 7 in row 1, column 3")
    print("Type q to quit.\n")

    # Load the puzzle and create the board
    puzzle = load_puzzle(difficulty)
    board = SudokuBoard(puzzle)
    board.display()

    # Keep going until the puzzle is solved or the player quits
    while not board.is_solved():
        move = get_user_move()

        # Player chose to quit
        if move is None:
            print("Thanks for playing!")
            break

        row, col, num = move

        # If the move was valid, show the updated board
        if board.make_move(row, col, num):
            board.display()

    # Congratulate the player if they finished
    if board.is_solved():
        print("You solved it! Great job!")