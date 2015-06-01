__author__ = 'spacekookie'
'''
DESCRIPTION:    Huge Fan is a fan control utility that uses lm_sensors and the /proc folder structure to control
                your fan speeds manually depending on the temperature. This is meant for system where the kernel
                doesn't properly contorl fan speeds already and PWM is not available.
AUTHOR:         Katharina 'spacekookie' Sabel <sabel.katharina@gmail.com>
LICENSE:        GNU Public License 3.0
'''

''' This file contains helper classes to handle interactions with fans '''

# Rename the input to something easy and quick to write
import subprocess as sh

class FanParser:

    @staticmethod
    def parse():
        cmd = "find /sys -name 'fan*'"
        # "cwm --rdf test.rdf --ntriples > test.nt"

        process = sh.Popen(cmd, stdout=sh.PIPE, shell=True)
        output = process.communicate()[0].split('\n')

        targets = {}

        for candy in output:
            if 'manual' in candy: targets['manual'] = candy
            if 'output' in candy: targets['output'] = candy
            if 'max' in candy: targets['max'] = candy
            if 'min' in candy: targets['min'] = candy

        return targets

class DataHandler:
    class __DataHandler:
        def __init__(self, meta):
            self.meta = meta
            self.manual = False

            self.speed_max = 5500
            self.speed_min = 2500

            self.current_speed = 2750
            self.target_speed = 2750

            self.current_temp = -1
            self.target_temp = -1

    instance = None

    def __init__(self, meta):
        if not DataHandler.instance:
            DataHandler.instance = DataHandler.__DataHandler(meta)
        else:
            DataHandler.instance.val = meta

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __read_value(self, target):
        cmd = 'cat %s' % self.meta[target]
        process = sh.Popen(cmd, stdout=sh.PIPE, shell=True)
        return process.communicate()[0]

    def __write_value(self, target, value):
        pass

    def set_manual_control(self, boolean):
        self.manual = boolean

    def get_manual_state(self):
        return self.manual

    def get_current_speed(self):
        return self.current_speed

    def get_target_speed(self):
        return self.target_speed

    def set_target_speed(self, speed):
        self.target_speed = speed
        self.current_speed = speed

    def get_min_speed(self):
        return self.speed_min

    def get_max_speed(self):
        return self.speed_max

    def get_current_temperature(self):
        return self.current_temp

    def get_target_temperature(self):
        return self.target_temp

    def set_target_temperature(self, temp):
        self.target_temp = temp
