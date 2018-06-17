#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EZT570i Command Register Reference"""
import binascii
import logging

import ctypes
import sys
import time

import os
import struct
from copy import copy

import chamber_commands
import chamber_communication
import modbus_packets

class Chamber(object):
    """"""
    def __init__(self, log, comm_type):
        self.log = log
        self.creg = chamber_commands.ChamberCommandRegisters()
        self.ccomm = chamber_communication.ChamberCommunication(comm_type, log)

    def connect(self):
        self.ccomm.connect_to_chamber()

    @property
    def operational_mode(self, value):
        """Read Operation Mode"""
        response = None
        assert 0 <= value <= 1
        if value == 0:
            response = "off"
        elif value == 1:
            response = "on"
        return response

    @property
    def clock(self):
        """Read the clock
        Registers:
        'CLOCK_YY_MM': 1,  # r, Clock (Year, Month)
        'CLOCK_DAY_DOE': 2,  # r, Clock (Day, DOE)
        'CLOCK_HH_MM': 3,  # r, Clock (Hours, Min)
        'CLOCK_SEC': 4,  # r, Clock (Seconds)
        """
        response = None
        value = self.ccom.read_registers(self.creg.ctrl[ 'CLOCK_YY_MM'], 4)
        # Break into 4x 2 byte chunks
        yy_mm, day_doe, hh_mm, sec = memoryview(value).cast('H')
        # split into 1 byte parts
        year, month = yy_mm
        day, doe = day_doe
        hour, minute = hh_mm
        seconds = sec
        response = [ year, month, day, doe, hour, minute, hour, minute, seconds]
        return response


def main():
    """Example of using this class
    """
    # --------------------
    # Logging setup
    # --------------------
    ch = logging.StreamHandler()
    ch_fmt = logging.Formatter("%(levelname)s\t: %(message)s")
    ch.setFormatter(ch_fmt)
    log = logging.getLogger()
    log.addHandler(ch)
    log.setLevel(logging.INFO)  # DEBUG,INFO,WARNING,ERROR,CRITICAL
    log.debug("Initialized Logger")
    comm_type="network"
    chamber = Chamber(log, comm_type)

    # ----------------------------------
    # Open communicaiton
    # ----------------------------------
    chamber.ccomm.connect()

    # ----------------------------------
    # Load Profile file
    # ----------------------------------
    project_file = 'GALAXY.txt'
    chamber.ccomm.load_profile(project_file)

    #----------------------------------
    # Write Value
    #-----------------------------------
    register, code = chamber.creg.encode_set_value('CHAMBER_LIGHT_CONTROL', 'on')
    chamber.ccomm.write_register(register, code)

    start_reg = chamber.creg.name_to_reg('CHAMBER_LIGHT_CONTROL')
    quantity_of_reg = 1
    values = chamber.ccomm.read_registers(start_reg, quantity_of_reg)
    log.info("Modbus Response:{}".format(values))
    print_read_registers(chamber, log, start_reg, values)

    register, code = chamber.creg.encode_set_value('CHAMBER_LIGHT_CONTROL', 'off')
    chamber.ccomm.write_register(register, code)

    start_reg = chamber.creg.name_to_reg('CHAMBER_LIGHT_CONTROL')
    quantity_of_reg = 1
    values = chamber.ccomm.read_registers(start_reg, quantity_of_reg)
    log.info("Modbus Response:{}".format(values))
    print_read_registers(chamber, log, start_reg, values)

    #----------------------------------
    # Read x registers
    # #----------------------------------
    start_reg = chamber.creg.name_to_reg('OPERATIONAL_MODE')
    quantity_of_reg = 60
    values = chamber.ccomm.read_registers(start_reg, quantity_of_reg)
    log.info("Modbus Response:{}".format(values))

    print_read_registers(chamber, log, start_reg, values)

def print_read_registers(chamber, log, start_reg, values):
    # this is the most promising

    log.info("\n\nRead: start_reg:{}, values:{}".format(start_reg, values))
    log.info("data:{}".format(values.data[:]))
    log.info("quantity:{}".format(len(values.data)))
    reg = copy(start_reg)
    for value in values.data[:]:
        if value is None:
            log.info("value is none")

        reg_name, value_human = chamber.creg.decode_read_value(reg, value)
        log.info(
            (
                "register:{:04x}, reg_name:{:<50}, value:{:04x}, value_human:{}"
            ).format(
                reg,
                reg_name,
                value,
                value_human
            )
        )
        reg += 1


if __name__ == '__main__':
    main()
