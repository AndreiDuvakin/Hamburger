import sys

from PyQt6.QtCore import Qt, QMimeData, QPoint
from PyQt6.QtGui import QPixmap, QDrag, QDropEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem, QListWidget, QMessageBox
from PyQt6 import uic


class GameWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('designs/PlayWin.ui', self)
        self.pushButton.clicked.connect(self.change_status_open)
        self.fridge_widget.setVisible(False)
        self.fridge_items = self.fridge_widget.children()
        self.setAcceptDrops(True)
        self.layers = []
        self.render_fridge()

    def render_fridge(self):
        for i in self.fridge_items:
            ing = IngredientFridge(i.objectName())
            i.children()[0].addChildWidget(ing)

    def dragEnterEvent(self, e):
        e.accept()

    def check_to_win(self):
        layers = list(map(lambda i: i.ingredient, self.layers))
        if layers[0] != 'bottom':
            self.ms = QMessageBox()
            self.ms.setWindowTitle('Игра окончена')
            self.ms.setText('Бутерброд должен начинаться с нижней булки')
            self.ms.setIcon(QMessageBox.Icon.Warning)
            self.ms.show()
            self.layers.clear()
            self.make_layers()
        if layers[0] == 'bottom' and layers[-1] == 'top':
            if len(layers) > 2 and any(list(map(lambda x: x not in ['top', 'bottom'], layers))):
                self.ms = QMessageBox()
                self.ms.setWindowTitle('Игра окончена')
                self.ms.setText('Бутерброд создан')
                self.ms.setIcon(QMessageBox.Icon.Information)
                self.ms.show()
                self.layers.clear()
                self.make_layers()
            elif len(layers) == 2:
                self.ms = QMessageBox()
                self.ms.setWindowTitle('Игра окончена')
                self.ms.setText('Это не Бутерброд')
                self.ms.setIcon(QMessageBox.Icon.Warning)
                self.ms.show()
                self.layers.clear()
                self.make_layers()

    def dropEvent(self, e: QDropEvent):
        position, widget = e.position(), e.source()
        purpose = self.childAt(QPoint(*map(int, (position.x(), position.y()))))
        if purpose.objectName() == "qt_scrollarea_viewport" or type(purpose) is HamburgerLayer:
            self.layers.append(widget)
            self.make_layers()
            self.check_to_win()

    def make_layers(self):
        self.hamburgers_layers.clear()
        for i in self.layers[::-1]:
            item = HamburgerLayer(i.ingredient)
            list_itwm = QListWidgetItem()
            self.hamburgers_layers.addItem(list_itwm)
            self.hamburgers_layers.setItemWidget(list_itwm, item)

    def change_status_open(self):
        if self.pushButton.text() == "Открыть":
            self.pushButton.setText("Закрыть")
        else:
            self.pushButton.setText("Открыть")
        self.fridge_widget.setVisible(not self.fridge_widget.isVisible())


class HamburgerLayer(QLabel):
    def __init__(self, ingredient: str):
        super().__init__()
        pixmap = QPixmap(f"res/layers/{ingredient}.svg")
        self.setMinimumHeight(30)
        self.setPixmap(pixmap)


class IngredientFridge(QLabel):
    def __init__(self, ingredient: str):
        super().__init__()
        self.ingredient = ingredient
        pixmap = QPixmap(f"res/ingredients/{ingredient}.svg")
        self.setPixmap(pixmap)
        self.resize(80, 50)
        if not ingredient in ['onion', 'top', 'bottom']:
            self.setScaledContents(True)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GameWin()
    win.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
