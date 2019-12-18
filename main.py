import sys
from typing import Optional, List, Tuple
from warnings import warn

import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets

from exploring import *
from gui.models import MainWindow
from maze import *


class ExploreManager(object):
    """
    Класс для описания исследования лабиринта
    """

    def __init__(self):
        self.maze: Optional[Maze] = None
        self.bot_list: Optional[List[Bot]] = None
        self.task_list: Optional[List[Tuple[int, int]]] = None
        self.running: bool = False

    def update_data(self, new_data):
        self.setup_simulation(bot_number=new_data[0],
                              height=new_data[1],
                              width=new_data[2])

    def setup_simulation(self,
                         manual_matrix: np.ndarray = None,
                         height: int = 25,
                         width: int = 25,
                         bot_number: int = 5,
                         starting_point: Tuple[int, int] = (1, 1)) -> None:
        """
        Parameters
        ----------
        manual_matrix : np.ndarray
            Матрица лабиринта, если не задана будет использована рандомная генерация
        height
            Высота лабиринта, используется во время рандомной генерации
        width
            Ширина лабиринта, используется во время рандомной генерации
        bot_number
            Количество ботов для исследования лабиринта
        starting_point
            Начальная точка для исследования (Место высадки первого бота)
        """

        # Создание лабиринта

        self.maze = Maze()
        if type(manual_matrix) == np.ndarray:
            self.maze.set_matrix_manually(manual_matrix)
        else:
            self.maze.set_matrix_randomly(height=height, width=width)

        # Создание списка ботов

        if bot_number < 1:
            warn('Количество ботов не может быть меньше 1. Будет использовано значение по умолчанию')
            bot_number: int = 5
        self.bot_list = [Bot(str(number)) for number in range(bot_number)]

        # Создание списка для хранения отложенных задач

        self.task_list = list()

        # Активация первого бота

        self.maze.change_block(starting_point, Maze.BOT_BLOCK)
        self.bot_list[0].activate(starting_point)

        self.running = True

    def get_active_bots(self) -> List[Bot]:
        """
            Метод для получения списка активных ботов
        Returns
        -------
        active_bots
            Список активных ботов
        """
        return list(filter(lambda bot: bot.status == Bot.ACTIVE_STATUS, self.bot_list))

    def get_waiting_bots(self) -> List[Bot]:
        """
            Метод для получения ожидающих ботов
        Returns
        -------
        waiting_bots
            Список ожидающих ботов
        """
        return list(filter(lambda bot: bot.status == Bot.WAITING_STATUS, self.bot_list))

    def exploring_step(self):
        """
        Метод, выполняющий 1 шаг исследования лабиринта
        Очередность действий во время шага:
        1) Каждый активный бот может перейти на следующую клетку, записать новую задачу в список
            или перейти в спящий режим, если нет возможности двигаться в неисследованную область
        2) Каждый спящий бот может активироваться для выполнения задач (если таковые имеются)
        """

        # Работа с активными ботами

        active_bots = self.get_active_bots()
        for bot in active_bots:
            bot_position = bot.position
            self.maze.change_block(bot_position, Maze.EXPLORED_BLOCK)
            got_task: bool = False

            if self.maze.matrix[bot_position[0] - 1, bot_position[1]] == Maze.UNEXPLORED_BLOCK:
                got_task = True
                bot.move_up()
                self.maze.change_block((bot_position[0] - 1, bot_position[1]), Maze.BOT_BLOCK)

            if self.maze.matrix[bot_position[0] + 1, bot_position[1]] == Maze.UNEXPLORED_BLOCK:
                if not got_task:
                    got_task = True
                    bot.move_down()
                    self.maze.change_block((bot_position[0] + 1, bot_position[1]), Maze.BOT_BLOCK)
                else:
                    self.task_list.append((bot_position[0] + 1, bot_position[1]))
                    self.maze.change_block((bot_position[0] + 1, bot_position[1]), Maze.PROCRASTINATED_BLOCK)

            if self.maze.matrix[bot_position[0], bot_position[1] - 1] == Maze.UNEXPLORED_BLOCK:
                if not got_task:
                    got_task = True
                    bot.move_left()
                    self.maze.change_block((bot_position[0], bot_position[1] - 1), Maze.BOT_BLOCK)
                else:
                    self.task_list.append((bot_position[0], bot_position[1] - 1))
                    self.maze.change_block((bot_position[0], bot_position[1] - 1), Maze.PROCRASTINATED_BLOCK)

            if self.maze.matrix[bot_position[0], bot_position[1] + 1] == Maze.UNEXPLORED_BLOCK:
                if not got_task:
                    got_task = True
                    bot.move_right()
                    self.maze.change_block((bot_position[0], bot_position[1] + 1), Maze.BOT_BLOCK)
                else:
                    self.task_list.append((bot_position[0], bot_position[1] + 1))
                    self.maze.change_block((bot_position[0], bot_position[1] + 1), Maze.PROCRASTINATED_BLOCK)

            if not got_task:
                bot.deactivate()

        # Работа со спящими ботами

        waiting_bots = self.get_waiting_bots()
        for bot in waiting_bots:
            if len(self.task_list) == 0:
                break
            task: Tuple[int, int] = self.task_list.pop(0)
            bot.activate(task)
            self.maze.change_block(task, Maze.BOT_BLOCK)

    def on_step_click(self):
        if self.running:
            self.exploring_step()
        else:
            warn('Входные параметры не заданны, выполнение невозможно')

    def on_reset_click(self):
        if self.maze is not None:
            self.maze.reset()
            self.setup_simulation(manual_matrix=self.maze.matrix)
        else:
            warn('Лабиринт не задан, сброс невозможен')


if __name__ == '__main__':
    em = ExploreManager()
    # while len(em.get_active_bots()) > 0:
    #     em.exploring_step()
    #     plt.imshow(em.maze.matrix)
    #     plt.pause(0.01)
    #     plt.clf()
    #
    # plt.imshow(em.maze.matrix)
    # plt.show()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(em)

    # window.link_start_btn()
    # window.link_stop_btn()
    window.link_step_btn(em.on_step_click)
    window.link_reset_btn(em.on_reset_click)
    window.link_new_maze_btn(window.setup_win.show)
    # window.link_save_btn()

    window.show()
    app.exec_()
