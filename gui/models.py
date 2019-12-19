from PyQt5 import QtWidgets

from .generated.MainWindow import Ui_MainWindow
from .generated.SetupWindow import Ui_SetupWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, em):
        super().__init__()
        self.setupUi(self)
        self.setup_win = SetupWindow()
        self.setup_win.main_win = self
        self.update_data = em.update_data

    def link_start_btn(self, func):
        self.StartBtn.clicked.connect(func)

    def link_stop_btn(self, func):
        self.StopBtn.clicked.connect(func)

    def link_step_btn(self, func):
        self.StepBtn.clicked.connect(func)

    def link_reset_btn(self, func):
        self.ResetBtn.clicked.connect(func)

    def link_new_maze_btn(self, func):
        self.NewMazeBtn.clicked.connect(func)

    def link_save_btn(self, func):
        self.SaveBtn.clicked.connect(func)

    def update_progress(self, val):
        self.ProgressBar.setValue(int(val*100))

    def update_step(self, val):
        self.StepLabel.setText("Шаг : {}".format(val))


class SetupWindow(QtWidgets.QMainWindow, Ui_SetupWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main_win = None
        self.GenerateBtn.clicked.connect(self.on_generate_click)

    def on_generate_click(self):
        bot_num = self.BotNumberSpinBox.value()
        height = self.MazeHeightSpinBox.value()
        width = self.MazeWidthSpinBox.value()
        self.main_win.update_progress(0)
        self.main_win.update_step(1)
        self.main_win.update_data((bot_num, height, width))
        self.close()
