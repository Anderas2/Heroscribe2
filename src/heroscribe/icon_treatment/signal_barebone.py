# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:51:17 2019

@author: Andreas
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtCore import QRectF, QObject

from monster_editor import Ui_Dialog as monstergui


# add a double click event to QGraphicsScene
class myGraphicsScene(QGraphicsScene):
    item_clicked = QtCore.pyqtSignal(object)
    raise_alert = QtCore.pyqtSignal(object)

    def __init__(self, parent = None):
        super(myGraphicsScene, self).__init__(parent)
        self.item_clicked.connect(self.mouseReleaseEvent)

    def mouseReleaseEvent(self, MouseEvent):
        print("Scene Mouse Release detected")
        self.raise_alert.emit("scene click released")

     
       


# define Monster data edit dialog
class MonsterData(QDialog):
    def __init__(self, parent = None):
        super(MonsterData, self).__init__(parent)

        self.ui = monstergui()
        self.ui.setupUi(self)
       
        # initialize monster picture
        self.scene_monpic = myGraphicsScene()
        self.ui.graphicsView.setScene(self.scene_monpic)
        self.scene_monpic.raise_alert.connect(self.update_monsterpic)
        
    def update_monsterpic(self):
        print("arrived after the double click event")
        pass


class test_gui():
    def test_it(self):
        if __name__ == '__main__':
            app = QApplication(sys.argv)
        else:
            app = QApplication([])
        app.lastWindowClosed.connect(app.quit)

        self.IM = MonsterData()
        self.IM.exec_()


