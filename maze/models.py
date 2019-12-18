from random import choice
from typing import Optional, Tuple
from warnings import warn

import matplotlib.pyplot as plt
import numpy as np


class Maze(object):
    WALL_BLOCK = -1
    UNEXPLORED_BLOCK = 0
    PROCRASTINATED_BLOCK = 1
    EXPLORED_BLOCK = 2
    BOT_BLOCK = 3

    def __init__(self):
        self.__matrix: Optional[np.ndarray] = None

    @property
    def matrix(self) -> np.ndarray:
        """
        Геттер для матрицы

        Returns
        -------
        matrix : np.ndarray
            Матрица лабиринта
        """
        return self.__matrix

    @property
    def height(self) -> int:
        """
        Геттер для высоты матрицы

        Returns
        -------
        height : int
            Высота матрицы
        """
        return self.__matrix.shape[0]

    @property
    def width(self) -> int:
        """
        Геттер для ширины матрицы

        Returns
        -------
        width : int
            Ширина матрицы
        """
        return self.__matrix.shape[1]

    def set_matrix_randomly(self, height: int = 25, width: int = 25) -> None:
        """
        Рандомная генерация матрицы

        Parameters
        ----------
        height : int
            Высота генерируемой матрицы
        width : int
            Ширина генерируемой матрицы

        References
        ----------
        https://habr.com/ru/post/262345/
        """

        # Валидация входных данных

        if height < 2:
            warn('Высота лабиринта не может быть меньше 2. '
                 'Будет использовано значение по умолчанию')
            height = 25
        if width < 2:
            warn('Ширина лабиринта не может быть меньше 2. '
                 'Будет использовано значение по умолчанию')
            width = 25
        if height % 2 == 0:
            warn('Высота лабиринта не может быть четной. '
                 'Значение будет увеличено на 1')
            height += 1
        if width % 2 == 0:
            warn('Ширина лабиринта не может быть четной. '
                 'Значение будет увеличено на 1')
            width += 1

        # Генерация начального темплейта

        self.__matrix = np.zeros((height, width))
        for height_idx in range(height):
            for width_idx in range(width):
                if (height_idx % 2 != 0) and (width_idx % 2 != 0):
                    self.__matrix[height_idx, width_idx] = Maze.UNEXPLORED_BLOCK
                else:
                    self.__matrix[height_idx, width_idx] = Maze.WALL_BLOCK

        # Создание коридоров в начальном темплейте

        current_point = (1, 1)
        visit_set = set()
        history_list = []
        while len(visit_set) < (width // 2) * (height // 2):
            visit_set.add(current_point)
            neighbours = []

            if current_point[0] != 1 and (current_point[0] - 2, current_point[1]) not in visit_set:
                neighbours.append((current_point[0] - 2, current_point[1]))
            if current_point[0] != height - 2 and (current_point[0] + 2, current_point[1]) not in visit_set:
                neighbours.append((current_point[0] + 2, current_point[1]))
            if current_point[1] != 1 and (current_point[0], current_point[1] - 2) not in visit_set:
                neighbours.append((current_point[0], current_point[1] - 2))
            if current_point[1] != width - 2 and (current_point[0], current_point[1] + 2) not in visit_set:
                neighbours.append((current_point[0], current_point[1] + 2))

            if len(neighbours) == 0:
                current_point = history_list.pop()
            else:
                history_list.append(current_point)
                next_point = choice(neighbours)

                self.__matrix[(current_point[0] + next_point[0]) // 2,
                              (current_point[1] + next_point[1]) // 2] = Maze.UNEXPLORED_BLOCK

                current_point = next_point

    def set_matrix_manually(self, matrix: np.ndarray) -> None:
        """
        Установка матрицы вручную

        Parameters
        ----------
        matrix : np.ndarray
            Матрица лабиринта
        """
        self.__matrix = matrix

    def change_block(self, coordinates: Tuple[int, int], new_block: int) -> None:
        """
        Метод для изменения типа блока лабиринта

        Parameters
        ----------
        coordinates : tuple of int
            Координаты необходимго блока
        new_block : int
            Новый статус блока
        """
        self.__matrix[coordinates] = new_block

    def reset(self):
        if self.__matrix is not None:
            for height_idx in range(self.height):
                for width_idx in range(self.width):
                    if self.matrix[height_idx, width_idx] != -1:
                        self.matrix[height_idx, width_idx] = 0


if __name__ == '__main__':
    mz = Maze()

    # Рандомная генерация матрицы

    mz.set_matrix_randomly(25, 25)
    plt.imshow(mz.matrix)
    plt.show()

    # Ручная установка матрицы

    mz.set_matrix_manually(np.array([[0, 0, 0, 0, 0],
                                     [0, 1, 0, 1, 0],
                                     [0, 1, 1, 1, 0],
                                     [0, 1, 0, 1, 0],
                                     [0, 0, 0, 0, 0]
                                     ]))
    plt.imshow(mz.matrix)
    plt.show()
