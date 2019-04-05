# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:51:17 2019

@author: Andreas
"""

import sys
from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsView

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QSize
# from PyQt5.QtWidgets import setStyleSheet

from monster_editor import Ui_Dialog as monstergui
#from pathlib import Path
#from PIL import Image



class MonsterData(QDialog):
    def __init__(self, parent = None,
                 monster = None):
        super(MonsterData, self).__init__(parent)

        if monster == None:
            monster = {'move': '6',
                       'at': '2',
                       'de': '2',
                       'bp': '1',
                       'mp': '2',
                       'name': 'Skeleton',
                       }

        self.background_path = 'monster_back_eu.png'
        self.dialog_back_path = "monstercard_dialog_back.png"
        
        self.ui = monstergui()
        self.ui.setupUi(self)

        self.set_monster(monster)
        self.ui.textEdit_name.setAlignment(Qt.AlignCenter)
        self.ui.plainText_at.setAlignment(Qt.AlignCenter)
        self.ui.plainText_move.setAlignment(Qt.AlignCenter)
        self.ui.plainText_at.setAlignment(Qt.AlignCenter)
        self.ui.plainText_de.setAlignment(Qt.AlignCenter)
        self.ui.plainText_bp.setAlignment(Qt.AlignCenter)
        self.ui.plainText_mp.setAlignment(Qt.AlignCenter)


        self.scene = QGraphicsScene()
        self.update_background(self.background_path)

        self.set_dialog_back(self.dialog_back_path)

        self.icon_name = "goblin" # shall be a heroscribe id
        self.pic_path = "goblin.png" # shall be a valid monster picture

        #self.accepted.connect(self.get_monster)





    def update_background(self, image_path):
        #Update Background Picture
        self.scene.clear()
        pixMap = QPixmap(image_path)
        self.scene.addPixmap(pixMap)
        h = pixMap.size().height()
        w = pixMap.size().width()
        self.ui.graphic_background.setScene(self.scene)
        self.ui.graphic_background.fitInView(QRectF(0, 0, w, h),
                                             #Qt.KeepAspectRatio
                                             )
        self.scene.update()

    def set_dialog_back(self, image_path):
        # TODO:
        # I ran in difficulties here. Apparently it is not an easy task
        # to set a new background picture in a dialog....
        pass

    def get_at_symbol(self):
        if self.ui.radio_at_skull.isChecked():
            return "skull"
        elif self.ui.radio_at_shield.isChecked():
            return "shield"
        elif self.ui.radio_at_walrus.isChecked():
            return "walrus"
        else:
            return "skull"

    def get_de_symbol(self):
        if self.ui.radio_de_skull.isChecked():
            return "skull"
        elif self.ui.radio_de_shield.isChecked():
            return "shield"
        elif self.ui.radio_de_walrus.isChecked():
            return "walrus"
        else:
            return "walrus"

    def set_at_symbol(self, symbol):
        ''' takes a symbol as string and sets the corresponding radio button'''
        if symbol == "skull":
            self.ui.radio_at_skull.setChecked(True)
        elif symbol == "shield":
            self.ui.radio_at_shield.setChecked(True)
        elif symbol == "walrus":
            self.ui.radio_at_walrus.setChecked(True)
        else:
            self.ui.radio_at_skull.setChecked(True)

    def set_de_symbol(self, symbol):
        ''' takes a symbol as string and sets the corresponding radio button'''
        if symbol == "skull":
            self.ui.radio_de_skull.setChecked(True)
        elif symbol == "shield":
            self.ui.radio_de_shield.setChecked(True)
        elif symbol == "walrus":
            self.ui.radio_de_walrus.setChecked(True)
        else:
            self.ui.radio_de_skull.setChecked(True)

    def set_monster(self, mon):

        self.ui.plainText_move.setText(str(mon.get('move', 6)))
        self.ui.plainText_at.setText(str(mon.get('at', 2)))
        self.ui.plainText_de.setText(str(mon.get('de', 2)))
        self.ui.plainText_bp.setText(str(mon.get('bp', 1)))
        self.ui.plainText_mp.setText(str(mon.get('mp', 0)))

        self.ui.textEdit_name.setText(mon.get('name', "Skeleton"))
        self.ui.at_diagonal.setCheckState(mon.get('diagonal', False))
        self.ui.at_ranged.setCheckState(mon.get('ranged',False))

        self.ui.at_number.setValue(mon.get('at_number', 1))

        self.ui.de_guardian.setCheckState(mon.get('guardian', False))
        self.ui.de_master.setCheckState(mon.get('master', False))
        self.ui.de_phalanx.setCheckState(mon.get('phalanx', False))

        self.ui.tags.setPlainText(mon.get('tags', ""))
        self.ui.spells.setPlainText(mon.get('spells', ""))

        self.pic_path = mon.get('picture', "")
        self.icon_name = mon.get('icon', "")
        self.ui.plain_text_special_rules.setPlainText(mon.get('specialrule', "No special rule"))
        self.set_at_symbol(mon.get('at_symbol', "skull"))
        self.set_de_symbol(mon.get('de_symbol', "walrus"))

        self.ui.at_damage_type.setPlainText(mon.get('at_dmg_type', ""))
        self.ui.de_immune.setPlainText(mon.get('immune', ""))
        self.ui.de_except.setPlainText(mon.get('except', ""))

    def get_monster(self):
        mon = {}
        mon['move'] = self.ui.plainText_move.text()
        mon['at'] = self.ui.plainText_at.text()
        mon['de'] = self.ui.plainText_de.text()
        mon['bp'] = self.ui.plainText_bp.text()
        mon['mp'] = self.ui.plainText_mp.text()
        mon['name'] = self.ui.textEdit_name.toPlainText()
        mon['diagonal'] = self.ui.at_diagonal.isChecked()
        mon['ranged'] = self.ui.at_ranged.isChecked()
        mon['at_number'] = self.ui.at_number.value()
        mon['guardian'] = self.ui.de_guardian.isChecked()
        mon['master'] = self.ui.de_master.isChecked()
        mon['phalanx'] = self.ui.de_phalanx.isChecked()
        mon['tags'] = self.ui.tags.toPlainText()
        mon['spells'] = self.ui.spells.toPlainText()
        mon['picture'] = self.pic_path
        mon['icon'] = self.icon_name
        mon['specialrule'] = self.ui.plain_text_special_rules.toPlainText()
        mon['at_symbol'] = self.get_at_symbol()
        mon['de_symbol'] = self.get_de_symbol()
        mon['at_dmg_type'] = self.ui.at_damage_type.toPlainText()
        mon['immune'] = self.ui.de_immune.toPlainText()
        mon['except'] = self.ui.de_except.toPlainText()
        #self.accept()
        return mon


if __name__ == '__main__':
    app = QApplication(sys.argv)
else:
    app = QApplication([])
app.lastWindowClosed.connect(app.quit)
IM = MonsterData()
IM.show()
#print(IM.get_monster())

#app.exec_()
sys.exit(app.exec_())

