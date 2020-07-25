#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is what your program will instantiate to talk to the chamber 

By John Stile At Meyer Sound Laboratories Inc.
this is distributed under a MIT license, see LICENSE
"""


import logging
import time
from copy import copy
import chamber_commands
import chamber_communication


class Chamber(object):
    """EZT570i Chamber functional interface"""

    def __init__(self, log, comm_params):
        self.log = log
        self.ccomm = chamber_communication.ChamberCommunication(comm_params, log)

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
        self.toggle_light(2)

        download_state = self.get_register('EZT570I_OFFLINE_DOWNLOAD_PROFILE')
        self.log.info("EZT570I_OFFLINE_DOWNLOAD_PROFILE:{}".format(download_state))

        # Read the file and load into chamber
        self.ccomm.load_profile(project_file)

        retry = 10
        while retry:
            retry -= 1
            time.sleep(1)
            # is the system ready to start?  0 = Yes
            download_state = self.get_register('EZT570I_OFFLINE_DOWNLOAD_PROFILE')
            self.log.info("EZT570I_OFFLINE_DOWNLOAD_PROFILE:{}".format(download_state))
            if download_state == "Online":
                self.log.info("Start Profile")
                self.set_register('PROFILE_START_STEP', 1)
                self.set_register('PROFILE_CONTROL_STATUS', 'run/resume')
                retry = 0
                continue
            else:
                self.log.info("Waiting For Chamber Ready")

        self.toggle_light(2)

    def stop_profile(self):
        """Stop profile and set safe temp"""
        self.set_register('PROFILE_CONTROL_STATUS', 'stop/off')
        self.temperature = 25

    def stop_chamber(self):
        """Stop profile and turn off pump"""
        self.set_register('PROFILE_CONTROL_STATUS', 'stop/all off')

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

    def toggle_light(self, toggles):
        for i in range(toggles):
            if i % 2:
                self.light = 'off'
            else:
                self.light = 'on'
            self.log.info("Chamber light:{}".format(self.light))
        time.sleep(0.5)

    @property
    def temperature(self):
        temp = self.get_register('LOOP_1_PROCESS_VALUE')
        return temp['degrees']

    @temperature.setter
    def temperature(self, value):
        self.set_register('LOOP_1_SETPOINT', value)

    @property
    def profile_control_status(self):
        status = self.get_register('PROFILE_CONTROL_STATUS')
        return status['mode']

    @profile_control_status.setter
    def profile_control_status(self, state):
        self.set_register('PROFILE_CONTROL_STATUS', state)

    @property
    def profile_current_step(self):
        temp = self.get_register('PROFILE_CURRENT_STEP')
        return temp['step']

    @property
    def alarms(self):
        """Return decoded alarms for these 5 registers
            EZT570I_ALARM_STATUS
            INPUT_ALARM_STATUS
            CHAMBER_ALARM_STATUS
            REFRIGERATION_ALARM_STATUS
            SYSTEM_STATUS_MONITOR
        """
        #alarm_names [
        #   'EZT570I_ALARM_STATUS'
        #   'INPUT_ALARM_STATUS'
        #   'CHAMBER_ALARM_STATUS'
        #   'REFRIGERATION_ALARM_STATUS'
        #   'SYSTEM_STATUS_MONITOR'
        #]      
        #start_reg = chamber_commands.name_to_reg('EZT570I_ALARM_STATUS')
        #values = self.ccomm.read_registers(start_reg, 5)
        #self.log.debug("Modbus Response:{}".format(values))

        alarms_read = {}
        alarms_read['ezt570i']  = self.get_register('EZT570I_ALARM_STATUS')
        alarms_read['input']  = self.get_register('INPUT_ALARM_STATUS')
        alarms_read['chamber']  = self.get_register('CHAMBER_ALARM_STATUS')
        alarms_read['refrig']  = self.get_register('REFRIGERATION_ALARM_STATUS')
        alarms_read['system']  = self.get_register('SYSTEM_STATUS_MONITOR')
         
        self.log.debug("alarms:{}".format(alarms_read))
        return alarms_read

    def log_a_dict(self, header, my_dict):
        """Uniform printing of dictinaries to log file
        Pads and indents for eaiser viewing
        Draws dots from the key to the value
        sorts alphabetically"""
        spacing = 40
        delimiter = '.'
        alignment = '<'
        self.log.info("{header}".format(header="=" * (spacing + 20)))
        self.log.info(header)
        for k, v in sorted(my_dict.iteritems()):
            self.log.info(
                (
                    "{key:{delimiter}{alignment}{spacing}} {value}"
                ).format(
                    key=k,
                    delimiter=delimiter,
                    alignment=alignment,
                    spacing=spacing,
                    value=v
                )
            )
        return("{header}".format(header="=" * (spacing + 20)))

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
    comm_params = {
        'comm_type': "network",
        'net_port': 50000,
        'net_addr': '192.168.0.36',
        'net_timeout': 20
    }
    chamber = Chamber(log, comm_params)
    chamber.connect()

    # File recovered from the chambers compact flash
    project_file = 'GALAXY.txt'
    #project_file = 'GALILEO.txt'

    # Print the content of the profile
    chamber.print_profile(project_file)

    log.info("Load and start profile:{}".format(project_file))
    chamber.start_profile(project_file)
    chamber.toggle_light(2)

    monitor_time = 10
    log.info("Monitor chamber temp for {} seconds".format(monitor_time))
    end_time = time.time() + monitor_time
    while time.time() <= end_time:
        log.info("Chamber Temp:{}".format(chamber.temperature))
    chamber.toggle_light(2)

    # NOTE:You can do only one of these 
    # log.info("End current profile, leave chamber running at safe temp")
    # chamber.stop_profile()
    log.info("Stop current profile, and stop chamber")
    chamber.stop_chamber()

    log.info("List all the readable registers")
    chamber.print_all_registers()

    # Print all alarm registers
    for k,v in chamber.alarms.iteritems():
        log.info(chamber.log_a_dict(k, v))
    
    #log.info("Profile Current Step:{}".format(chamber.profile_current_step))



if __name__ == '__main__':
    main()
