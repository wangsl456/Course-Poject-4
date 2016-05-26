#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Course Project 4
TCP/IP demo

author: Junyong Wang

last edited: May 2016
"""

import sys, random
from PyQt4 import QtGui, QtCore
from GUI import *
from SelectiveRepeat import *
from GoBackN import *

class Widget(QtGui.QWidget):
    
    def __init__(self):
        
        super(Widget, self).__init__()
        self.initUI()
        self.isStart = False
        pass
        
    def initUI(self):

        #Init GUI
        
        self.gui = GUI(self)
        
        #Combobox Init
        
        self.combx = QtGui.QComboBox(self)
        self.combx.addItem('Typewriter style')
        self.combx.addItem('Fixed Sender Windo')
        
        
        #Push Button Init
        
        self.btn = QtGui.QPushButton('Start', self)
        
        #Radio Button Init
        
        self.rbut_GBN = QtGui.QRadioButton('Go back N', self)
        self.rbut_SR = QtGui.QRadioButton('Selective Repeat', self)
        
        #LCD Init
        self.lcd_wndSize = QtGui.QLCDNumber(2, self)
        self.lcd_e2eDelay = QtGui.QLCDNumber(5, self)
        self.lcd_timeout = QtGui.QLCDNumber(6, self)
        self.lcd_pkt = QtGui.QLCDNumber(3, self)
        
        self.lcd_wndSize.display(5)
        self.lcd_e2eDelay.display(5000)
        self.lcd_timeout.display(11000)
        self.lcd_pkt.display(60)

        self.lcd_wndSize.setSegmentStyle(2)
        self.lcd_e2eDelay.setSegmentStyle(2)
        self.lcd_timeout.setSegmentStyle(2)
        self.lcd_pkt.setSegmentStyle(2)
        #Slider Init
        self.sld_wndSize = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld_e2eDelay = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld_timeout = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld_pkt = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        
        self.sld_wndSize.setRange(1, 10)
        self.sld_wndSize.setValue(5)
        self.sld_wndSize.setPageStep(1)
        
        self.sld_e2eDelay.setRange(1000, 30000)
        self.sld_e2eDelay.setValue(5000)
        self.sld_e2eDelay.setSingleStep(500)
        self.sld_e2eDelay.setPageStep(500)
        
        self.sld_timeout.setRange(1000, 20000)
        self.sld_timeout.setValue(11000)
        self.sld_timeout.setSingleStep(500)
        self.sld_timeout.setPageStep(500)

        self.sld_pkt.setRange(1, 120)
        self.sld_pkt.setValue(60)
        self.sld_pkt.setPageStep(1)
        
        #Slider 
        self.title_wndSize = QtGui.QLabel('window Size')
        self.title_e2eDelay = QtGui.QLabel('end to end delay')
        self.title_timeout = QtGui.QLabel('time out')
        self.title_pkt = QtGui.QLabel('number of packets emited per minute')
        self.title_ptl = QtGui.QLabel('protocol')
        self.title_scrollmode = QtGui.QLabel('scroll mode')
        self.title_emt = QtGui.QLabel('automatic emission of packets')
        
        #grid Init
        grid = QtGui.QGridLayout()
        
        grid.setSpacing(10)

        grid.addWidget(self.title_ptl, 0, 0)
        grid.addWidget(self.rbut_GBN, 0, 1)
        grid.addWidget(self.rbut_SR, 1, 1)
        grid.addWidget(self.btn, 0, 2)
        QtCore.QObject.connect(self.btn, QtCore.SIGNAL("clicked()"), self.Start)
        QtCore.QObject.connect(self.rbut_GBN, QtCore.SIGNAL("clicked()"), self.ModeGBN)
        QtCore.QObject.connect(self.rbut_SR, QtCore.SIGNAL("clicked()"), self.ModeSR)
        
        grid.addWidget(self.title_wndSize, 2, 0)
        grid.addWidget(self.sld_wndSize, 2, 1)
        grid.addWidget(self.lcd_wndSize, 2, 2)
        self.sld_wndSize.valueChanged.connect(self.lcd_wndSize.display)
        self.sld_wndSize.valueChanged.connect(self.gui.setWndSize)
        
        grid.addWidget(self.title_e2eDelay, 3, 0)
        grid.addWidget(self.sld_e2eDelay, 3, 1)
        grid.addWidget(self.lcd_e2eDelay, 3, 2)
        self.sld_e2eDelay.valueChanged.connect(self.lcd_e2eDelay.display)
        self.sld_e2eDelay.valueChanged.connect(self.gui.sete2eDelay)
        
        grid.addWidget(self.title_timeout, 4, 0)
        grid.addWidget(self.sld_timeout, 4, 1)
        grid.addWidget(self.lcd_timeout, 4, 2)
        self.sld_timeout.valueChanged.connect(self.lcd_timeout.display)
        self.sld_timeout.valueChanged.connect(self.gui.settimeout)
        
        grid.addWidget(self.title_pkt, 5, 0)
        grid.addWidget(self.sld_pkt, 5, 1)
        grid.addWidget(self.lcd_pkt, 5, 2)
        self.sld_pkt.valueChanged.connect(self.lcd_pkt.display)
        self.sld_pkt.valueChanged.connect(self.gui.setpkt)
        
        grid.addWidget(self.title_scrollmode, 6, 0)
        grid.addWidget(self.combx, 6, 1)
        QtCore.QObject.connect(self.combx, QtCore.SIGNAL("activated(int)"), self.ModeScroll)
        
        grid.addWidget(self.title_emt, 7, 0)
        
        grid.addWidget(self.gui, 8, 0, 5, 3)
        
        self.setLayout(grid)
        
        self.showMaximized()
        self.setWindowTitle('Selective Repeat / Go Back N')
        self.show()
        pass
        
    def paintEvent(self, e):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()
        pass
    def draw(self, qp):
        self.gui.draw(qp)
        pass
    
    def SendData(self):
        
        pass
    def Start(self):
        if self.isStart == False:
            self.gui.StartAction()
            self.isStart = True
            self.btn.setText('Stop')
            pass
        elif self.isStart == True:
            self.gui.StopAction()
            self.isStart = False
            self.btn.setText('Start')
            pass
        pass
    def ModeGBN(self):
        self.gui.setMode(0)
        pass
    def ModeSR(self):
        self.gui.setMode(1)
        pass
    def ModeScroll(self):
        self.gui.setScrollMode(self.combx.currentIndex())
    def keyPressEvent(self, e):
        
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        pass
            
def main():
    
    #Init Class Var
    
    app = QtGui.QApplication(sys.argv)
    ex = Widget()
    sys.exit(app.exec_())
    pass

if __name__ == '__main__':
    main()