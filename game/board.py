import enum
from typing import List, Tuple, Optional


@enum.unique
class CellType(enum.Enum):
    UNKNOWN = -1
    EMPTY = 0,
    MINES_CLOSE_1 = 1,
    MINES_CLOSE_2 = 2,
    MINES_CLOSE_3 = 3,
    MINES_CLOSE_4 = 4,
    MINES_CLOSE_5 = 5,
    MINES_CLOSE_6 = 6,
    MINES_CLOSE_7 = 7,
    MINES_CLOSE_8 = 8,
    MINE = 9


class GameBoard(object):
    __CELL_REPRESENTATION = {
        CellType.UNKNOWN: "U",
        CellType.EMPTY: " ",
        CellType.MINES_CLOSE_1: "1",
        CellType.MINES_CLOSE_2: "2",
        CellType.MINES_CLOSE_3: "3",
        CellType.MINES_CLOSE_4: "4",
        CellType.MINES_CLOSE_5: "5",
        CellType.MINES_CLOSE_6: "6",
        CellType.MINES_CLOSE_7: "7",
        CellType.MINES_CLOSE_8: "8",
        CellType.MINE: "\u2716"
    }

    def __init__(self, rows: int, columns: int):
        """
        Class constructor

        :param rows: Number of rows of the grid
        :param columns: Number of columns of the grid
        """

        self._rows = rows
        self._columns = columns
        self._visibility = [[False for _ in range(columns)] for _ in range(rows)]
        self._internal = [[CellType.EMPTY for _ in range(columns)] for _ in range(rows)]

    def __setitem__(self, position: Tuple[int, int], cell_type: CellType):
        """
        Sets the cell type for an specific position

        :param position: Position of the cell
        :param cell_type: Type of the cell
        """

        row, column = position
        self._internal[row][column] = cell_type

    def __getitem__(self, position: Tuple[int, int]) -> CellType:
        """
        Returns the cell type in an specific position

        :param position: Position of the cell
        :return: Cell type
        """

        row, column = position
        return self._internal[row][column]

    def get(self, row: int, column: int) -> Optional[CellType]:
        """
        Safely returns the cell type in an specific position

        :param row: Cell row
        :param column: Cell column
        :return: Cell type if given position is valid, None otherwise
        """

        if row < 0 or row >= self._rows or \
           column < 0 or column >= self._columns:
            return None

        return self._internal[row][column]

    def is_visible(self, row: int, column: int):
        """Returns whether a cell is visible or not"""

        return self._visibility[row][column]

    @property
    def internal_state(self) -> List[List[CellType]]:
        """
        Return the internal state
        """

        return self._internal

    @property
    def external_state(self) -> List[List[CellType]]:
        """
        Return the external state
        """

        return [[
            cell_type if self._visibility[r][c] else CellType.UNKNOWN
            for c, cell_type in enumerate(row)]
            for r, row in enumerate(self._internal)]

    def reveal(self, row: int, column: int):
        """
        Reveals cell in the given position

        :return: Number of cells revealed
        """

        if row < 0 or row >= self._rows or \
           column < 0 or column >= self._columns or \
           self._visibility[row][column]:
            return 0

        revealed = 1
        self._visibility[row][column] = True
        if self._internal[row][column] == CellType.EMPTY:
            rl, rp = row - 1, row + 1
            cl, cp = column - 1, column + 1

            for r, c in (
                (rl, cl), (rl, column), (rl, cp),
                (row, cl), (row, cp),
                (rp, cl), (rp, column), (rp, cp)
            ):
                revealed += self.reveal(r, c)

        return revealed

    def __repr__(self):
        """Returns game board representation"""

        internal_repr = "\n".join("|" + "|".join(self.__CELL_REPRESENTATION[cell_type]
                                                 for cell_type in row) + "|"
                                  for row in self.internal_state)

        external_repr = "\n".join("|" + "|".join(self.__CELL_REPRESENTATION[cell_type]
                                                 for cell_type in row) + "|"
                                  for row in self.external_state)

        return "Board dimensions: {}x{}\n" \
               "Internal representation:\n" \
               "{}\n\n" \
               "External representation:\n" \
               "{}\n".format(self._rows, self._columns, internal_repr, external_repr)

    def __str__(self):
        """Returns game board formatted as a string"""

        return "\n".join("|" + "|".join(self.__CELL_REPRESENTATION[cell_type]
                                        for cell_type in row) + "|" for row in self._internal)
