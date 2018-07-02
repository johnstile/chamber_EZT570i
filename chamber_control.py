#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EZT570i Command Register Reference"""
import logging
import time
from copy import copy

import chamber_commands
import chamber_communication

class Chamber(object):
    """"""
    def __init__(self, log, comm_type, comm_params):
        self.log = log
        self.ccomm = chamber_communication.ChamberCommunication(comm_type, comm_params, log)

    def connect(self):
        self.ccomm.connect()

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

    def start_profile(self):
        # ---------------------------------
        # Start the profile
        # ---------------------------------
        # is the system ready to start?  0 = Yes
        start_reg = chamber_commands.name_to_reg('EZT570I_OFFLINE_DOWNLOAD_PROFILE')
        quantity_of_reg = 1
        values = self.ccomm.read_registers(start_reg, quantity_of_reg)
        self.log.debug("Modbus Response:{}".format(values))
        self.print_read_registers(start_reg, values)

        register, code = chamber_commands.encode_set_value('PROFILE_START_STEP', 1)
        self.ccomm.write_register(register, code)
        start_reg = chamber_commands.name_to_reg('PROFILE_START_STEP')
        quantity_of_reg = 1
        values = self.ccomm.read_registers(start_reg, quantity_of_reg)
        self.log.debug("Modbus Response:{}".format(values))
        self.print_read_registers(start_reg, values)

        register, code = chamber_commands.encode_set_value('PROFILE_CONTROL_STATUS', 'run/resume')
        self.ccomm.write_register(register, code)
        start_reg = chamber_commands.name_to_reg('PROFILE_CONTROL_STATUS')
        quantity_of_reg = 1
        values = self.ccomm.read_registers(start_reg, quantity_of_reg)
        self.log.debug("Modbus Response:{}".format(values))
        self.print_read_registers(start_reg, values)

    def stop_chamber(self):
        register, code = chamber_commands.encode_set_value('PROFILE_CONTROL_STATUS', 'stop/all off')
        self.ccomm.write_register(register, code)
        start_reg = chamber_commands.name_to_reg('PROFILE_CONTROL_STATUS')
        quantity_of_reg = 1
        values = self.ccomm.read_registers(start_reg, quantity_of_reg)
        self.log.debug("Modbus Response:{}".format(values))
        self.print_read_registers(start_reg, values)

    def stop_profile(self):
        register, code = chamber_commands.encode_set_value('PROFILE_CONTROL_STATUS', 'stop/off')
        self.ccomm.write_register(register, code)
        start_reg = chamber_commands.name_to_reg('PROFILE_CONTROL_STATUS')
        quantity_of_reg = 1
        values = self.ccomm.read_registers(start_reg, quantity_of_reg)
        self.log.debug("Modbus Response:{}".format(values))
        self.print_read_registers(start_reg, values)

        register, code = chamber_commands.encode_set_value('LOOP_1_SETPOINT', 25)
        self.ccomm.write_register(register, code)
        start_reg = chamber_commands.name_to_reg('LOOP_1_SETPOINT')
        quantity_of_reg = 1
        values = self.ccomm.read_registers(start_reg, quantity_of_reg)
        self.log.debug("Modbus Response:{}".format(values))
        self.print_read_registers(start_reg, values)

    def print_read_registers(self, start_reg, values):

        self.log.debug("\n\nRead: start_reg:{}, values:{}".format(start_reg, values))
        self.log.debug("data:{}".format(values.data[:]))
        self.log.info("quantity:{}".format(len(values.data)))
        reg = copy(start_reg)
        for value in values.data[:]:
            if value is None:
                self.log.info("value is none")

            reg_name, value_human = chamber_commands.decode_read_value(reg, value)
            self.log.info(
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

    def light(self, state):
        """
        Turn on or off the light
        :param state: on|off
        :return:
        """
        register, code = chamber_commands.encode_set_value('CHAMBER_LIGHT_CONTROL', state)
        self.ccomm.write_register(register, code)
        start_reg = chamber_commands.name_to_reg('CHAMBER_LIGHT_CONTROL')
        values = self.ccomm.read_registers(start_reg, 1)
        self.log.debug("Modbus Response:{}".format(values))
        self.print_read_registers(start_reg, values)

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

    # Connect to the chamber
    comm_type="network"
    comm_params = {
        'net_port' : 50000,
        'net_addr' : '192.168.0.36',
        'net_timeout' : 20
    }
    chamber = Chamber(log, comm_type, comm_params)
    chamber.connect()

    # File recovered from the chambers compact flash
    project_file = 'GALAXY.txt'

    # Print the content of the profile
    chamber.ccomm.print_profile(project_file)

    # Start the Galaxy profile
    chamber.ccomm.load_profile(project_file)
    chamber.start_profile()

    # Toggle light
    chamber.light('on')
    chamber.light('off')
    chamber.light('on')
    chamber.light('off')

    time.sleep(5)
    # End current profile, leave chamber running at safe temp
    chamber.stop_profile()
    # Stop current profile, and stop chamber
    #chamber.stop_chamber()

    # Toggle light
    chamber.light('on')
    chamber.light('off')
    chamber.light('on')
    chamber.light('off')

    # List all the readable registers
    start_reg = chamber_commands.name_to_reg('OPERATIONAL_MODE')
    quantity_of_reg = 200
    values = chamber.ccomm.read_registers(start_reg, quantity_of_reg)
    log.debug("Modbus Response:{}".format(values))
    chamber.print_read_registers(start_reg, values)

if __name__ == '__main__':
    main()
