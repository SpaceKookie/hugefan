#!/usr/bin/python3.4

__author__ = 'spacekookie'
'''
DESCRIPTION:    Huge Fan is a fan control utility that uses lm_sensors and the /proc folder structure to control
                your fan speeds manually depending on the temperature. This is meant for system where the kernel
                doesn't properly contorl fan speeds already and PWM is not available.
AUTHOR:         Katharina 'spacekookie' Sabel <sabel.katharina@gmail.com>
LICENSE:        GNU Public License 3.0
'''

''' This file contains the main code for the app as well as PyQt handlers to draw windows '''

# Some imports for Qt and sys calls.
import sys
from PyQt4 import QtGui, QtCore, uic

# Some internal imports
from fan_helper import FanHelper, FanParser

# Some nice constants
__APPNAME__ = 'HugeFan'
__VERSION__ = '0.1'

# Some UI modifyers
S_PAD = 15
M_PAD = 25
L_PAD = 50

class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        # Setup some basic stuff about this UI
        uic.loadUi('layout/main.ui', self)
        self.setFixedSize(315, 500)
        self.show()

        # This will setup some stuff for background logic
        FanParser()

        # Now actually go and bind functions to it.
        self.bindUI()

    def bindUI(self):
        pass

    def runLoop(self):
        print("UPDATING!")

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()