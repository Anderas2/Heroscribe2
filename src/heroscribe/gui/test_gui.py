import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
#from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class hs2_window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window stats
        self.title = 'Heroscribe 2.0'
        self.left = 10
        self.top = 10
        self.width = 1024
        self.height = 768
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top, self.width, self.height)
        self.statusBar().showMessage('Map Editor')

        # Add Objects button
        add_button = QPushButton('Add object', self)
        add_button.setToolTip('This button adds elements to the map')
        add_button.move(20, 20)
        add_button.clicked.connect(self.add_click)

        # Select/Remove Object button
        select_button = QPushButton('Select', self)
        select_button.setToolTip('This button allows objects to be selcted or removed from the map')
        select_button.move(20, 50)
        select_button.clicked.connect(self.select_click)

        # Darken button
        dark_button = QPushButton('Darken', self)
        dark_button.setToolTip('This button darkens squares on the map')
        dark_button.move(20, 80)
        dark_button.clicked.connect(self.dark_click)

        # Display the window
        self.show()

    @pyqtSlot()
    def add_click(self):
        print('Add button pressed')

    @pyqtSlot()
    def select_click(self):
        print('Select/Remove button pressed')

    @pyqtSlot()
    def dark_click(self):
        print('Darken button pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = hs2_window()
    sys.exit(app.exec_())