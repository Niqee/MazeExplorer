import sys
from time import sleep
from tkinter import filedialog
from typing import Optional, List, Tuple
from warnings import warn

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets

from exploring import *
from gui.models import MainWindow
from maze import *


class ExploreManager(object):
    """
    Класс для описания исследования лабиринта
    """
    WALL_COLOR = (12, 22, 57)
    UNEXPLORED_COLOR = (162, 162, 162)
    PROCRASTINATED_COLOR = (245, 170, 42)
    EXPLORED_COLOR = (90, 160, 90)
    BOT_COLOR = (252, 26, 26)

    START_COLOR_G = (0.6, 0.6, 0.6)
    PROCRASTINATED_COLOR_G = (0.96, 0.67, 0.16)
    EXPLORED_COLOR_G = (0.35, 0.63, 0.35)
    BOT_COLOR_G = (0.99, 0.1, 0.1)

    def __init__(self):
        self.maze: Optional[Maze] = None
        self.bot_list: Optional[List[Bot]] = None
        self.task_list: Optional[List[Tuple[int, int]]] = None
        self.graph: Optional[nx.Graph] = None
        self.ready: bool = False
        plt.ion()
        self.matrix_img = None
        self.graph_colormap: Optional[pd.DataFrame] = None
        self.graph_ax = None
        self.step = 0

    def update_data(self,
                    new_bot_num: int,
                    new_height: int = None,
                    new_width: int = None,
                    new_manual_matrix: np.ndarray = None):
        """
        Метод для обновления симуляции

        Parameters
        ----------
        new_bot_num : int
            Новое количество ботов
        new_height : int
            Новая вертикаль
        new_width : int
            Новая горизонталь
        new_manual_matrix :int
            Новая матрица
        """
        if new_manual_matrix is not None:
            self.setup_simulation(bot_number=new_bot_num,
                                  manual_matrix=new_manual_matrix)
        else:
            self.setup_simulation(bot_number=new_bot_num,
                                  height=new_height,
                                  width=new_width)
        self.show_matrix(hard=True)

    def show_matrix(self, hard: bool = False):
        """
        Метод для вывода лабиринта

        Parameters
        ----------
        hard : bool
            Если True то график будет полностью сброшен перед отображением
        """
        show_matrix = np.zeros(self.maze.matrix.shape + tuple([3]))
        for height_idx in range(self.maze.height):
            for width_idx in range(self.maze.width):
                if self.maze.matrix[height_idx, width_idx] == Maze.WALL_BLOCK:
                    show_matrix[height_idx, width_idx, :] = ExploreManager.WALL_COLOR
                elif self.maze.matrix[height_idx, width_idx] == Maze.UNEXPLORED_BLOCK:
                    show_matrix[height_idx, width_idx, :] = ExploreManager.UNEXPLORED_COLOR
                elif self.maze.matrix[height_idx, width_idx] == Maze.EXPLORED_BLOCK:
                    show_matrix[height_idx, width_idx, :] = ExploreManager.EXPLORED_COLOR
                elif self.maze.matrix[height_idx, width_idx] == Maze.PROCRASTINATED_BLOCK:
                    show_matrix[height_idx, width_idx, :] = ExploreManager.PROCRASTINATED_COLOR
                else:
                    show_matrix[height_idx, width_idx, :] = ExploreManager.BOT_COLOR

        if self.matrix_img is None or hard:
            if self.matrix_img is not None:
                plt.close()
            fig, (matrix_ax, self.graph_ax) = plt.subplots(ncols=2, figsize=(5, 5))
            fig.set_size_inches(10, 5)

            self.matrix_img = matrix_ax.imshow(show_matrix.astype(np.uint8))
        else:
            self.matrix_img.set_data(show_matrix.astype(np.uint8))
            self.graph_ax.clear()
        nx.draw_kamada_kawai(self.graph, ax=self.graph_ax, with_labels=True, node_color=self.graph_colormap['color'])
        plt.draw()
        plt.pause(0.01)

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

        self.graph = nx.Graph()
        self.graph_colormap = pd.DataFrame(
            {'id': [str((-1, -1)), str(starting_point)], 'color': [self.START_COLOR_G, self.BOT_COLOR_G]}).set_index(
            'id')
        self.graph.add_edge((-1, -1), starting_point)

        self.step = 1

        self.ready = True

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
            self.graph_colormap.loc[str(bot_position), 'color'] = self.EXPLORED_COLOR_G
            got_task: bool = False

            if self.maze.matrix[bot_position[0] - 1, bot_position[1]] == Maze.UNEXPLORED_BLOCK:
                got_task = True
                bot.move_up()
                self.maze.change_block((bot_position[0] - 1, bot_position[1]), Maze.BOT_BLOCK)
                self.graph.add_edge(bot_position, bot.position)
                new_node = pd.DataFrame([{'id': str(bot.position), 'color': self.BOT_COLOR_G}]).set_index('id')
                self.graph_colormap = self.graph_colormap.append(new_node)

            if self.maze.matrix[bot_position[0] + 1, bot_position[1]] == Maze.UNEXPLORED_BLOCK:
                if not got_task:
                    got_task = True
                    bot.move_down()
                    self.maze.change_block((bot_position[0] + 1, bot_position[1]), Maze.BOT_BLOCK)
                    self.graph.add_edge(bot_position, bot.position)
                    new_node = pd.DataFrame([{'id': str(bot.position), 'color': self.BOT_COLOR_G}]).set_index('id')
                else:
                    self.task_list.append((bot_position[0] + 1, bot_position[1]))
                    self.maze.change_block((bot_position[0] + 1, bot_position[1]), Maze.PROCRASTINATED_BLOCK)
                    self.graph.add_edge(bot_position, (bot_position[0] + 1, bot_position[1]))
                    new_node = pd.DataFrame(
                        [{'id': str((bot_position[0] + 1, bot_position[1])),
                          'color': self.PROCRASTINATED_COLOR_G}]).set_index('id')
                self.graph_colormap = self.graph_colormap.append(new_node)

            if self.maze.matrix[bot_position[0], bot_position[1] - 1] == Maze.UNEXPLORED_BLOCK:
                if not got_task:
                    got_task = True
                    bot.move_left()
                    self.maze.change_block((bot_position[0], bot_position[1] - 1), Maze.BOT_BLOCK)
                    self.graph.add_edge(bot_position, bot.position)
                    new_node = pd.DataFrame([{'id': str(bot.position), 'color': self.BOT_COLOR_G}]).set_index('id')
                else:
                    self.task_list.append((bot_position[0], bot_position[1] - 1))
                    self.maze.change_block((bot_position[0], bot_position[1] - 1), Maze.PROCRASTINATED_BLOCK)
                    self.graph.add_edge(bot_position, (bot_position[0], bot_position[1] - 1))
                    new_node = pd.DataFrame(
                        [{'id': str((bot_position[0], bot_position[1] - 1)),
                          'color': self.PROCRASTINATED_COLOR_G}]).set_index('id')
                self.graph_colormap = self.graph_colormap.append(new_node)

            if self.maze.matrix[bot_position[0], bot_position[1] + 1] == Maze.UNEXPLORED_BLOCK:
                if not got_task:
                    got_task = True
                    bot.move_right()
                    self.maze.change_block((bot_position[0], bot_position[1] + 1), Maze.BOT_BLOCK)
                    self.graph.add_edge(bot_position, bot.position)
                    new_node = pd.DataFrame([{'id': str(bot.position), 'color': self.BOT_COLOR_G}]).set_index('id')
                else:
                    self.task_list.append((bot_position[0], bot_position[1] + 1))
                    self.maze.change_block((bot_position[0], bot_position[1] + 1), Maze.PROCRASTINATED_BLOCK)
                    self.graph.add_edge(bot_position, (bot_position[0], bot_position[1] + 1))
                    new_node = pd.DataFrame(
                        [{'id': str((bot_position[0], bot_position[1] + 1)),
                          'color': self.PROCRASTINATED_COLOR_G}]).set_index('id')
                self.graph_colormap = self.graph_colormap.append(new_node)

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
            self.graph_colormap.loc[str(bot.position), 'color'] = self.BOT_COLOR_G

        self.step += 1

    def get_step(self) -> int:
        """
        Метод для получения номера текущего хода

        Returns
        -------
        step : int
            Номер текущего хода
        """
        return self.step

    def get_progress(self) -> float:
        """
        Метод для получения текущего прогресса

        Returns
        -------
        progress : float
            Текущий прогресс
        """
        not_wall_num = np.sum(self.maze.matrix != Maze.WALL_BLOCK)
        explored_num = np.sum(self.maze.matrix == Maze.EXPLORED_BLOCK)
        return explored_num / not_wall_num

    def on_step_click(self, win: MainWindow):
        """
        Метод, вызывающийся при нажатии на кнопку "Шаг"

        Parameters
        ----------
        win : MainWindow
            Обьект главного окна
        """
        sleep(0.1)
        if not self.ready:
            warn('Входные параметры не заданны, выполнение невозможно')
        elif self.get_progress() == 1:
            warn('Лабиринт пройден')
        else:
            self.exploring_step()
            win.update_step(self.step)
            win.update_progress(self.get_progress())
            self.show_matrix()

    def on_reset_click(self, win: MainWindow):
        """
        Метод, вызывающийся при нажатии на кнопку "Сброс"

        Parameters
        ----------
        win : MainWindow
            Обьект главного окна
        """
        sleep(0.1)
        if self.maze is not None:
            self.maze.reset()
            self.setup_simulation(manual_matrix=self.maze.matrix)
            win.update_step(self.step)
            win.update_progress(self.get_progress())
            self.show_matrix()
        else:
            warn('Лабиринт не задан, сброс невозможен')

    def on_save_click(self):
        """
        Метод, вызывающийся при нажатии на кнопку "Сохранить лабиринт"
        """
        sleep(0.1)
        if self.maze is None:
            warn('Лабиринт не задан, сохранение невозможно')
            return
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is not None:
            save_matrix = self.maze.matrix
            for h_idx in range(self.maze.height):
                for w_idx in range(self.maze.width):
                    save_matrix[h_idx, w_idx] = Maze.WALL_BLOCK \
                        if self.maze.matrix[h_idx, w_idx] == Maze.WALL_BLOCK \
                        else Maze.UNEXPLORED_BLOCK
            # noinspection PyTypeChecker
            np.savetxt(f, save_matrix)
            f.close()

    def on_step20_click(self, win):
        """
        Метод, вызывающийся при нажатии на кнопку "20 Шагов"

        Parameters
        ----------
        win : MainWindow
            Обьект главного окна
        """
        sleep(0.1)
        for i in range(20):
            self.on_step_click(win)

    def on_step10_click(self, win):
        """
        Метод, вызывающийся при нажатии на кнопку "10 Шагов"

        Parameters
        ----------
        win : MainWindow
            Обьект главного окна
        """
        sleep(0.1)
        for i in range(10):
            self.on_step_click(win)


if __name__ == '__main__':
    em = ExploreManager()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(em)

    window.link_step20_btn(lambda: em.on_step20_click(window))
    window.link_step10_btn(lambda: em.on_step10_click(window))
    window.link_step_btn(lambda: em.on_step_click(window))
    window.link_reset_btn(lambda: em.on_reset_click(window))
    window.link_new_maze_btn(window.setup_win.show)
    window.link_save_btn(em.on_save_click)

    window.show()
    app.exec_()
