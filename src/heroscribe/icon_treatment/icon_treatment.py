import sys
from PyQt5.QtWidgets import(QApplication, QGraphicsScene, QDialog, QFileDialog,
                            )
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5 import QtCore
from PyQt5.QtCore import QTranslator, QSize, Qt

from pathlib import Path
from copy import deepcopy
import tempfile
import os

from src.heroscribe.icon_treatment.bring_your_own_png_wrapper import png_prepa





class svg_test():
    def start_test(self):
        if __name__ == '__main__':
            app = QApplication(sys.argv)
        else:
            app = QApplication([])
        app.lastWindowClosed.connect(app.quit)

        locale = QtCore.QLocale.system().name()
        qtTranslator = QTranslator()
        if qtTranslator.load("monstereditor_"+locale):
            app.installTranslator(qtTranslator)

        autotrace_path = Path("C:/Users/Andreas/25 Heroquest/Heroscribe 2/src/heroscribe/helper/autotrace/autotrace.exe")
        icon_path = Path("C:/Users/Andreas/25 Heroquest/Heroscribe 2/Icons/MyIcons")
        
        self.p = png_prepa(autotrace_path = autotrace_path,
                           icon_path = icon_path)
        if self.p.exec_():
            print("ok pressed")
            print("find your svg here")
            print(self.p.outfilepath)
        

        
        
        #app.exec_()
        #sys.exit(app.exec_())

    def __init__(self):
        self.start_test()
