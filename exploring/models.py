from typing import Tuple, Optional
from time import time, sleep
from warnings import warn


class Bot(object):
    """
    Класс для описания бота
    """
    ACTIVE_STATUS: int = 1
    WAITING_STATUS: int = 0

    def __init__(self, name: str = None):
        self.__status: int = Bot.WAITING_STATUS
        self.__position: Tuple[Optional[int], Optional[int]] = (None, None)
        if name is None:
            sleep(0.01)
            self.__name: str = 'BOT_{id}'.format(id=str(time()))
        else:
            self.__name: str = name

    @property
    def status(self) -> int:
        """
        Метод для получения статуса бота

        Returns
        -------
        status : int
            Статус бота
        """
        return self.__status

    @property
    def position(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Метод для получения координат бота

        Returns
        -------
        position : tuple of int
            Координаты бота (height, width)
        """
        return tuple(self.__position)

    @property
    def name(self) -> str:
        """
        Метод для получения имени бота

        Returns
        -------
        name : str
            Имя бота
        """
        return self.__name

    def activate(self, drop_position: Tuple[int, int]) -> None:
        """
        Метод для активации бота

        Parameters
        ----------
        drop_position : tuple of int
            Координаты точки, в которой бот начинает исследование
        """
        if self.__status == Bot.ACTIVE_STATUS:
            warn('Попытка перевести активного бота {name} в активное состояние.'.format(name=self.name))
        self.__status = Bot.ACTIVE_STATUS
        self.__position = drop_position

    def deactivate(self) -> None:
        """
        Метод для перевода бота в режим ожидания
        """
        if self.__status == Bot.WAITING_STATUS:
            warn('Попытка перевести ожидающего бота {name} в ожидающее состояние.'.format(name=self.name))
        self.__status = Bot.WAITING_STATUS
        self.__position = (None, None)

    def move_up(self) -> None:
        """
        Метод для перемещения бота на 1 клетку вверх
        """
        self.__position = (self.__position[0] - 1, self.__position[1])

    def move_down(self) -> None:
        """
        Метод для перемещения бота на 1 клетку вниз
        """
        self.__position = (self.__position[0] + 1, self.__position[1])

    def move_left(self) -> None:
        """
        Метод для перемещения бота на 1 клетку влево
        """
        self.__position = (self.__position[0], self.__position[1] - 1)

    def move_right(self) -> None:
        """
        Метод для перемещения бота на 1 клетку вправо
        """
        self.__position = (self.__position[0], self.__position[1] + 1)


if __name__ == '__main__':
    bot1 = Bot()
    bot2 = Bot()
    print(bot1.name)
    print(bot2.name)
