# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'size_your_symbol.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_symbol_sizing(object):
    def setupUi(self, dialog_symbol_sizing):
        dialog_symbol_sizing.setObjectName("dialog_symbol_sizing")
        dialog_symbol_sizing.resize(572, 643)
        dialog_symbol_sizing.setToolTipDuration(-1)
        dialog_symbol_sizing.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog_symbol_sizing)
        self.buttonBox.setGeometry(QtCore.QRect(320, 600, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.spin_width = QtWidgets.QSpinBox(dialog_symbol_sizing)
        self.spin_width.setGeometry(QtCore.QRect(20, 600, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Gaze")
        font.setPointSize(14)
        self.spin_width.setFont(font)
        self.spin_width.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_width.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spin_width.setMinimum(0)
        self.spin_width.setMaximum(30)
        self.spin_width.setProperty("value", 1)
        self.spin_width.setObjectName("spin_width")
        self.spin_height = QtWidgets.QSpinBox(dialog_symbol_sizing)
        self.spin_height.setGeometry(QtCore.QRect(100, 600, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Gaze")
        font.setPointSize(14)
        self.spin_height.setFont(font)
        self.spin_height.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_height.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spin_height.setMaximum(30)
        self.spin_height.setProperty("value", 1)
        self.spin_height.setObjectName("spin_height")
        self.label = QtWidgets.QLabel(dialog_symbol_sizing)
        self.label.setGeometry(QtCore.QRect(20, 580, 61, 16))
        font = QtGui.QFont()
        font.setFamily("HQModern")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setMidLineWidth(0)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dialog_symbol_sizing)
        self.label_2.setGeometry(QtCore.QRect(100, 580, 61, 16))
        font = QtGui.QFont()
        font.setFamily("HQModern")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setMidLineWidth(0)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(dialog_symbol_sizing)
        self.buttonBox.accepted.connect(dialog_symbol_sizing.accept)
        self.buttonBox.rejected.connect(dialog_symbol_sizing.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog_symbol_sizing)

    def retranslateUi(self, dialog_symbol_sizing):
        _translate = QtCore.QCoreApplication.translate
        dialog_symbol_sizing.setWindowTitle(_translate("dialog_symbol_sizing", "Size your symbol"))
        self.spin_width.setToolTip(_translate("dialog_symbol_sizing", "Enter the width in game board squares here"))
        self.spin_height.setToolTip(_translate("dialog_symbol_sizing", "Enter the height in game board squares here"))
        self.label.setText(_translate("dialog_symbol_sizing", "Width"))
        self.label_2.setText(_translate("dialog_symbol_sizing", "Height"))

