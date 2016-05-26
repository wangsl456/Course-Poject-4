#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Course Project 4
Message Class

author: Junyong Wang

last edited: May 2016
"""
import sys, random
from PyQt4 import QtCore
class Msg():
    def __init__(self, att, idx):
        # 0 -- no data received yet
        # 1 -- data buffered (ready to send, delivered or sent but no ack received yet)
        # 2 -- ack
        # 3 -- transmission confirmed
        # 4 -- data has been delivered to upper network layer
        self.attri = att
        self.index = idx
        self.arrive = False
        self.succeed = False
        self.progress = 0
        self.time = 0
        self.timeout = False
        self.active = False
        self.sending = False
        pass
    
    def setAtrribute(self, a):
        self.attri = a
        pass
    def setIndex(self, i):
        self.index = i
    def Arrive(self):
        self.arrive = True
        self.active = False
        self.progress = 0
        pass
    def Active(self):
        self.active = True
        self.arrive = False
        self.timeout = False
        self.time = 0
        self.progress = 0
        self.succeed = False
        self.sending = True
        pass
    def Deactive(self):
        self.active = False
        pass
    def Succeed(self):
        self.succeed = True
        self.arrive = False
        self.progress = 0
        self.time = 0
        self.timeout = False
        self.active = False
        self.sending = False
        pass
    def Sending(self):
        self.sending = True
    def isArrive(self):
        return self.arrive
    def isActive(self):
        return self.active
    def isSucceed(self):
        return self.succeed
    def isSending(self):
        return self.sending
    def PlusProgress(self, d):
        self.progress += d
        if self.progress >= 400.0:
            self.Arrive()
            pass
        pass
    def ResetTime(self):
        self.time = 0
        pass
    def getTime(self):
        return self.time
    def getProgress(self):
        return self.progress
    def getIndex(self):
        return self.index
    def addTime(self):
        if self.succeed == False:
            self.time += 20.0
            pass