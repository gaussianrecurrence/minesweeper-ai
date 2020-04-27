import random
import numpy as np
from typing import Tuple

from game.board import (
    CellType,
    GameBoard
)
from game.generator import GameBoardGenerator


class DatasetGenerator(GameBoardGenerator):
    __NUMBER_OF_CLASSES = 10

    __CELL_TYPE_TO_LABEL = {
        CellType.EMPTY: 1.,
        CellType.MINES_CLOSE_1: 8./9.,
        CellType.MINES_CLOSE_2: 7./9.,
        CellType.MINES_CLOSE_3: 6./9.,
        CellType.MINES_CLOSE_4: 5./9.,
        CellType.MINES_CLOSE_5: 4./9.,
        CellType.MINES_CLOSE_6: 3./9.,
        CellType.MINES_CLOSE_7: 2./9.,
        CellType.MINES_CLOSE_8: 1./9.,
        CellType.MINE: 0.,
    }

    __CELL_TYPE_TO_ONE_HOT = {
        CellType.EMPTY: np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32),
        CellType.UNKNOWN: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=np.float32),
        CellType.MINES_CLOSE_1: np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32),
        CellType.MINES_CLOSE_2: np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32),
        CellType.MINES_CLOSE_3: np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0], dtype=np.float32),
        CellType.MINES_CLOSE_4: np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0], dtype=np.float32),
        CellType.MINES_CLOSE_5: np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0], dtype=np.float32),
        CellType.MINES_CLOSE_6: np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0], dtype=np.float32),
        CellType.MINES_CLOSE_7: np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0], dtype=np.float32),
        CellType.MINES_CLOSE_8: np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0], dtype=np.float32)
    }

    def __init__(self, rows: int, columns: int, mines_percent: float, batch_size: int):
        """
        Class
        :param rows: Number of rows of the grid
        :param columns: Number of columns of the grid
        :param mines_percent: Percentage of mines in the grid
        :param batch_size: Size of the batch to be generated
        """

        self._batch_size = batch_size
        GameBoardGenerator.__init__(self, rows, columns, mines_percent)

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates a new random dataset entry
        """

        x = np.zeros((self._batch_size, self._rows, self._columns,
                      self.__NUMBER_OF_CLASSES), dtype=np.float32)
        y = np.zeros((self._batch_size, self._rows, self._columns), dtype=np.float32)

        for i in range(self._batch_size):
            x[i], y[i] = self._generate()

        return x, y

    def _generate(self) -> Tuple[np.ndarray, np.ndarray]:

        board = GameBoardGenerator._generate(self)
        self.__reveal_board(board, np.random.random())

        external_state = board.external_state
        x = np.zeros((self._rows, self._columns,
                      self.__NUMBER_OF_CLASSES), dtype=np.float32)
        y = np.zeros((self._rows, self._columns), dtype=np.float32)

        for r in range(self._rows):
            for c in range(self._columns):
                y[r, c] = self.__CELL_TYPE_TO_LABEL[board[r, c]]
                x[r, c] = self.__CELL_TYPE_TO_ONE_HOT[external_state[r][c]]

        return x, y

    def __reveal_board(self, board: GameBoard, reveal_percent: float):

        cells_to_reveal = int(reveal_percent * (self._rows * self._columns - self._mines))
        positions = [(r, c) for c in range(self._columns) for r in range(self._rows)]
        random.shuffle(positions)
        cells_revealed = 0

        for r, c in positions:
            if board[r, c] != CellType.MINE and not board.is_visible(r, c):
                cells_revealed += board.reveal(r, c)
                if cells_revealed >= cells_to_reveal:
                    break

