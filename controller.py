import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
from keylogger import Keylogger
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from filemanager import write
from command import Command

class Controller:
    def __init__(self):
        self.main_window = Ui_MainWindow()

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.main_window.setupUi(MainWindow, self)
        MainWindow.show()
        self.keylogger = Keylogger()
        sys.exit(app.exec_())

    def load(self):
        print("load")
        for index, command in enumerate(self.keylogger.commands):
            self.main_window.macros_table.insertRow(index)
            self.main_window.macros_table.setItem(index, 0, QTableWidgetItem(command.name))
            self.main_window.macros_table.setItem(index, 1, QTableWidgetItem(",".join(command.parameters)))
            self.main_window.macros_table.setItem(index, 2, QTableWidgetItem(command.response))

    def save(self):
        commands = []
        for i in range(self.main_window.macros_table.rowCount()):
            name = self.main_window.macros_table.item(i, 0).text()
            parameters = self.main_window.macros_table.item(i, 1).text().split(",")
            response = self.main_window.macros_table.item(i, 2).text()
            commands.append(Command(name, parameters, response))
        print(commands)
        write("macros.json", commands)

    def add(self):
        self.main_window.macros_table.insertRow(self.main_window.macros_table.rowCount())


Controller()
