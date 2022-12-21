import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
from mainUi import UiMainWindow
from addEditCoffeeForm import UiChangeWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Drinks(QMainWindow, UiMainWindow):  # основное окно
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chan = None
        self.update_table()

        self.btn_change.clicked.connect(self.open_window)

    def open_window(self):  # открытие окна для работы с бд
        self.chan = ChangeDrinks()
        self.chan.show()

    def update_table(self):
        self.tw_drinks.clear()
        con = sqlite3.connect(r"data\coffee.db")
        cur = con.cursor()

        result = cur.execute("""SELECT * FROM drinks""").fetchall()  # все напитки

        title = [elem[0] for elem in cur.description]  # заголовки

        con.close()

        self.tw_drinks.setColumnCount(len(title))  # заполнение таблицы
        self.tw_drinks.setRowCount(1)
        self.tw_drinks.setHorizontalHeaderLabels(title)

        for i, row in enumerate(result):
            self.tw_drinks.setRowCount(i + 1)
            for j, elem in enumerate(row):
                self.tw_drinks.setItem(i, j, QTableWidgetItem(str(elem)))

        self.tw_drinks.resizeColumnsToContents()


class ChangeDrinks(QWidget, UiChangeWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_or_update = False  # проверка, когда надо создать новый элемент в бд или обновить
        self.box_update()  # обновить список напитков после изменений
        self.cb_drinks.activated.connect(self.show_drinks)  # выбор напитка
        self.btn_change.clicked.connect(self.save_drinks)

    def show_drinks(self):  # показать напиток, который выбрал пользователь
        title = self.cb_drinks.currentText()  # название выбранного напитка
        result = self.sql_request("*", 'название сорта', title)[0]  # данный о напитке
        for i, line in enumerate([self.line_id, self.line_name, self.line_roasting,
                                  self.line_ground, self.line_description, self.line_coast, self.line_volume]):
            line.setText(str(result[i]))  # показать данные о напитке пользователю

        self.btn_change.setText("изменить")  # изменить текст кнопки
        self.create_or_update = True  # теперь напиток будет меняться, а не создаваться

    def save_drinks(self):  # сохранить напиток или изменить
        list_edit = []  # список внесенных данный пользователя о напитке

        for edit in [self.line_name, self.line_roasting, self.line_ground,
                     self.line_description, self.line_coast, self.line_volume, self.line_id]:
            list_edit.append(edit.text())

        con = sqlite3.connect(r"data\coffee.db")
        cur = con.cursor()

        if self.create_or_update:  # если в бд надо добавить элемент
            cur.execute("""
            UPDATE drinks SET 'название сорта' = ?, 'степень обжарки' = ?, 'молотый/в зернах' = ?, 
                'описание вкуса' = ?, 'цена' = ?, 'объем упаковки' = ?
                    WHERE id = ?""", (*list_edit,))

            self.create_or_update = False
            self.btn_change.setText("создать")

        else:  # если изменить
            cur.execute("""
            INSERT INTO drinks('название сорта', 'степень обжарки',
             'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки')
                VALUES (?, ?, ?, ?, ?, ?)""", (*list_edit[:-1],))

        con.commit()
        con.close()

        self.box_update()  # обновить список напитков

    def sql_request(self, value, condition1="1", condition2="1"):  # запросы к бд
        con = sqlite3.connect(r"data\coffee.db")
        cur = con.cursor()

        result = cur.execute(f'''SELECT {value} FROM drinks WHERE "{condition1}" = "{condition2}"''').fetchall()

        con.close()
        return result

    def box_update(self):  # обновление данных
        result = [("",)] + self.sql_request('"название сорта"')

        self.cb_drinks.clear()
        for elem in result:
            self.cb_drinks.addItem(str(elem[0]))

        for edit in [self.line_name, self.line_roasting, self.line_ground,
                     self.line_description, self.line_coast, self.line_volume, self.line_id]:
            edit.setText("")

    def closeEvent(self, event):
        dr.update_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dr = Drinks()
    dr.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
