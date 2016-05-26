#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Course Project 4
Detail Action for Selective Repeat

author: Junyong Wang

last edited: May 2016
"""
import sys
from PyQt4 import QtGui, QtCore
from Message import *
class SRAction():
    def __init__(self):
        self.Start = False
        self.SendWndSize = 5
        self.SendWndBegin = 5
        self.RecvWndSize = 5
        self.RecvWndBegin = 5
        self.NextSend = 5
        self.Start = False
        self.MsgQueU = []
        self.MsgQueL = []
        self.MaxSz = 100
        self.MsgQueSend = []
        self.MsgQueACK = []
        for i in range(self.MaxSz):
            self.MsgQueU.append(Msg(1, i))
            self.MsgQueL.append(Msg(0, i))
            pass
        pass
    def Ready2Send(self):
        if (self.NextSend < self.SendWndBegin + self.SendWndSize) and self.Start == True:
            self.Send(self.NextSend)
            self.NextSend += 1
        pass
    def Send(self, i):
        self.MsgQueSend.append(Msg(1, i))
        self.MsgQueSend[-1].Active()  
        self.MsgQueU[i].Sending()
        pass
    
    def SendACK(self, i):
        self.MsgQueACK.append(Msg(2, i))
        self.MsgQueACK[-1].Active()
        pass
    
    def Resend(self):
        for i in range(len(self.MsgQueU)):
            if self.MsgQueU[i].isSending():
                if self.MsgQueU[i].getTime() >= self.timeout:
                    self.MsgQueU[i].ResetTime()
                    self.Send(self.MsgQueU[i].getIndex())
                    pass
                pass
            pass
        pass
    
    def Recv(self, i):
        self.MsgQueL[i].setAtrribute(4)
        if self.MsgQueL[i].isSucceed() == False:
            self.MsgQueL[i].Succeed()
            self.MsgQueL[i].setAtrribute(4)
            self.SendACK(self.MsgQueL[i].getIndex())
            self.RecvWndBegin += 1
        pass
    
    def RecvACK(self, i):
        if self.MsgQueU[i].isSucceed() == False:
            self.MsgQueU[i].Succeed()
            self.MsgQueU[i].setAtrribute(3)
            self.SendWndBegin += 1
        pass
    def getNextSend(self):
        return self.NextSend
    
    def QueueProc(self):
        delList = []
        if len(self.MsgQueSend) > 0:
            for i in range(len(self.MsgQueSend)):
                if self.MsgQueSend[i].isArrive():
                    self.Recv(self.MsgQueSend[i].getIndex())
                    delList.append(i)
                elif self.MsgQueSend[i].isActive():
                    self.MsgQueSend[i].PlusProgress(400.0 * 20.0 / self.e2eDelay)
                    pass
                pass
            pass
        for i in range(len(delList)):
            del self.MsgQueSend[i]
        delList = []
        if len(self.MsgQueACK) > 0:
            for i in range(len(self.MsgQueACK)):
                if self.MsgQueACK[i].isArrive():
                    self.RecvACK(self.MsgQueACK[i].getIndex())
                    delList.append(i)
                    pass
                elif self.MsgQueACK[i].isActive():
                    self.MsgQueACK[i].PlusProgress(400.0 * 20.0 / self.e2eDelay)
                    pass
                pass
        for i in range(len(delList)):
            del self.MsgQueACK[i]
        for i in range(len(self.MsgQueU)):
            if self.MsgQueU[i].isSending():
                self.MsgQueU[i].addTime()
        self.Resend()
        pass
    
    def PageLeft(self, d):
        self.NextSend -= d
        self.SendWndBegin -= d
        self.RecvWndBegin -= d
        del self.MsgQueU[0:d]
        del self.MsgQueL[0:d]
        for i in range(d):
            self.MsgQueU.append(Msg(1, self.MaxSz - d + i))
            self.MsgQueL.append(Msg(0, self.MaxSz - d + i))
        for i in range(0, self.MaxSz - d):
            self.MsgQueU[i].setIndex(self.MsgQueU[i].getIndex() - d)
            self.MsgQueL[i].setIndex(self.MsgQueL[i].getIndex() - d)
            pass
        if len(self.MsgQueSend) != 0:
            for i in range(len(self.MsgQueSend)):
                self.MsgQueSend[i].setIndex(self.MsgQueSend[i].getIndex() - d)
                pass
            pass
        if len(self.MsgQueACK) != 0:
            for i in range(len(self.MsgQueACK)):
                self.MsgQueACK[i].setIndex(self.MsgQueACK[i].getIndex() - d)
                pass
            pass
        pass
    def getMsgQueU(self):
        return self.MsgQueU
    def getMsgQueL(self):
        return self.MsgQueL
    def getMsgQueSend(self):
        return self.MsgQueSend
    def getMsgQueACK(self):
        return self.MsgQueACK
    def getSendWndBegin(self):
        return self.SendWndBegin
    def getRecvWndBegin(self):
        return self.RecvWndBegin
    def getSendWndSize(self):
        return self.SendWndSize
    def getRecvWndSize(self):
        return self.RecvWndSize
    def StartAction(self):
        self.Start = True
        pass
    def StopAction(self):
        self.Start = False
        pass
    def setSendWndSize(self, sz):
        self.SendWndSize = sz
        pass
    def setRecvWndSize(self, sz):
        self.RecvWndSize = sz
        pass
    def sete2eDelay(self, delay):
        self.e2eDelay = delay
        pass
    def settimeout(self, to):
        self.timeout = to
        pass
    def setpkt(self, p):
        self.pkt = p
        pass
    def setSendWndBegin(self, bg):
        self.SendWndBegin = bg
        self.NextSend = bg + 1
        pass
    def setRecvWndBegin(self, bg):
        self.RecvWndBegin = bg
        pass
    def setNextSend(self, s):
        self.NextSend = s
        pass
    def setNextACK(self, a):
        self.NextACK = a
        pass