# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:51:17 2019

@author: Andreas
"""

import sys
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QDialog

class IconMetadata(QDialog):
    def __init__(self, parent = None):
        super(IconMetadata, self).__init__(parent)
        #self.app = QApplication(sys.argv)

        #self.app = QApplication()

        #somewhere in constructor:
        uic.loadUi('icon_dialog.ui', self)

        #self.buttons.accepted.connect(self.accept)
        #self.buttons.rejected.connect(self.reject)
        #self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
else:
    app = QApplication()

IM = IconMetadata()
IM.show()
#sys.exit(IM.app.exec_())