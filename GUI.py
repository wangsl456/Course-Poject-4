#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Course Project 4
GUI

author: Junyong Wang

last edited: May 2016
"""
import sys, random
from PyQt4 import QtGui, QtCore
from SelectiveRepeat import *
from GoBackN import *


class GUI(QtGui.QWidget):
    def __init__(self, parent = None):
        
        super(GUI, self).__init__(parent)
        
        self.isChanged = True
        self.Action = None
        #Init data
        self.SendWndSize = 5
        self.RecvWndSize = 5
        self.e2eDelay = 5000
        self.timeout = 11000
        self.pkt = 60
        
        self.SendWndBegin = 5
        self.RecvWndBegin = 5
        self.NextSend = 5
        self.NextACK = 5
        
        self.Start = False
        self.Mode = 'GBN'
        self.ScrollMode = 'Typewriter'
        
        self.SR = SRAction()
        self.GBN = GBNAction()
        
        self.ScrollMode = 1
        
        #Timer Init
        
        
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.TimerAction)
        self.timer.start(20)
        
        self.timerSendSR = QtCore.QTimer()
        QtCore.QObject.connect(self.timerSendSR, QtCore.SIGNAL("timeout()"), self.SR.Ready2Send)
        self.timerSendSR.start(60000 / self.pkt)
        self.timerSendGBN = QtCore.QTimer()
        QtCore.QObject.connect(self.timerSendGBN, QtCore.SIGNAL("timeout()"), self.GBN.Ready2Send)
        self.timerSendGBN.start(60000 / self.pkt)
        #Commom
        #Init Graphic data
        
        self.White = QtGui.QColor(255, 255, 255)
        self.Blue = QtGui.QColor(0, 0, 100)
        self.Green = QtGui.QColor(0, 255, 0)
        self.Yellow = QtGui.QColor(150, 150, 0)
        self.Violet = QtGui.QColor(0 , 0, 200)
        self.Gray = QtGui.QColor(135, 135, 135)
        self.Black = QtGui.QColor(0, 0, 0)
        self.Pink = QtGui.QColor( 200, 0, 50)
        self.ColorDict = {0 : self.White, 1 : self.Blue, 2 : self.Green, 3 : self.Yellow, 4 : self.Violet, 5 : self.Pink}
        
        self.CubeW = 20
        self.CubeH = 40
        
        self.UpperH = 50
        self.LowerH = 450
        
        self.CubeInterval = 30
        pass
    
    def Send(self):
        if self.Mode == 'SR':
            self.SR.Send()
            pass
        elif self.Mode == 'GBN':
            self.GBN.Send()
            pass
        pass
        
        
    def draw(self, qp):
        if self.Mode == 'SR':
            self.Action = self.SR
        elif self.Mode == 'GBN':
            self.Action = self.GBN
        if self.ScrollMode == 0:
            if self.Action.getSendWndBegin() >= 25:
                self.Action.PageLeft(10)
                pass
            pass
        elif self.ScrollMode == 1:
            if self.Action.getSendWndBegin() >= 5 +self.SendWndSize:
                self.Action.PageLeft(1)
                pass
            pass
        pass
        #Static Graphics
        posx = self.x()
        posy = self.y()
        size = self.size()
        
        qp.setPen(self.Black)
        
        qp.setBrush(self.Gray)
        qp.drawRect(posx + self.Action.getSendWndBegin() * self.CubeInterval - 5, posy + self.UpperH - 5, (self.Action.getSendWndSize() - 1) * self.CubeInterval + self.CubeW + 10, self.CubeH + 10)
        if self.Mode == 'SR':
            qp.drawRect(posx + self.Action.getRecvWndBegin() * self.CubeInterval - 5, posy + self.LowerH - 5, (self.Action.getRecvWndSize() - 1) * self.CubeInterval + self.CubeW + 10, self.CubeH + 10)
        
        tmp = 0
        MsgQue = []
        MsgQue = self.Action.getMsgQueU()
        for i in range(len(MsgQue)):
            qp.setBrush(self.ColorDict[MsgQue[i].attri])
            qp.drawRect(posx + MsgQue[i].getIndex() * self.CubeInterval, posy + self.UpperH, self.CubeW, self.CubeH)
            if MsgQue[i].isSending():
                qp.setBrush(self.Pink)
                rect = QtCore.QRect(posx + MsgQue[i].getIndex() * self.CubeInterval - self.CubeW / 2.0, posy + self.UpperH - self.CubeW / 2.0, self.CubeW, self.CubeW)
                if tmp == 0:
                    qp.drawPie(rect, 90 * 16, - 1.0 * MsgQue[i].getTime() * 5760.0 / self.timeout)
                    if self.Mode == 'GBN':
                        tmp += 1

        MsgQue = []
        MsgQue = self.Action.getMsgQueL()
        for i in range(len(MsgQue)):
            qp.setBrush(self.ColorDict[MsgQue[i].attri])
            qp.drawRect(posx + MsgQue[i].getIndex() * self.CubeInterval, posy + self.LowerH, self.CubeW, self.CubeH)
        MsgQue = []
        MsgQue = self.Action.getMsgQueSend()
        if len(MsgQue) != 0:
            for i in range(len(MsgQue)):
                if MsgQue[i].isActive() == True:
                    qp.setBrush(self.ColorDict[MsgQue[i].attri])
                    qp.drawRect(posx + MsgQue[i].getIndex() * self.CubeInterval, posy + self.UpperH + MsgQue[i].getProgress(), self.CubeW, self.CubeH)

                    
        MsgQue = []
        MsgQue = self.Action.getMsgQueACK()
        if len(MsgQue) != 0:
            for i in range(len(MsgQue)):
                if MsgQue[i].isActive() == True:
                    qp.setBrush(self.ColorDict[MsgQue[i].attri])
                    qp.drawRect(posx + MsgQue[i].getIndex() * self.CubeInterval, posy + self.LowerH - MsgQue[i].getProgress(), self.CubeW, self.CubeH)
                    pass
                pass

#        for i in range(self.SendWndSize):
#            qp.drawRect(posx + self.SendWndBegin * self.CubeInterval - 5, posy + self.UpperH - 5, (self.SendWndSize - 1) * self.CubeInterval + self.CubeW + 10, self.CubeH + 10)
#            pass
        
#        if self.Mode == 'SR':
#            for i in range(self.SendWndSize):
#                qp.drawRect(posx + self.RecvWndBegin * self.CubeInterval - 5, posy + self.LowerH - 5, (self.RecvWndSize - 1) * self.CubeInterval + self.CubeW + 10, self.CubeH + 10)
        
#        qp.setPen(self.Black)
#        qp.setBrush(self.White)
        
#        self.CubeNum = (size.width() + self.CubeInterval) / self.CubeInterval
#        for i in range(self.CubeNum):
#            qp.drawRect(posx + i * self.CubeInterval, posy + self.UpperH, self.CubeW, self.CubeH)
#            qp.drawRect(posx + i * self.CubeInterval, posy + self.LowerH, self.CubeW, self.CubeH)
#            pass
        
        #Dynamic Graphics
        
        pass
    
    def TimerAction(self):
        if self.Mode == 'SR' and self.Start == True:
            self.SR.QueueProc()
            pass
        elif self.Mode == 'GBN' and self.Start == True:
            self.GBN.QueueProc()
            pass
        self.update()
        pass
    
        
    def setParameters(self):
        if self.Mode == 'SR':
            self.SR.setSendWndSize(self.SendWndSize)
            self.SR.setRecvWndSize(self.RecvWndSize)
            self.SR.sete2eDelay(self.e2eDelay)
            self.SR.settimeout(self.timeout)
            self.SR.setpkt(self.pkt)
            self.SR.setSendWndBegin(self.SendWndBegin)
            self.SR.setRecvWndBegin(self.RecvWndBegin)
            self.SR.setNextSend(self.NextSend)
            self.SR.setNextACK(self.NextACK)
            pass
        elif self.Mode == 'GBN':
            self.GBN.setSendWndSize(self.SendWndSize)
            self.GBN.setRecvWndSize(self.RecvWndSize)
            self.GBN.sete2eDelay(self.e2eDelay)
            self.GBN.settimeout(self.timeout)
            self.GBN.setpkt(self.pkt)
            self.GBN.setSendWndBegin(self.SendWndBegin)
            self.GBN.setRecvWndBegin(self.RecvWndBegin)
            self.GBN.setNextSend(self.NextSend)
            self.GBN.setNextACK(self.NextACK)
            pass
        self.SR.__init__()
        self.GBN.__init__()
        pass
    
    def StartAction(self):
        self.Start = True
        if self.isChanged == True:
            self.setParameters()
            self.isChanged = False
        if self.Mode == 'SR':
            self.SR.StartAction()
            pass
        elif self.Mode == 'GBN':
            self.GBN.StartAction()
            pass
        
        pass
    
    def StopAction(self):
        if self.Mode == 'SR':
            self.SR.StopAction()
            pass
        elif self.Mode == 'GBN':
            self.GBN.StopAction()
            pass
        self.Start = False
        pass
    
    def setMode(self, mode):
        if mode == 0:
            self.Mode = 'GBN'
            pass
        elif mode == 1:
            self.Mode = 'SR'
            pass
        self.isChanged = True
        pass
    def setWndSize(self, sz):
        self.SendWndSize = sz
        self.RecvWndSize = sz
        self.isChanged = True
        pass
    def sete2eDelay(self, d):
        self.e2eDelay = d
        self.isChanged = True
        pass
    def settimeout(self, t):
        self.timeout = t
        self.isChanged = True
        pass
    def setpkt(self, p):
        self.pkt = p
        self.isChanged = True
        pass
    def setScrollMode(self, i):
        self.ScrollMode = i
        self.isChanged = True
        pass