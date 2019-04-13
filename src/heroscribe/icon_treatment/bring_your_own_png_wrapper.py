# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:51:17 2019

@author: Andreas
"""
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

from src.heroscribe.helper import png_to_svg as ps
from src.heroscribe.icon_treatment.bring_your_own_png import Ui_bring_your_own_png as prepa_gui


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


# define png preparation dialog
class png_prepa(QDialog):
    def __init__(self, parent = None,
                 autotrace_path = None,
                 original_path = None,
                 icon_path = None):
        super(png_prepa, self).__init__(parent)
        self.ui = prepa_gui()
        self.ui.setupUi(self)

        self.icon_path = icon_path

        # initialize picture tool
        self.bg = ps.BlackGradients()
        self.bg.AUTOTRACE = str(autotrace_path)
        
        # initialize graphic scenes
        self.scene_original = myGraphicsScene()
        self.ui.graphic_original.setScene(self.scene_original)
        self.scene_original.raise_alert.connect(self.symbol_dialog)
        
        self.scene_prepared = QGraphicsScene()
        self.ui.graphic_prepared.setScene(self.scene_prepared)

        self.scene_svg_eu = QGraphicsScene()
        self.ui.graphic_svg_eu.setScene(self.scene_svg_eu)

        # if given, initialize pics
        self.original_path = original_path
        if self.original_path:
            self.update_original(self.original_path)


        # initialize slider connections
        self.ui.prepa_slider_medianfilter.valueChanged.connect(self.update_median)
        self.ui.prepa_line_edit_medianfilter.returnPressed.connect(self.update_median_text)

        self.ui.prepa_slider_contrast.valueChanged.connect(self.update_contrast)
        self.ui.prepa_line_edit_contrast.returnPressed.connect(self.update_contrast_text)

        self.ui.prepa_slider_despeckle.valueChanged.connect(self.update_despeckle)
        self.ui.prepa_line_edit_despeckle.returnPressed.connect(self.update_despeckle_text)

        self.ui.prepa_slider_corner.valueChanged.connect(self.update_corner)
        self.ui.prepa_line_edit_corner.returnPressed.connect(self.update_corner_text)

        self.ui.prepa_slider_errorthreshold.valueChanged.connect(self.update_errorthreshold)
        self.ui.prepa_line_edit_errorthreshold.returnPressed.connect(self.update_errorthreshold_text)

        self.ui.button_next.clicked.connect(self.next)
        self.ui.button_cancel.clicked.connect(self.cancel)
        
        self.ui.button_upsampling.clicked.connect(self.update_prepared_png)

        self.update_median()
        self.update_contrast()

        # initialize in-memory working copies
        self.png_orig_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self.png_orig_temp.close()
        
        self.png_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self.png_temp.close()

        self.svg_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
        self.svg_temp.close()

        self.svg_temp_us = tempfile.NamedTemporaryFile(delete=False, suffix=".svg")
        self.svg_temp_us.close()
        



        # initialize autotrace button
        self.ui.button_autotrace.clicked.connect(self.autotrace)

    def next(self):
        self.close_down()

        if not self.icon_path.exists():
            icon_path.mkdir()    
        self.svg_name = self.ui.lineEdit_filename.text()
        
        outfilepath = self.icon_path / self.svg_name
        if not outfilepath.exists():
            os.rename(self.svg_temp.name,
                  str(outfilepath))

        if os.path.exists(self.svg_temp.name):
            os.remove(self.svg_temp.name)
        self.outfilepath = outfilepath

    def cancel(self):
        self.close_down()
        os.remove(self.svg_temp.name)
        
    def close_down(self):
        self.png_orig_temp.close()
        self.png_temp.close()
        self.svg_temp_us.close()
        os.remove(self.png_orig_temp.name)
        os.remove(self.png_temp.name)
        os.remove(self.svg_temp_us.name)

        

    def autotrace(self):
        despeckle = 10
        gradient_mid = self.ui.prepa_slider_despeckle.value()/100
        errorthresh = self.ui.prepa_slider_errorthreshold.value()/10
        cornerdetect = self.ui.prepa_slider_corner.value()
        try:
            self.bg.make_vector(self.png_temp.name,
                                self.svg_temp_us.name,
                                despeckle = despeckle,
                                errorthresh = errorthresh,
                                cornerdetect = cornerdetect)
            self.bg.recolor_svg_file('black',
                                     self.svg_temp_us.name,
                                     self.svg_temp.name,
                                     gradient_mid = gradient_mid)
                
            self.scene_svg_eu.clear()
            svg_eu = QGraphicsSvgItem(self.svg_temp.name)


            #scaled = svg_eu.scaled(191, 191, Qt.KeepAspectRatio)
            self.scene_svg_eu.addItem(svg_eu)
            self.scene_svg_eu.update()
            self.ui.graphic_svg_eu.fitInView(svg_eu)
        except Exception as err:
            print(str(err))
             
                            
    def update_corner(self):
        '''after the slider has been used, update the text edit'''
        v = self.ui.prepa_slider_corner.value()
        self.ui.prepa_line_edit_corner.setText(str(v))
        
    def update_corner_text(self):
        ''' after the text has been edited, update the slider'''
        v = self.ui.prepa_line_edit_corner.text()
        try:
            num = int(v)
            self.ui.prepa_slider_corner.setValue(num)
        except:
            v = self.ui.prepa_slider_corner.value()
            self.ui.prepa_line_edit_corner.setText(str(v))             
                            
    def update_errorthreshold(self):
        '''after the slider has been used, update the text edit'''
        v = self.ui.prepa_slider_errorthreshold.value()
        self.ui.prepa_line_edit_errorthreshold.setText(str(v))
        
    def update_errorthreshold_text(self):
        ''' after the text has been edited, update the slider'''
        v = self.ui.prepa_line_edit_errorthreshold.text()
        try:
            num = int(v)
            self.ui.prepa_slider_errorthreshold.setValue(num)
        except:
            v = self.ui.prepa_slider_errorthreshold.value()
            self.ui.prepa_line_edit_errorthreshold.setText(str(v))  
            
                            
    def update_despeckle(self):
        '''after the slider has been used, update the text edit'''
        v = self.ui.prepa_slider_despeckle.value()
        self.ui.prepa_line_edit_despeckle.setText(str(v))
        
    def update_despeckle_text(self):
        ''' after the text has been edited, update the slider'''
        v = self.ui.prepa_line_edit_despeckle.text()
        try:
            num = int(v)
            self.ui.prepa_slider_despeckle.setValue(num)
        except:
            v = self.ui.prepa_slider_despeckle.value()
            self.ui.prepa_line_edit_despeckle.setText(str(v))            

        
    def update_median(self):
        '''after the slider has been used, update the text edit'''
        v = self.ui.prepa_slider_medianfilter.value()
        self.ui.prepa_line_edit_medianfilter.setText(str(v))
        self.update_prepared_png()
        
    def update_median_text(self):
        ''' after the text has been edited, update the slider'''
        v = self.ui.prepa_line_edit_medianfilter.text()
        try:
            num = int(v)
            self.ui.prepa_slider_medianfilter.setValue(num)
        except:
            v = self.ui.prepa_slider_medianfilter.value()
            self.ui.prepa_line_edit_medianfilter.setText(str(v))            
        self.update_prepared_png()
                
    def update_contrast(self):
        '''after the slider has been used, update the text edit'''
        v = self.ui.prepa_slider_contrast.value()
        self.ui.prepa_line_edit_contrast.setText(str(v))
        self.update_prepared_png()

    def update_contrast_text(self):
        try:
            num = int(v)
            self.ui.prepa_slider_medianfilter.setValue(num)
        except:
            v = self.ui.prepa_slider_medianfilter.value()
            self.ui.prepa_line_edit_medianfilter.setText(str(v))
        self.update_prepared_png()
    
    def update_prepared_png(self):
        if not self.original_path:
            return
        median = self.ui.prepa_slider_medianfilter.value()
        if median > 0:
            median = median * 2 + 1
        contrast = self.ui.prepa_slider_contrast.value()
        upsampling = self.ui.button_upsampling.isChecked()
        if upsampling > 0:
            upsampling = 4
        # work on the file
        try:
            self.bg.recolor_one_png(infile = self.png_orig_temp.name,
                               temp_file = self.png_temp.name,
                               medianfilter = median,
                               contrast = contrast,
                               upsampling = upsampling)
            # display it
            self.scene_prepared.clear()
            pix_map = QPixmap(self.png_temp.name)
            scaled = pix_map.scaled(191, 191, Qt.KeepAspectRatio)
            self.scene_prepared.addPixmap(scaled)
            self.scene_prepared.update()
        except Exception as err:
            print(str(err))        

    def symbol_dialog(self):
        # Get new file
        image = QFileDialog.getOpenFileName(self, "Choose a picture", "")
        image_path = Path(image[0]) # file dialog returns a tuple
        self.png_orig_temp
        self.update_original(image_path)

    def update_original(self, image_path):
        # use new file
        if not image_path.is_file() :
            return
        self.svg_name = image_path.stem + '.svg'
        self.original_path = str(image_path)
        self.ui.lineEdit_filename.setText(str(self.svg_name))
        self.scene_original.clear()
        pix_map = QPixmap(str(image_path))
        self.pic_original = pix_map

        # save to ram located temp file
        pix_map.save(self.png_orig_temp.name, format="PNG")
        
        scaled = pix_map.scaled(191, 191, Qt.KeepAspectRatio) # scale
        self.scene_original.addPixmap(scaled) # add it to viewer
        self.scene_original.update() # update the viewer for the user
        self.update_prepared_png()




