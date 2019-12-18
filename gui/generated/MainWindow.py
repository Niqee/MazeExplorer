# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\job\MazeExplorer\gui\ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 283)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.InfoBox = QtWidgets.QGroupBox(self.centralwidget)
        self.InfoBox.setObjectName("InfoBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.InfoBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.StepLabel = QtWidgets.QLabel(self.InfoBox)
        self.StepLabel.setObjectName("StepLabel")
        self.verticalLayout_2.addWidget(self.StepLabel)
        self.ProgressLabel = QtWidgets.QLabel(self.InfoBox)
        self.ProgressLabel.setObjectName("ProgressLabel")
        self.verticalLayout_2.addWidget(self.ProgressLabel)
        self.ProgressBar = QtWidgets.QProgressBar(self.InfoBox)
        self.ProgressBar.setProperty("value", 0)
        self.ProgressBar.setObjectName("ProgressBar")
        self.verticalLayout_2.addWidget(self.ProgressBar)
        self.verticalLayout.addWidget(self.InfoBox)
        self.ControlBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ControlBox.setMaximumSize(QtCore.QSize(16777215, 70))
        self.ControlBox.setObjectName("ControlBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.ControlBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.StartBtn = QtWidgets.QPushButton(self.ControlBox)
        self.StartBtn.setObjectName("StartBtn")
        self.horizontalLayout.addWidget(self.StartBtn)
        self.StopBtn = QtWidgets.QPushButton(self.ControlBox)
        self.StopBtn.setObjectName("StopBtn")
        self.horizontalLayout.addWidget(self.StopBtn)
        self.StepBtn = QtWidgets.QPushButton(self.ControlBox)
        self.StepBtn.setObjectName("StepBtn")
        self.horizontalLayout.addWidget(self.StepBtn)
        self.ResetBtn = QtWidgets.QPushButton(self.ControlBox)
        self.ResetBtn.setObjectName("ResetBtn")
        self.horizontalLayout.addWidget(self.ResetBtn)
        self.NewMazeBtn = QtWidgets.QPushButton(self.ControlBox)
        self.NewMazeBtn.setObjectName("NewMazeBtn")
        self.horizontalLayout.addWidget(self.NewMazeBtn)
        self.SaveBtn = QtWidgets.QPushButton(self.ControlBox)
        self.SaveBtn.setObjectName("SaveBtn")
        self.horizontalLayout.addWidget(self.SaveBtn)
        self.verticalLayout.addWidget(self.ControlBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главное окно"))
        self.InfoBox.setTitle(_translate("MainWindow", "Информация"))
        self.StepLabel.setText(_translate("MainWindow", "Шаг : 0"))
        self.ProgressLabel.setText(_translate("MainWindow", "Прогресс :"))
        self.ControlBox.setTitle(_translate("MainWindow", "Панель управления"))
        self.StartBtn.setText(_translate("MainWindow", "Пуск"))
        self.StopBtn.setText(_translate("MainWindow", "Стоп"))
        self.StepBtn.setText(_translate("MainWindow", "Шаг"))
        self.ResetBtn.setText(_translate("MainWindow", "Сброс"))
        self.NewMazeBtn.setText(_translate("MainWindow", "Новый лабиринт"))
        self.SaveBtn.setText(_translate("MainWindow", "Сохранить лабиринт"))
