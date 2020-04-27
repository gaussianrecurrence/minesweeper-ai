import random

from game.board import (
    GameBoard,
    CellType
)


class GameBoardGenerator(object):

    __NEARBY_MINES_TO_CELL_TYPE = (
        CellType.MINES_CLOSE_1,
        CellType.MINES_CLOSE_2,
        CellType.MINES_CLOSE_3,
        CellType.MINES_CLOSE_4,
        CellType.MINES_CLOSE_5,
        CellType.MINES_CLOSE_6,
        CellType.MINES_CLOSE_7,
        CellType.MINES_CLOSE_8,
    )

    def __init__(self, rows: int, columns: int, mines_percent: float):
        """
        Class constructor

        :param rows: Number of rows of the grid
        :param columns: Number of columns of the grid
        :param mines_percent: Percentage of mines in the grid
        """

        self._rows = rows
        self._columns = columns
        self._mines = int(mines_percent * rows * columns)

    def __call__(self) -> GameBoard:
        """
        Generates a new random board
        """

        while True:
            yield self._generate()

    def _generate(self) -> GameBoard:

        board = GameBoard(self._rows, self._columns)
        positions = [(r, c) for c in range(self._columns) for r in range(self._rows)]

        random.shuffle(positions)
        for r, c in positions[:self._mines]:
            board[r, c] = CellType.MINE

        self.__update_nearby_mines(board)

        return board

    def __update_nearby_mines(self, board):

        for row in range(self._rows):
            for column in range(self._columns):

                if board[row, column] == CellType.MINE:
                    continue

                mines = 0
                rl, rp = row - 1, row + 1
                cl, cp = column - 1, column + 1

                for r, c in (
                        (rl, cl), (rl, column), (rl, cp),
                        (row, cl), (row, cp),
                        (rp, cl), (rp, column), (rp, cp)
                ):
                    if board.get(r, c) == CellType.MINE:
                        mines += 1

                if mines > 0:
                    board[row, column] = self.__NEARBY_MINES_TO_CELL_TYPE[mines-1]
