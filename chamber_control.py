#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from copy import copy
import chamber_commands
import chamber_communication

class Chamber(object):
    """EZT570i Chamber functional interface"""
    def __init__(self, log, comm_type, comm_params):
        self.log = log
        self.ccomm = chamber_communication.ChamberCommunication(comm_type, comm_params, log)

    def connect(self):
        self.ccomm.connect()

    def disconnect(self):
        self.ccomm.disconnect()

    def get_register(self, reg_name):
        """Return value given human readable register name"""
        start_reg = chamber_commands.name_to_reg(reg_name)
        values = self.ccomm.read_registers(start_reg, 1)
        self.log.debug("Modbus Response:{}".format(values))
        value_human = chamber_commands.decode_read_value(start_reg, values.data[0])
        return value_human

    def set_register(self, reg_name, value):
        """Set value given human readable register name and value"""
        register, code = chamber_commands.encode_set_value(reg_name, value)
        self.ccomm.write_register(register, code)
        start_reg = chamber_commands.name_to_reg(reg_name)
        quantity_of_reg = 1
        values = self.ccomm.read_registers(start_reg, quantity_of_reg)
        self.log.debug("Modbus Response:{}".format(values))

    def print_read_registers(self, start_reg, values):
        """Mostly for development, to show state of machine"""
        self.log.debug("\n\nRead: start_reg:{}, values:{}".format(start_reg, values))
        self.log.debug("data:{}".format(values.data[:]))
        self.log.info("quantity:{}".format(len(values.data)))
        reg = copy(start_reg)
        for value in values.data[:]:
            if value is None:
                self.log.info("value is none")
            reg_name = chamber_commands.reg_value_to_name(reg)
            value_human = chamber_commands.decode_read_value(reg, value)
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

    def print_all_registers(self):
        start_reg = chamber_commands.name_to_reg('OPERATIONAL_MODE')
        quantity_of_reg = 200
        values = self.ccomm.read_registers(start_reg, quantity_of_reg)
        self.log.debug("Modbus Response:{}".format(values))
        self.print_read_registers(start_reg, values)

    def print_profile(self, project_file):
        """Display the profile"""
        self.ccomm.print_profile(project_file)

    def start_profile(self, project_file):
        # Read the file and load into chamber
        self.ccomm.load_profile(project_file)
       
        # is the system ready to start?  0 = Yes
        download_state = self.get_register('EZT570I_OFFLINE_DOWNLOAD_PROFILE')
        if not download_state:
            self.set_register('PROFILE_START_STEP', 1)
            self.set_register('PROFILE_CONTROL_STATUS', 'run/resume')

    def stop_chamber(self):
        """Stop profile and turn off pump"""
        self.set_register('PROFILE_CONTROL_STATUS', 'stop/all off')

    def stop_profile(self):
        """Stop profile and set safe temp"""
        self.set_register('PROFILE_CONTROL_STATUS', 'stop/off')
        self.temperature = 25

    @property
    def light(self):
        return self.get_register('CHAMBER_LIGHT_CONTROL')

    @light.setter
    def light(self, state):
        """Turn on or off the light
        :param str state: 'on'|'off'
        """
        self.log.info("Light {}".format(state))
        self.set_register('CHAMBER_LIGHT_CONTROL', state)

    @property
    def temperature(self):
        dict = self.get_register('LOOP_1_PROCESS_VALUE')
        return dict['degrees']

    @temperature.setter
    def temperature(self, value):
        self.set_register('LOOP_1_SETPOINT', value)

    @property
    def profile_control_status(self):
        dict = self.get_register('PROFILE_CONTROL_STATUS')
        return dict['mode']

    @profile_control_status.setter
    def profile_control_status(self, state):
        self.set_register('PROFILE_CONTROL_STATUS', state)


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
    chamber.print_profile(project_file)
    
    # Start the Galaxy profile
    chamber.start_profile(project_file)

    # Toggle light
    for i in range(4):
        if i%2:
            chamber.light = 'off'
        else:
            chamber.light = 'on'
        log.info("Chamber light:{}".format(chamber.light))

    time.sleep(5)

    # End current profile, leave chamber running at safe temp
    chamber.stop_profile()
    # Stop current profile, and stop chamber
    #chamber.stop_chamber()

    # Toggle light
    for i in range(4):
        if i%2:
            chamber.light = 'off'
        else:
            chamber.light = 'on'
        log.info("Chamber light:{}".format(chamber.light))


    # Show current mode
    log.info("Chamber Mode:{}".format(chamber.profile_control_status))

    # Monitor chamber temp
    monitor_time = 10
    end_time = time.time() + monitor_time
    while time.time() <= end_time:
        log.info("Chamber Temp:{}".format(chamber.temperature))

    # List all the readable registers
    chamber.print_all_registers()


if __name__ == '__main__':
    main()
