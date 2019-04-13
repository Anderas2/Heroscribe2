# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:51:17 2019

@author: Andreas
"""

import sys
from PyQt5 import QtCore, uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDesktopWidget
from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path

from PyQt5.QtCore import QRectF, QTranslator, QObject
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QSize


from monster_editor import Ui_Dialog as monstergui



# add a double click event to QGraphicsScene
class myGraphicsScene(QGraphicsScene):
    item_clicked = QtCore.pyqtSignal(object)
    raise_alert = QtCore.pyqtSignal(object)

    def __init__(self, parent = None):
        super(myGraphicsScene, self).__init__(parent)
        self.item_clicked.connect(self.mouseReleaseEvent)

    def mouseReleaseEvent(self, MouseEvent):
        #Scene Mouse Release detected
        self.raise_alert.emit("something")
        


# define Monster data edit dialog
class MonsterData(QDialog):
    def __init__(self, parent = None,
                 monster = None,
                 style = "EU"):
        super(MonsterData, self).__init__(parent)

        if monster == None:
            monster = {'move': '6',
                       'at': '2',
                       'de': '2',
                       'bp': '1',
                       'mp': '2',
                       'name': 'Skeleton',
                       }
        self.input_monster = monster
        
        self.ui = monstergui()
        self.ui.setupUi(self)

        # initialize monster picture
        self.scene_monpic = myGraphicsScene()
        self.ui.graphicsView.setScene(self.scene_monpic)
        self.scene_monpic.raise_alert.connect(self.monsterpic_dialog)

        # read monster dict and set dialog         
        self.set_monster(monster)
        
        # align to center the five monster values
        self.ui.textEdit_name.setAlignment(Qt.AlignCenter)
        self.ui.plainText_at.setAlignment(Qt.AlignCenter)
        self.ui.plainText_move.setAlignment(Qt.AlignCenter)
        self.ui.plainText_at.setAlignment(Qt.AlignCenter)
        self.ui.plainText_de.setAlignment(Qt.AlignCenter)
        self.ui.plainText_bp.setAlignment(Qt.AlignCenter)
        self.ui.plainText_mp.setAlignment(Qt.AlignCenter)

        
        # initialize background picture
        self.scene = QGraphicsScene()

        self.style = style
        if style.lower() == "eu":
            self.apply_eu_style()
        else:
            self.apply_us_style()
            
        #self.set_dialog_back(self.dialog_back_path)

        self.icon_name = "goblin" # shall be a heroscribe id

        self.accepted.connect(self.get_monster)
        self.rejected.connect(self.get_input)
        self.ui.radio_us.clicked.connect(self.apply_us_style)
        self.ui.radio_eu.clicked.connect(self.apply_eu_style)


    def apply_us_style(self):
        self.update_background('monster_back_us.png')
        # set headline to us romic font
        font = QtGui.QFont()
        font.setFamily("Romic")
        font.setPointSize(16)
        self.ui.textEdit_name.setFont(font)
        self.ui.radio_us.setChecked(True)
        
    def apply_eu_style(self):
        self.update_background('monster_back_eu.png')
        # set headline to EU Gaze font
        font = QtGui.QFont()
        font.setFamily("Gaze")
        font.setPointSize(18)
        self.ui.textEdit_name.setFont(font)
        self.ui.radio_eu.setChecked(True)

    def monsterpic_dialog(self):
        # Get new file
        image = QFileDialog.getOpenFileName(self, "Choose a picture", "")
        image_path = Path(image[0]) # file dialog returns a tuple
        self.update_monsterpic(image_path)

    def set_monsterpic(self, image_path = None):
        image_path = Path(image_path)
        if image_path.is_file():
            self.update_monsterpic(image_path)
        
    def update_monsterpic(self, image_path = None):
        # use new file
        if not image_path.is_file() :
            return
        self.scene_monpic.clear()
        pix_map = QPixmap(str(image_path))
        self.pix_map = pix_map
        scaled = pix_map.scaled(162, 189, Qt.KeepAspectRatio)
        if scaled.size().width() < 162:
            scaled = pix_map.scaledToWidth(162)
        if scaled.size().height() < 189:
            scaled = pix_map.scaledToHeight(189)
        self.scene_monpic.addPixmap(scaled)
        self.scene_monpic.update()
        self.monsterpic_path = str(image_path)

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
        # TODO: change dialogue background to something beautiful
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
        ''' Set all dialog values to the stuff coming via dict '''
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
        image_path = mon.get('picture', None)
        if image_path:
            self.set_monsterpic(image_path)

    def get_input(self):
        '''method to get monster if the dialog was finished with cancel'''
        return self.input_monster

    def get_monster(self):
        '''method to get monster if the dialog was finished with ok'''
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
        mon['picture'] = self.monsterpic_path
        #self.accept()
        return mon


class test_gui():
    def test_it(self):
        if __name__ == '__main__':
            app = QApplication(sys.argv)
        else:
            app = QApplication([])
        app.lastWindowClosed.connect(app.quit)
        locale = QtCore.QLocale.system().name()
        qtTranslator = QTranslator()
        if qtTranslator.load("monstereditor_"+locale):
            app.installTranslator(qtTranslator)
    
        goblin = {'move': '10', 'at': '2', 'de': '1', 'bp': '1', 'mp': '1',
                  'name': 'Goblin', 'at_number': 1,  'tags': 'bg, green',
                  'picture': 'C:\\Users\\Andreas\\25 Heroquest\\Bildersammlung\\MonsterBearbeitet\\Goblin.jpg',}        
        self.IM = MonsterData(monster = goblin, style="US")
        if self.IM.exec_():
            self.monster = self.IM.get_monster()
        else:
            self.monster = self.IM.get_input()
        #self.IM.show()
        #print(IM.get_monster())

        #app.exec_()
        print (self.monster)
        #sys.exit(app.exec_())

