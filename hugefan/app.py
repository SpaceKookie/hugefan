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
import sys, time

from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import QTimer

from threading import Thread

# Some internal imports
from helpers import DataHandler, FanParser

# Some nice constants
__APPNAME__ = 'HugeFan'
__VERSION__ = '0.2'
__DT__ = 0.25

__VERBOSE__ = False

# Global variables to be used by all threads
huge_fan = None
dt = None
gt = None
TERMINATOR = False

class DataUpdateThread(QtCore.QThread):
    def __init__(self, parent):
        self.parent = parent
        self.running = True

    def make_it_so(self):
        while self.running:
            self.parent.update()

    def terminate(self):
        self.running = False


class HugeFan(QtGui.QMainWindow):
    def __init__(self):
        super(HugeFan, self).__init__()

        # Setup some basic stuff about this UI
        self.ui = uic.loadUi('layout/main.ui', self)

        self.data = DataHandler(None)
        max_fan = self.data.get_max_speed()
        min_fan = self.data.get_min_speed()

        self.ui.speed_slider.setValue(self.data.get_current_speed())
        self.ui.speed_slider.setRange(min_fan, max_fan)
        self.ui.speed_slider.setToolTip("Current target: %d" % self.data.get_target_speed())

        # self.setFixedSize(315, 500)
        self.show()

        # Now actually go and bind functions to it.
        self.bind_ui()

        # Initiate the background data update thread
        self.thread = DataUpdateThread(self)
        self.thread.make_it_so()

    @QtCore.pyqtSlot(int)
    def adjust_speed(self, value):
        self.data.set_target_speed(value)

    # @QtCore.pyqtSlot()
    # def change_state(self):
    #     if self.data.get_manual_state():
    #         self.ui.speed_slider.setEnabled(False)
    #         self.ui.temp_slider.setEnabled(False)
    #         self.data.set_manual_control(False)
    #     else:
    #         self.ui.speed_slider.setEnabled(True)
    #         self.ui.temp_slider.setEnabled(True)
    #         self.data.set_manual_control(True)

    def bind_ui(self):
        # self.connect(self.ui.enable_box, QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('change_state()'))
        self.connect(self.ui.speed_slider, QtCore.SIGNAL('valueChanged(int)'), self, QtCore.SLOT('adjust_speed(int)'))

    def update(self):
        print("Yes")

        # Updating info labels
        # self.ui.content_cur_speed.setText("<b>%s</b>" % self.data.get_current_speed())
        # self.ui.content_cur_temp.setText("<b>%s</b>" % self.data.get_current_temperature())

        # Updating slider positions
        # self.ui.speed_slider.setValue(self.data.get_target_speed())

        # TODO: Update graphs

def main_gui(args):

    # Init the PyQt core
    core = QtGui.QApplication(args)

    # Init the app class
    global huge_fan
    huge_fan = HugeFan()

    # Run the actual app and catch the return code for errors.
    status = core.exec_()

    # Make that other thread settle down
    global TERMINATOR
    TERMINATOR = True

    # Wait a bit
    time.sleep(__DT__ * 2)

    # NOW actually quit the app
    sys.exit(status)



def data_thread(delta):
    counter = 0
    while huge_fan is None:
        if __VERBOSE__:
            print("Waiting [%d] for thread lock" % counter)
            counter += 1

    dh = DataHandler(None)

    while True:
        if TERMINATOR:
            break

        # Updates the UI
        # huge_fan.update()
        time.sleep(delta)


if __name__ == '__main__':

    # This looks up the fan targets and initialises the DataHandler
    tmp = FanParser.parse()
    DataHandler(tmp)

    # Setup threading
    # dt = Thread(target=data_thread, args=(__DT__, ))
    gt = Thread(target=main_gui, args=(sys.argv, ))

    # Now start the threads
    # dt.start()
    gt.start()

    # Join threads
    # dt.join()
    gt.join()

