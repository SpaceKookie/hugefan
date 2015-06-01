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

class FanHelper:

    def __init__(self, meta):
        pass

    def get_current_speed(self):
        pass

    def get_target_speed(self):
        pass

    def get_speed_bounds(self):
        pass

    def get_min_speed(self):
        pass

    def get_max_speed(self):
        pass

    def set_manual_control(self, bool):
        pass

    def set_speed(self, speed):
        pass