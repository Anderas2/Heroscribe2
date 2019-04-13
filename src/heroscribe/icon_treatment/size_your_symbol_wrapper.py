# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:51:17 2019

@author: Andreas
"""

import sys
from pathlib import Path
from copy import deepcopy
import tempfile
import os


from PyQt5.QtWidgets import(QApplication, QGraphicsScene, QDialog, QFileDialog,
                            QGraphicsView, QGraphicsItem, QGraphicsRectItem,
                            QFrame, QAbstractScrollArea)
from PyQt5.QtGui import (QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap,
                         QWheelEvent)
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QLocale, QRect
from PyQt5.QtCore import QTranslator, QSize, Qt


from src.heroscribe.helper import png_to_svg as ps
from src.heroscribe.icon_treatment.size_your_symbol import Ui_dialog_symbol_sizing as size_gui


# define your own SVG class for size handling


class MyQGraphicsView(QGraphicsView):

    def __init__ (self, parent=None):
        super(MyQGraphicsView, self).__init__ (parent)

    def wheelEvent(self, event):
        # Zoom Factor
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        angle = event.angleDelta().y() - event.angleDelta().x()
        if angle > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
            
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

class myGraphicsScene(QGraphicsScene):
    # add a signal so I can use the changed box
    # the scene has signals, the box not, so I add it to the scene.
    # But it will be emitted from the Box. Hopefully.
    rect_changed = pyqtSignal(object, object)

class GraphicsRectItem(QGraphicsRectItem):

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +16.0
    handleSpace = -8.0

    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        self.mousePressPos = mouseEvent.pos()

        if self.handleSelected:
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            self.interactiveMove(mouseEvent.pos())        
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None


    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        Then emits the current bounding box for others to reuse it
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)


    def interactiveMove(self, mousePos):
        diff = QPointF(0, 0)
        rect = self.rect()
        boundingRect = self.boundingRect()
        
        from_x = self.mousePressPos.x()
        from_y = self.mousePressPos.y()
        
        to_x = mousePos.x()
        to_y = mousePos.y()
        
        diff.setX(to_x - from_x)
        diff.setY(to_y - from_y)

        self.moveBy(diff.x(), diff.y())
        
        # Emit bounding rect here!
   
        if self.scene() is not None:
            self.scene().rect_changed.emit(self.rect(), self.pos())   
        self.update()

        self.updateHandlesPos()


    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)
        self.prepareGeometryChange()

        # frame start positions
        frame_from_x = self.mousePressRect.left()
        frame_from_y = self.mousePressRect.top()

        mouse_diff_x = mousePos.x()- self.mousePressPos.x()
        mouse_diff_y = mousePos.y() - self.mousePressPos.y()
        
        frame_to_x = frame_from_x + mouse_diff_x
        frame_to_y = frame_from_y + mouse_diff_y
        
        diff.setX(frame_to_x - frame_from_x)
        diff.setY(frame_to_y - frame_from_y)
        

        if self.handleSelected == self.handleTopLeft:
            boundingRect.setLeft(frame_to_x)
            boundingRect.setTop(frame_to_y)

            rect.setLeft(frame_to_x + offset)
            rect.setTop(frame_to_y + offset)
            
            self.setRect(rect)


        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        if self.scene() is not None:
            self.scene().rect_changed.emit(self.rect(), self.pos())   
        self.updateHandlesPos()
        self.update()



    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        painter.setBrush(QBrush(QColor(250, 250, 0, 30)))
        painter.setPen(QPen(QColor(0,0,0,30), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 250, 50)))
        painter.setPen(QPen(QColor(0, 0, 0, 100), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)







# define png preparation dialog
class svg_size(QDialog):
    def showEvent(self, event):
        #self.grview.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        pass

    def standard_size(self):
        # size in sqares times squaresize, minus distance from square borders
        w = self.ui.spin_width.value() * self.squaresize - 10
        h = self.ui.spin_height.value() * self.squaresize - 10
        
        standard_size = QRectF(0, 0, w, h)
        start_pos = QPointF(self.startpos + 5, self.startpos + 5)
        self.start_bounding_rect = QRectF(self.startpos + 5,
                                          self.startpos + 5, w, h)
        self.accept_rect(standard_size, start_pos)
        self.user_rect.setRect(self.start_bounding_rect)

    
    def __init__(self, parent = None,
                 original_path = None,
                 icon_path = None,
                 xmax = 1100,
                 ymax = 1100,
                 squaresize = 100):
        
        super(svg_size, self).__init__(parent)

        # boilerplate initialization
        self.xmax = xmax
        self.ymax = ymax
        self.squaresize = squaresize
        self.ui = size_gui()
        self.ui.setupUi(self)

        self.startpos = 5 * self.squaresize

        
        self.icon_path = Path(icon_path) if icon_path else None
        self.original_path = Path(original_path) if original_path else None
        self.outfilepath = None
        
        # set up grahpicsView
        self.grview = MyQGraphicsView(self)
        self.grview.setGeometry(QRect(0, 0, 571, 571))
        self.grview.setContextMenuPolicy(Qt.NoContextMenu)
        self.grview.setFrameShadow(QFrame.Plain)
        self.grview.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.grview.setObjectName("graphicsView")
        
        #self.ui.graphicsView.wheelEvent = my_mouse_wheel_event
        self.scene = myGraphicsScene() # use my own scene class with the added signal
        self.scene.setSceneRect(0, 0, self.xmax, self.ymax)

        # Paint the grid lines every 100 "svg_points"
        for i in range(0, self.xmax+1, self.squaresize):
            self.line(i, hori = False)
        for i in range(0, self.ymax+1, self.squaresize):
            self.line(i, hori = True)

        # start rect and svg with some standard numbers
        self.svg = QGraphicsSvgItem(str(icon_path))
        self.user_rect = GraphicsRectItem(QRectF(self.startpos + 5,
                                                 self.startpos + 5,
                                                 self.squaresize - 10,
                                                 self.squaresize - 10))

        # add svg and rect to scene
        self.scene.addItem(self.svg)
        self.scene.addItem(self.user_rect)

        # set sizes according to spinboxes
        start_bounding_rect = self.standard_size()

        # connect interactive elements
        self.ui.spin_height.valueChanged.connect(self.standard_size)
        self.ui.spin_width.valueChanged.connect(self.standard_size)
        self.scene.rect_changed.connect(self.accept_rect)



        # put the graphics on the screen and show
        self.grview.setScene(self.scene)
        #self.grview.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.grview.show()

    def retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.graphicsView.setToolTip(_translate("dialog_symbol_sizing",
                                                "After width and height are entered, do the last adjustments in this window"))
    def line(self, coord, hori=True):
        if hori:
            self.scene.addLine(0, coord, self.xmax, coord, QPen())
        else:
            self.scene.addLine(coord, 0, coord, self.ymax, QPen())
        

    def accept_rect(self, rect, pos):
        ''' takes the new coordinates from the moved rectangle and applies them to the svg graphic'''
        br = self.svg.boundingRect()
        relative = min(br.width(), br.height())
        rect_min = min(rect.width(), rect.height())
        scale = rect_min/relative
        self.svg.setScale(scale)
        self.svg_scale = scale

        pos_x = pos.x() + rect.x()
        pos_y = pos.y() + rect.y()
        self.svg.setX(pos_x)
        self.svg.setY(pos_y)
        self.svg_pos = (pos_x % self.squaresize,
                        pos_y % self.squaresize)






class test():
    def __init__(self):

        original_path = Path("C:/Users/Andreas/25 Heroquest/Heroscribe 2/Icons/MyIcons/Clovis.svg")

        icon_path = Path("C:/Users/Andreas/25 Heroquest/Heroscribe 2/Icons/MyIcons/Clovis.svg")

        if __name__ == '__main__':
            app = QApplication(sys.argv)
        else:
            app = QApplication([])
        app.lastWindowClosed.connect(app.quit)
        
        locale = QLocale.system().name()
        qtTranslator = QTranslator()
        if qtTranslator.load("monstereditor_"+locale):
            app.installTranslator(qtTranslator)

        self.xmax = 1100
        self.ymax = 1100
        self.squaresize = 100
        self.s = svg_size(icon_path = icon_path,
                     xmax = self.xmax,
                     ymax = self.ymax,
                     squaresize = self.squaresize)
        
        if self.s.exec_():
            scale = self.s.svg_scale
            print("final scale is ", scale)
            pos = self.s.svg_pos
            print("final svg position is ", pos)
            
        else:
            print("window cancelled")

