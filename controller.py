import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
from keylogger import Keylogger
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from filemanager import write
from command import Command


class Controller:
    def __init__(self):
        self.current_category = 0
        self.main_window = Ui_MainWindow()

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.main_window.setupUi(MainWindow, self)
        MainWindow.show()
        self.keylogger = Keylogger()
        self.load()
        self.main_window.category_box.currentIndexChanged.connect(self.category_changed)
        sys.exit(app.exec_())

    def category_changed(self):
        self.save()
        self.load_macros()
        self.current_category = self.main_window.category_box.currentIndex()

    def load_macros(self):
        self.main_window.macros_table.setRowCount(0)
        for index, command in enumerate(self.keylogger.get_commands_by_category(
                self.keylogger.categories[self.main_window.category_box.currentIndex()])):
            self.main_window.macros_table.insertRow(index)
            self.main_window.macros_table.setItem(index, 0, QTableWidgetItem(command.name))
            self.main_window.macros_table.setItem(index, 1, QTableWidgetItem(",".join(command.parameters)))
            self.main_window.macros_table.setItem(index, 2, QTableWidgetItem(command.response))

    def load_categories(self):
        self.main_window.category_box.clear()
        self.main_window.category_box.addItems(self.keylogger.categories)

    def load(self):
        self.load_categories()
        self.load_macros()

    def add_category(self):
        self.keylogger.categories.append(self.main_window.category_name_inpt.toPlainText())
        self.load_categories()

    def save(self):
        commands = []
        for i in range(self.main_window.macros_table.rowCount()):
            name = self.main_window.macros_table.item(i, 0).text()
            parameters = [] if self.main_window.macros_table.item(i, 1).text() == "" else self.main_window.macros_table.item(i, 1).text().split(",")
            response = self.main_window.macros_table.item(i, 2).text()
            commands.append(Command(name, parameters, response,
                     self.keylogger.categories[self.current_category]))
        for command in self.keylogger.get_commands_except_category(self.keylogger.categories[self.current_category]):
            commands.append(command)
        write("macros.json", commands)

    def add(self):
        self.main_window.macros_table.insertRow(self.main_window.macros_table.rowCount())


Controller()
