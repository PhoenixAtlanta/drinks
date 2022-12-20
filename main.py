import sys
import sqlite3
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Drinks(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн

        con = sqlite3.connect("coffee.db")
        cur = con.cursor()

        result = cur.execute("""SELECT * FROM drinks""").fetchall()

        title = [elem[0] for elem in cur.description]

        con.close()

        self.tw_drinks.setColumnCount(len(title))
        self.tw_drinks.setRowCount(1)
        self.tw_drinks.setHorizontalHeaderLabels(title)

        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tw_drinks.setItem(i, j, QTableWidgetItem(str(elem)))

        self.tw_drinks.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dr = Drinks()
    dr.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
