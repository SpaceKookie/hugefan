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
import time
from PyQt4 import QtGui, QtCore, uic
from threading import Thread

# Some internal imports
from fan_helper import FanHelper, FanParser

# Some nice constants
__APPNAME__ = 'HugeFan'
__VERSION__ = '0.1'
__DT__ = 0.25

__VERBOSE__ = False

# Some UI modifyers
S_PAD = 15
M_PAD = 25
L_PAD = 50

# Global variables to be used by all threads
hugefan = None
dt = None
gt = None
TERMINATOR = False


class HugeFan(QtGui.QMainWindow):
    def __init__(self):
        super(HugeFan, self).__init__()

        # Setup some basic stuff about this UI
        self.ui = uic.loadUi('layout/main2.ui', self)

        # self.setFixedSize(315, 500)
        self.show()

        # Now actually go and bind functions to it.
        self.bindUI()

    @QtCore.pyqtSlot(int, name='value')
    def open(self, value):
        print "Yay! %d" % value

    def bindUI(self):
        # self.connect(self.ui.actionOpen, QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('open()'))
        self.connect(self.ui.horizontalSlider, QtCore.SIGNAL('valueChanged(int)'), self, QtCore.SLOT('open(value)'))

        #self.connect(self.horizontalSlider, QtCore.SIGNAL("valueChanged(int)"),
        #            self, QtCore.SLOT("some_function(self, value)"))

    def update(self, current_speed, current_temp, target_speed, target_temp):
        pass

def main_gui(args):

    # Init the PyQt core
    core = QtGui.QApplication(args)

    # Init the app class
    global hugefan
    hugefan = HugeFan()

    # Run the actual app and catch the return code for errors.
    status = core.exec_()

    # Make that other thread settle down
    global TERMINATOR
    TERMINATOR = True

    # Wait a bit
    time.sleep(__DT__ * 2)

    # NOW actually quit the app
    sys.exit(status)


def data_thread(dt):
    counter = 0
    while hugefan is None:
        if __VERBOSE__: print("Waiting for thread lock: %d" % counter); counter += 1

    meta = FanParser.parse()
    fan_handler = FanHelper(meta)

    while True:
        if TERMINATOR: break
        # print(meta)
        hugefan.update(fan_handler.get_current_speed(), -1, fan_handler.get_target_speed(), -2)
        time.sleep(dt)


if __name__ == '__main__':
    # Setup threading
    dt = Thread(target=data_thread, args=(__DT__, ))
    gt = Thread(target=main_gui, args=(sys.argv, ))

    # Now start the threads
    dt.start()
    gt.start()

    # Join threads
    dt.join()
    gt.join()

