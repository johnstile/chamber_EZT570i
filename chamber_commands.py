#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EZT570i Command Register Reference"""
import struct
import ctypes

class BitFields(ctypes.BigEndianStructure):
    """Several registers hold bit-oriented data"""
    _fields_ = [
        ("bit1", ctypes.c_uint8, 1),  # asByte & 1
        ("bit2", ctypes.c_uint8, 1),  # asByte & 2
        ("bit3", ctypes.c_uint8, 1),  # asByte & 4
        ("bit4", ctypes.c_uint8, 1),  # asByte & 8
        ("bit5", ctypes.c_uint8, 1),  # asByte & 16
        ("bit6", ctypes.c_uint8, 1),  # asByte & 32
        ("bit7", ctypes.c_uint8, 1),  # asByte & 64
        ("bit8", ctypes.c_uint8, 1),  # asByte & 128
        ("bit9", ctypes.c_uint8, 1),  # asByte & 512
        ("bit10", ctypes.c_uint8, 1),  # asByte & 1024
        ("bit11", ctypes.c_uint8, 1),  # asByte & 2048
        ("bit12", ctypes.c_uint8, 1),  # asByte & 4096
        ("bit13", ctypes.c_uint8, 1),  # asByte & 16384
        ("bit14", ctypes.c_uint8, 1),  # asByte & 32768
        ("bit15", ctypes.c_uint8, 1),  # asByte & 65536
        ("bit16", ctypes.c_uint8, 1),  # asByte & 65536
    ]

a_state = {
    0: 'normal',
    1: 'Alarm'
}

int_to_two_bytes = struct.Struct('!h').pack

class ChamberCommandRegisters(object):
    """Read and Write Registers
    Used in Read Registers Command (0x03) for multi register read.
    Used in Write Register Commnad (0x06) for single register write.
    """

    def __init__(self, log):
        self.log = log

    # Dictionary map registers to function
    ctrl = {
        'OPERATIONAL_MODE': 0,  # r,
        'CLOCK_YY_MM': 1,  # r, Clock (Year, Month)
        'CLOCK_DAY_DOW': 2,  # r, Clock (Day, DOE)
        'CLOCK_HH_MM': 3,  # r, Clock (Hours, Min)
        'CLOCK_SEC': 4,  # r, Clock (Seconds)
        'POWER_RECOVERY_MODE': 5,  # r/w, Power Recovery Mode
        'POWER_OUT_TIME': 6,  # r/w,
        'DEFROST_OPERATING_MODE': 7,  # r/w,
        'AUTO_DEFROST_TEMPERATURE_SETPOINT': 8,  # r/w
        'AUTO_DEFROST_TIME_INTERVAL': 9,  # r/w
        'DEFROST_STATUS': 10,  # r,
        'TIME_REMAINING_UNTIL_NEXT_DEFROST': 11,  # r,
        'PRODUCT_CONTROL': 12,  # r/w
        'PRODUCT_CONTROL_UPPER_SETPOINT': 13,  # r/w,
        'PRODUCT_CONTROL_LOWER_SETPOINT': 14,  # r/w,
        'CONDENSATION_CONTROL': 15,  # r/w,
        'CONDENSATION_CONTROL_MONITOR_MODE': 16,  # r/w,
        'CONDENSATION_CONTROL_INPUT_SELECTION': 17,  # r/w,
        'CONDENSATION_CONTROL_TEMPERATORE_RAMP_RATE_LIMIT': 18,  # r/w,
        'CONDENSATION_CONTROL_DEUPOINT_LIMIT': 19,  # r,
        'CONDENSATION_CONTROL_DUEPOINT_ACTUAL': 20,  # r,
        'CHAMBER_LIGHT_CONTROL': 21,  # r/w,
        'CHAMBER_MANUAL_EVENT_CONTROL': 22,  # r/w,
        'CUSTOMER_MANUAL_EVENT_CONTROL': 23,  # r/w,
        'PROFILE_CONTROL_STATUS': 24,  # r/w,
        'PROFILE_ADVANCED_STEP': 25,  # w,
        'PROFILE_NAME_CH_1_2': 26,  # r,
        'PROFILE_NAME_CH_3_4': 27,  # r,
        'PROFILE_NAME_CH_5_6': 28,  # r,
        'PROFILE_NAME_CH_7_8': 29,  # r,
        'PROFILE_NAME_CH_9_10': 30,  # r,
        'PROFILE_START_DATE_YY_MM': 31,  # r,
        'PROFILE_STOP_DATE_YY_MM': 34,  # r,
        'PROFILE_START_DATE_DAY_DOW': 32,  # r,
        'PROFILE_STOP_DATE_DAY_DOW': 35,  # r,
        'PROFILE_START_DATE_HH_MM': 33,  # r,
        'PROFILE_STOP_DATE_HH_MM': 36,  # r,
        'PROFILE_START_STEP': 37,  # r/w,
        'PROFILE_CURRENT_STEP': 38,  # r,
        'PROFILE_LAST_STEP': 39,  # r,
        'PROFILE_TIME_LEFT_IN_CURRENT_STEP_HHH': 40,  # r,
        'PROFILE_TIME_LEFT_IN_CURRENT_STEP_MM_SS': 41,  # r,
        'PROFILE_WAIT_FOR_STATUS': 42,  # r,
        'PROFILE_WAIT_FOR_SETPOINT': 43,  # r,
        'PROFILE_CURRENT_JUMP_STEP': 44,  # r,
        'PROFILE_JUMPS_REMAINING_IN_CURRENT_STEP': 45,  # r,
        'PROFILE_LOOP_1_TARGET_SETPOINT': 46,  # r,
        'PROFILE_LOOP_2_TARGET_SETPOINT': 47,  # r,
        'PROFILE_LOOP_3_TARGET_SETPOINT': 48,  # r,
        'PROFILE_LOOP_4_TARGET_SETPOINT': 49,  # r,
        'PROFILE_LOOP_5_TARGET_SETPOINT': 50,  # r,
        'PROFILE_LAST_JUMP_FROM_STEP': 51,  # r,
        'PROFILE_LAST_JUMP_TO_STEP': 52,  # r,
        'PROFILE_TOTAL_JUMPS_MADE': 53,  # r,
        'ALARM_ACKNOWLEDGE': 54,  # w,
        'EZT570I_ALARM_STATUS': 55,  # w,
        'INPUT_ALARM_STATUS': 56,  # w,
        'CHAMBER_ALARM_STATUS': 57,  # w,
        'REFRIGERATION_ALARM_STATUS': 58,  # w,
        'SYSTEM_STATUS_MONITOR': 59,  # r,
        'LOOP_1_SETPOINT': 60,  # r/w,
        'LOOP_2_SETPOINT': 72,  # r/w,
        'LOOP_3_SETPOINT': 84,  # r/w,
        'LOOP_4_SETPOINT': 96,  # r/w,
        'LOOP_5_SETPOINT': 108,  # r/w,
        'LOOP_1_PROCESS_VALUE': 61,  # r/w,
        'LOOP_2_PROCESS_VALUE': 73,  # r/w,
        'LOOP_3_PROCESS_VALUE': 85,  # r/w,
        'LOOP_4_PROCESS_VALUE': 97,  # r/w,
        'LOOP_5_PROCESS_VALUE': 109,  # r/w,
        'LOOP_1_PERCENT_OUTPUT': 62,  # r,
        'LOOP_2_PERCENT_OUTPUT': 74,  # r,
        'LOOP_3_PERCENT_OUTPUT': 86,  # r,
        'LOOP_4_PERCENT_OUTPUT': 98,  # r,
        'LOOP_5_PERCENT_OUTPUT': 110,  # r,
        'LOOP_1_AUTOTUNE_STATUS': 63,  # r/w,
        'LOOP_2_AUTOTUNE_STATUS': 75,  # r/w,
        'LOOP_3_AUTOTUNE_STATUS': 87,  # r/w,
        'LOOP_4_AUTOTUNE_STATUS': 99,  # r/w,
        'LOOP_5_AUTOTUNE_STATUS': 111,  # r/w,
        'LOOP_1_UPPER_SETPOINT_LIMIT': 64,  # r/w,
        'LOOP_2_UPPER_SETPOINT_LIMIT': 76,  # r/w,
        'LOOP_3_UPPER_SETPOINT_LIMIT': 88,  # r/w,
        'LOOP_4_UPPER_SETPOINT_LIMIT': 100,  # r/w,
        'LOOP_5_UPPER_SETPOINT_LIMIT': 112,  # r/w,
        'LOOP_1_LOWER_SETPOINT_LIMIT': 65,  # r/w,
        'LOOP_2_LOWER_SETPOINT_LIMIT': 77,  # r/w,
        'LOOP_3_LOWER_SETPOINT_LIMIT': 89,  # r/w,
        'LOOP_4_LOWER_SETPOINT_LIMIT': 101,  # r/w,
        'LOOP_5_LOWER_SETPOINT_LIMIT': 113,  # r/w,
        'LOOP_1_ALARM_TYPE': 66,  # r/w,
        'LOOP_2_ALARM_TYPE': 78,  # r/w,
        'LOOP_3_ALARM_TYPE': 90,  # r/w,
        'LOOP_4_ALARM_TYPE': 102,  # r/w,
        'LOOP_5_ALARM_TYPE': 114,  # r/w,
        'LOOP_1_ALARM_MODE': 67,  # r/w,
        'LOOP_2_ALARM_MODE': 79,  # r/w,
        'LOOP_3_ALARM_MODE': 91,  # r/w,
        'LOOP_4_ALARM_MODE': 103,  # r/w,
        'LOOP_5_ALARM_MODE': 115,  # r/w,
        'LOOP_1_ALARM_OUTPUT_ASSIGNMENT': 68,  # r/w,
        'LOOP_2_ALARM_OUTPUT_ASSIGNMENT': 80,  # r/w,
        'LOOP_3_ALARM_OUTPUT_ASSIGNMENT': 92,  # r/w,
        'LOOP_4_ALARM_OUTPUT_ASSIGNMENT': 104,  # r/w,
        'LOOP_5_ALARM_OUTPUT_ASSIGNMENT': 116,  # r/w,
        'LOOP_1_HIGH_ALARM_SETPOINT': 69,  # r/w,
        'LOOP_2_HIGH_ALARM_SETPOINT': 81,  # r/w,
        'LOOP_3_HIGH_ALARM_SETPOINT': 93,  # r/w,
        'LOOP_4_HIGH_ALARM_SETPOINT': 105,  # r/w,
        'LOOP_5_HIGH_ALARM_SETPOINT': 117,  # r/w,
        'LOOP_1_LOW_ALARM_SETPOINT': 70,  # r/w,
        'LOOP_2_LOW_ALARM_SETPOINT': 82,  # r/w,
        'LOOP_3_LOW_ALARM_SETPOINT': 94,  # r/w,
        'LOOP_4_LOW_ALARM_SETPOINT': 106,  # r/w,
        'LOOP_5_LOW_ALARM_SETPOINT': 118,  # r/w,
        'LOOP_1_ALARM_HYSTERESIS': 71,  # r/w,
        'LOOP_2_ALARM_HYSTERESIS': 83,  # r/w,
        'LOOP_3_ALARM_HYSTERESIS': 95,  # r/w,
        'LOOP_4_ALARM_HYSTERESIS': 107,  # r/w,
        'LOOP_5_ALARM_HYSTERESIS': 119,  # r/w,
        'MONITOR_INPUT_1_PROCESS_VALUE': 120,  # r,w,
        'MONITOR_INPUT_2_PROCESS_VALUE': 127,  # r,w,
        'MONITOR_INPUT_3_PROCESS_VALUE': 134,  # r,w,
        'MONITOR_INPUT_4_PROCESS_VALUE': 141,  # r,w,
        'MONITOR_INPUT_5_PROCESS_VALUE': 148,  # r,w,
        'MONITOR_INPUT_6_PROCESS_VALUE': 155,  # r,w,
        'MONITOR_INPUT_7_PROCESS_VALUE': 162,  # r,w,
        'MONITOR_INPUT_8_PROCESS_VALUE': 169,  # r,w,
        'MONITOR_INPUT_1_ALARM_TYPE': 121,  # r/w
        'MONITOR_INPUT_2_ALARM_TYPE': 128,  # r/w
        'MONITOR_INPUT_3_ALARM_TYPE': 135,  # r/w
        'MONITOR_INPUT_4_ALARM_TYPE': 142,  # r/w
        'MONITOR_INPUT_5_ALARM_TYPE': 149,  # r/w
        'MONITOR_INPUT_6_ALARM_TYPE': 156,  # r/w
        'MONITOR_INPUT_7_ALARM_TYPE': 163,  # r/w
        'MONITOR_INPUT_8_ALARM_TYPE': 170,  # r/w
        'MONITOR_INPUT_1_ALARM_MODE': 122,  # r/w
        'MONITOR_INPUT_2_ALARM_MODE': 129,  # r/w
        'MONITOR_INPUT_3_ALARM_MODE': 136,  # r/w
        'MONITOR_INPUT_4_ALARM_MODE': 143,  # r/w
        'MONITOR_INPUT_5_ALARM_MODE': 150,  # r/w
        'MONITOR_INPUT_6_ALARM_MODE': 157,  # r/w
        'MONITOR_INPUT_7_ALARM_MODE': 164,  # r/w
        'MONITOR_INPUT_8_ALARM_MODE': 171,  # r/w
        'MONITOR_INPUT_1_ALARM_OUTPUT_ASSIGNMENT': 123,  # r/w
        'MONITOR_INPUT_2_ALARM_OUTPUT_ASSIGNMENT': 130,  # r/w
        'MONITOR_INPUT_3_ALARM_OUTPUT_ASSIGNMENT': 137,  # r/w
        'MONITOR_INPUT_4_ALARM_OUTPUT_ASSIGNMENT': 144,  # r/w
        'MONITOR_INPUT_5_ALARM_OUTPUT_ASSIGNMENT': 151,  # r/w
        'MONITOR_INPUT_6_ALARM_OUTPUT_ASSIGNMENT': 158,  # r/w
        'MONITOR_INPUT_7_ALARM_OUTPUT_ASSIGNMENT': 165,  # r/w
        'MONITOR_INPUT_8_ALARM_OUTPUT_ASSIGNMENT': 172,  # r/w
        'MONITOR_INPUT_1_HIGH_ALARM_SETPOINT': 124,  # r/w,
        'MONITOR_INPUT_2_HIGH_ALARM_SETPOINT': 131,  # r/w,
        'MONITOR_INPUT_3_HIGH_ALARM_SETPOINT': 138,  # r/w,
        'MONITOR_INPUT_4_HIGH_ALARM_SETPOINT': 145,  # r/w,
        'MONITOR_INPUT_5_HIGH_ALARM_SETPOINT': 152,  # r/w,
        'MONITOR_INPUT_6_HIGH_ALARM_SETPOINT': 159,  # r/w,
        'MONITOR_INPUT_7_HIGH_ALARM_SETPOINT': 166,  # r/w,
        'MONITOR_INPUT_8_HIGH_ALARM_SETPOINT': 173,  # r/w,
        'MONITOR_INPUT_1_LOW_ALARM_SETPOINT': 125,  # r/w,
        'MONITOR_INPUT_2_LOW_ALARM_SETPOINT': 132,  # r/w,
        'MONITOR_INPUT_3_LOW_ALARM_SETPOINT': 139,  # r/w,
        'MONITOR_INPUT_4_LOW_ALARM_SETPOINT': 146,  # r/w,
        'MONITOR_INPUT_5_LOW_ALARM_SETPOINT': 153,  # r/w,
        'MONITOR_INPUT_6_LOW_ALARM_SETPOINT': 160,  # r/w,
        'MONITOR_INPUT_7_LOW_ALARM_SETPOINT': 167,  # r/w,
        'MONITOR_INPUT_8_LOW_ALARM_SETPOINT': 174,  # r/w,
        'MONITOR_INPUT_1_ALARM_HYSTERESIS': 126,  # r/w,
        'MONITOR_INPUT_2_ALARM_HYSTERESIS': 133,  # r/w,
        'MONITOR_INPUT_3_ALARM_HYSTERESIS': 140,  # r/w,
        'MONITOR_INPUT_4_ALARM_HYSTERESIS': 147,  # r/w,
        'MONITOR_INPUT_5_ALARM_HYSTERESIS': 154,  # r/w,
        'MONITOR_INPUT_6_ALARM_HYSTERESIS': 161,  # r/w,
        'MONITOR_INPUT_7_ALARM_HYSTERESIS': 168,  # r/w,
        'MONITOR_INPUT_8_ALARM_HYSTERESIS': 175,  # r/w,
        'PROFILE_STEP_TIME_ADJUSTMENT': 179,  # w,
        'EZT570I_OFFLINE_DOWNLOAD_PROFILE': 180  # r,
    }

    def encode_set_value(self, name, value):
        """
        For setting values, translate human readable to EZT570i protocol.
        :param name: Register name
        :param value: Human understandable value
        :return: 1) EZT570i register, 2) value to write
        """
        reg = self.name_to_reg(name)
        code = None
        if reg is not None:
            if name == 'CHAMBER_LIGHT_CONTROL':
                if value == 'off':
                    code = 0
                elif value == 'on':
                    code = 1
        return reg, code

    def decode_read_value(self, reg, value):
        """Run method that matches the register name"""
        name = self.reg_value_to_name(reg)

        if not name:
            return "UNDEFINED", "NO MATCH"

        operation = getattr(self, name.lower())
        if not callable(operation):
            return name, "NO MATCH"

        return operation(name, value)

    def bitfield(self, raw):
        """Convert int to array of bits"""
        bits_fields = BitFields(raw)
        response = [
            bits_fields.bit1,
            bits_fields.bit2,
            bits_fields.bit3,
            bits_fields.bit4,
            bits_fields.bit5,
            bits_fields.bit6,
            bits_fields.bit7,
            bits_fields.bit8,
            bits_fields.bit9,
            bits_fields.bit10,
            bits_fields.bit11,
            bits_fields.bit12,
            bits_fields.bit13,
            bits_fields.bit14,
            bits_fields.bit15,
            bits_fields.bit16
        ]
        return response

    def reg_value_to_name(self, search_reg):
        for name, reg in self.ctrl.iteritems():
            if reg == search_reg:
                return name

    def name_to_reg(self, search_name):
        return self.ctrl.get(search_name)

    def get_loop_autotune_status(self, name, value):
        mode = {
            0: 'Autotune Off',
            1: 'Start Autotune',
            2: 'Autotune In Progress',
            4: 'Cancel Autotune'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def get_loop_alarm_type(self, name, value):
        mode = {
            0: 'Alarm Off',
            3: 'Porcess High',
            5: 'Process Low',
            7: 'Process Both',
            24: 'Deviation High',
            40: 'Deviation Low',
            56: 'Deviation Both'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def get_monitor_input_alarm_type(self, name, value):
        mode = {
            0: 'Alarm Off',
            3: 'Process High',
            5: 'Process Low',
            7: 'Process Both'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def get_signed_int_tens_decimal(self, name, value):
        """
         -32768 – 32767 (-3276.8 – 3276.7)
         """
        response = value / 10
        return name, "degrees:{:.1f}".format(float(response))

    def get_event_control(self, name, value):
        bit_array = self.bitfield(value)
        response = {
            'Event 1': a_state[bit_array[0]],
            'Event2': a_state[bit_array[1]],
            'Event 3': a_state[bit_array[2]],
            'Event 4': a_state[bit_array[3]],
            'Event 5': a_state[bit_array[4]],
            'Event 6': a_state[bit_array[5]],
            'Event 7': a_state[bit_array[6]],
            'Event 8': a_state[bit_array[7]],
            'Event 9': a_state[bit_array[8]],
            'Event 10': a_state[bit_array[9]],
            'Event 11': a_state[bit_array[10]],
            'Event 12': a_state[bit_array[11]],
            'Event 13': a_state[bit_array[12]],
            'Event 14': a_state[bit_array[13]],
            'Event 15': a_state[bit_array[14]]
        }
        return name, "status:{}".format(response)

    def get_loop_alarm_output_assignment(self, name, value):
        mode = {
            0: 'No Output Selected',
            1: 'Digital Output (Customer Event) 1 Selected',
            2: 'Digital Output (Customer Event) 2 Selected',
            4: 'Digital Output (Customer Event) 3 Selected',
            8: 'Digital Output (Customer Event) 4 Selected',
            16: 'Digital Output (Customer Event) 5 Selected',
            32: 'Digital Output (Customer Event) 6 Selected',
            64: 'Digital Output (Customer Event) 7 Selected',
            128: 'Digital Output (Customer Event) 8 Selected',
            256: 'Digital Output (Customer Event) 9 Selected',
            512: 'Digital Output (Customer Event) 10 Selected',
            1024: 'Digital Output (Customer Event) 11 Selected',
            2048: 'Digital Output (Customer Event) 12 Selected',
            4096: 'Digital Output (Customer Event) 13 Selected',
            8192: 'Digital Output (Customer Event) 14 Selected',
            16384: 'Digital Output (Customer Event) 15 Selected'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def get_loop_alarm_mode(self, name, value):
        bit_array = self.bitfield(value)
        bit0 = {
            0: 'Alarm Self Clears',
            1: 'Alarm Latches'
        }
        bit1 = {
            0: 'Close on Alarm',
            1: 'Open on Alarm'
        }
        bit4 = {
            0: 'Audible Alarm Off',
            1: 'Audible Alarm On'
        }
        bit5 = {
            0: 'Chamber Continues On Alarm',
            1: 'Chamber Shuts Down On Alarm'
        }
        response = {
            'Step': bit0[bit_array[0]],
            'Door': bit1[bit_array[1]],
            'Audible': bit4[bit_array[4]],
            'Profile': bit5[bit_array[5]]
        }
        return name, ("status:{}").format(response)

    def get_loop_percent_output(self, name, value):
        """
        -10000 – 10000 (-100.00 – 100.00)
        """
        response = value / 100
        return name, "%out:{}".format(response)

    def get_minutes(self, name, value):
        """
            0 - 32767 minutes
        """
        return name, "minutes:{}".format(value)

    #-------------------------------
    # Start register methods
    #-------------------------------
    def operational_mode(self, name, value):
        mode = {
            0: 'Off',
            1: 'On'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def clock_yy_mm(self, name, value):
        """
        high byte: Year: 0 to 99
        low byte: Month: 1=Jan, ... 12=Dec
        """
        b_year, b_month = int_to_two_bytes(value & 0xFFFF)
        year = struct.unpack('B', b_year)[0]
        month = struct.unpack('B', b_month)[0]
        return name, "year: 20{}, month:{}".format(year, month)

    def clock_day_dow(self, name, value):
        """
        high byte: Day of Month: 1 to 31
        low byte: Day  of Week: 0=Sun, ... 6=Sat
        """
        b_dom, b_dow = int_to_two_bytes(value & 0xFFFF)
        dom = struct.unpack('B', b_dom)[0]
        dow = struct.unpack('B', b_dow)[0]
        return name, "DayOfMonth:{}, DayOfWeek:{}".format(dom, dow)

    def clock_hh_mm(self, name, value):
        """
        high byte: Hours: 1 to 23
        low byte: Minutes: 0 to 59
        """
        b_hour, b_minutes = int_to_two_bytes(value & 0xFFFF)
        hour = struct.unpack('B', b_hour)[0]
        minutes = struct.unpack('B', b_minutes)[0]
        return name, "Hour:{}, Minute:{}".format(hour, minutes)

    def clock_sec(self, name, value):
        """
        2 bytes: seconds: 0 to 59
        """
        return name, "Seconds:{}".format(value)

    def power_recovery_mode(self, name, value):
        mode = {
            0: 'Continue',
            1: 'Hold',
            2: 'Terminate',
            4: 'Reset',
            8: 'Resume'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def power_out_time(self, name, value):
        """
        0 - 32767 seconds
        """
        return name, "Seconds:{}".format(value)

    def defrost_operating_mode(self, name, value):
        mode = {
            0: 'Disabled',
            1: 'Manual Mode Selected',
            3: 'Auto Mode Selected'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def auto_defrost_temperature_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def auto_defrost_time_interval(self, name, value):
        return self.get_minutes(name, value)

    def defrost_status(self, name, value):
        mode = {
            0: 'Not in Defrost',
            1: 'In Defrost',
            3: 'In Prechill'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def time_remaining_until_next_defrost(self, name, value):
        return self.get_minutes(name, value)

    def product_control(self, name, value):
        mode = {
            0: 'Off',
            1: 'Deviation',
            2: 'Process',
            4: 'Off',
            5: 'Deviation using Event for enable',
            6: 'Process using Event for enable'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def product_control_upper_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def product_control_lower_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def condensation_control(self, name, value):
        mode = {
            0: "Off",
            1: "On"
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def condensation_control_monitor_mode(self, name, value):
        mode = {
            1: "Use Single Input",
            2: "Use Lowest Input",
            4: "Use Highest Input",
            8: "Use Average of all Inputs"
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def condensation_control_input_selection(self, name, value):
        bit_array = self.bitfield(value)
        response = {
            'Product': 0,
            'PV1': bit_array[0],
            'PV2': bit_array[1],
            'PV3': bit_array[2],
            'PV4': bit_array[3],
            'PV5': bit_array[4],
            'PV6': bit_array[5],
            'PV7': bit_array[6],
            'PV8': bit_array[7],
        }
        return name, "pv:{}".format(response)

    def condensation_control_temperatore_ramp_rate_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def condensation_control_deupoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def condensation_control_duepoint_actual(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def chamber_light_control(self, name, value):
        mode = {
            0: "Off",
            1: "On"
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def chamber_manual_event_control(self, name, value):
        return self.get_event_control(name, value)

    def customer_manual_event_control(self, name, value):
        return self.get_event_control(name, value)

    def profile_control_status(self, name, value):
        mode = {
            0: 'Stop/Off',
            1: 'Stop/All Off',
            2: 'Hold',
            4: 'Run/Resume',
            8: 'Autostart',
            16: 'Wait',
            32: 'Ramp',
            64: 'Soak',
            128: 'Guaranteed Soak'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def profile_advanced_step(self, name, value):
        mode = {
            1: 'Advance Previous Step',
            2: 'Advance Next Step'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Mode:{}".format(s)

    def profile_name_ch_1_2(self, name, value):
        """
        32 – 126 (high byte)
        32 – 126 (low byte)
        """
        b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
        hch = struct.unpack('B', b_hch)[0]
        lch = struct.unpack('B', b_lch)[0]
        return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))

    def profile_name_ch_3_4(self, name, value):
        """
        32 – 126 (high byte)
        32 – 126 (low byte)
        """
        b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
        hch = struct.unpack('B', b_hch)[0]
        lch = struct.unpack('B', b_lch)[0]
        return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))

    def profile_name_ch_5_6(self, name, value):
        """
        32 – 126 (high byte)
        32 – 126 (low byte)
        """
        b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
        hch = struct.unpack('B', b_hch)[0]
        lch = struct.unpack('B', b_lch)[0]
        return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))

    def profile_name_ch_7_8(self, name, value):
        """
        32 – 126 (high byte)
        32 – 126 (low byte)
        """
        b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
        hch = struct.unpack('B', b_hch)[0]
        lch = struct.unpack('B', b_lch)[0]
        return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))

    def profile_name_ch_9_10(self, name, value):
        """
        32 – 126 (high byte)
        32 – 126 (low byte)
        """
        b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
        hch = struct.unpack('B', b_hch)[0]
        lch = struct.unpack('B', b_lch)[0]
        return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))

    def profile_start_date_yy_mm(self, name, value):
        """
        high byte: Year: 0 to 99
        low byte: Month: 1=Jan, ... 12=Dec
        """
        b_year, b_month = int_to_two_bytes(value & 0xFFFF)
        year = struct.unpack('B', b_year)[0]
        month = struct.unpack('B', b_month)[0]
        return name, "year: 20{}, month:{}".format(year, month)

    def profile_stop_date_yy_mm(self, name, value):
        """
        high byte: Year: 0 to 99
        low byte: Month: 1=Jan, ... 12=Dec
        """
        b_year, b_month = int_to_two_bytes(value & 0xFFFF)
        year = struct.unpack('B', b_year)[0]
        month = struct.unpack('B', b_month)[0]
        return name, "year: 20{}, month:{}".format(year, month)

    def profile_start_date_day_dow(self, name, value):
        """
        high byte: Day of Month: 1 to 31
        low byte: Day  of Week: 0=Sun, ... 6=Sat
        """
        b_dom, b_dow = int_to_two_bytes(value & 0xFFFF)
        dom = struct.unpack('B', b_dom)[0]
        dow = struct.unpack('B', b_dow)[0]
        return name, "DayOfMonth:{}, DayOfWeek:{}".format(dom, dow)

    def profile_stop_date_day_dow(self, name, value):
        """
        high byte: Day of Month: 1 to 31
        low byte: Day  of Week: 0=Sun, ... 6=Sat
        """
        b_dom, b_dow = int_to_two_bytes(value & 0xFFFF)
        dom = struct.unpack('B', b_dom)[0]
        dow = struct.unpack('B', b_dow)[0]
        return name, "DayOfMonth:{}, DayOfWeek:{}".format(dom, dow)

    def profile_start_date_hh_mm(self, name, value):
        """
        high byte: Hours: 1 to 23
        low byte: Minutes: 0 to 59
        """
        b_hour, b_minutes = int_to_two_bytes(value & 0xFFFF)
        hour = struct.unpack('B', b_hour)[0]
        minutes = struct.unpack('B', b_minutes)[0]
        return name, "Hour:{}, Minute:{}".format(hour, minutes)

    def profile_stop_date_hh_mm(self, name, value):
        """
        high byte: Hours: 1 to 23
        low byte: Minutes: 0 to 59
        """
        b_hour, b_minutes = int_to_two_bytes(value & 0xFFFF)
        hour = struct.unpack('B', b_hour)[0]
        minutes = struct.unpack('B', b_minutes)[0]
        return name, "Hour:{}, Minute:{}".format(hour, minutes)

    def profile_start_step(self, name, value):
        """0 - 99"""
        return name, "step:{}".format(value)

    def profile_current_step(self, name, value):
        """0 - 99"""
        return name, "step:{}".format(value)

    def profile_last_step(self, name, value):
        """0 - 99"""
        return name, "step:{}".format(value)

    def profile_time_left_in_current_step_hhh(self, name, value):
        """1 – 999 Hours"""
        return name, "hours:{}".format(value)

    def profile_time_left_in_current_step_mm_ss(self, name, value):
        """
         high byte: Minutes: 0 to 59
         low byte: Seconds: 0 to 59
         """
        b_minutes, b_seconds = int_to_two_bytes(value & 0xFFFF)
        minutes = struct.unpack('B', b_minutes)[0]
        seconds = struct.unpack('B', b_seconds)[0]
        return name, "Minute:{}, Seconds:{}".format(minutes, seconds)

    def profile_wait_for_status(self, name, value):
        mode = {
            0:    'Not Waiting',
            1:    'Input 1',
            2:    'Input 2',
            4:    'Input 3',
            8:    'Input 4',
            16:   'Input 5',
            32:   'Input 6',
            64:   'Input 7',
            128:  'Input 8',
            256:  'Input 9',
            512:  'Input 10',
            1024: 'Input 11',
            2048: 'Input 12',
            4096: 'Input 13',
            8192: 'Digital Input'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def profile_wait_for_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def profile_current_jump_step(self, name, value):
        """0 - 99"""
        return name, "step:{}".format(value)

    def profile_jumps_remaining_in_current_step(self, name, value):
        """0 - 99"""
        return name, "jumps:{}".format(value)

    def profile_loop_1_target_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def profile_loop_2_target_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def profile_loop_3_target_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def profile_loop_4_target_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def profile_loop_5_target_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def profile_last_jump_from_step(self, name, value):
        """0 - 99"""
        return name, "step:{}".format(value)

    def profile_last_jump_to_step(self, name, value):
        """0 - 99"""
        return name, "step:{}".format(value)

    def profile_total_jumps_made(self, name, value):
        """0 – 32767"""
        return name, "jumps:{}".format(value)

    def alarm_acknowledge(self, name, value):
        mode = {
            1: 'Alarm Silence',
            2: 'Pumpdown Reset'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

    def ezt570i_alarm_status(self, name, value):
        bit_array = self.bitfield(value)
        response = {
            'Input1 Sensor Break': a_state[bit_array[0]],
            'Input2 Sensor Break': a_state[bit_array[1]],
            'Input3 Sensor Break': a_state[bit_array[2]],
            'Input4 Sensor Break': a_state[bit_array[3]],
            'Input5 Sensor Break': a_state[bit_array[4]],
            'Input6 Sensor Break': a_state[bit_array[5]],
            'Input7 Sensor Break': a_state[bit_array[6]],
            'Input8 Sensor Break': a_state[bit_array[7]],
            'Input9 Sensor Break': a_state[bit_array[8]],
            'Input10 Sensor Break': a_state[bit_array[9]],
            'Input11 Sensor Break': a_state[bit_array[10]],
            'Input12 Sensor Break': a_state[bit_array[11]],
            'Input13 Sensor Break': a_state[bit_array[12]],
            '(not assigned)': a_state[bit_array[13]],
            'Loop Communications Failure': a_state[bit_array[14]],
        }
        return name, "status:{}".format(response)

    def input_alarm_status(self, name, value):
        bit_array = self.bitfield(value)
        response = {
            'Input1 Alarm':   a_state[bit_array[0]],
            'Input2 Alarm':   a_state[bit_array[1]],
            'Input3 Alarm':   a_state[bit_array[2]],
            'Input4 Alarm':   a_state[bit_array[3]],
            'Input5 Alarm':   a_state[bit_array[4]],
            'Input6 Alarm':   a_state[bit_array[5]],
            'Input7 Alarm':   a_state[bit_array[6]],
            'Input8 Alarm':   a_state[bit_array[7]],
            'Input9 Alarm':   a_state[bit_array[8]],
            'Input10 Alarm':  a_state[bit_array[9]],
            'Input11 Alarm':  a_state[bit_array[10]],
            'Input12 Alarm':  a_state[bit_array[11]],
            'Input13 Alarm':  a_state[bit_array[12]],
            '(not assigned 1)': a_state[bit_array[13]],
            '(not assigned 2)': a_state[bit_array[14]]
        }
        return name, "status:{}".format(response)

    def chamber_alarm_status(self, name, value):
        bit_array = self.bitfield(value)
        response = {
            'Heater High Limit (Plenum A)': a_state[bit_array[0]],
            'External Product Safety': a_state[bit_array[1]],
            'Boiler Over-Temp (Plenum A)': a_state[bit_array[2]],
            'Boiler Low Water (Plenum A)': a_state[bit_array[3]],
            'Dehumidifier System Fault (System B Boiler Over-Temp)': a_state[bit_array[4]],
            'Motor Overload (Plenum A)': a_state[bit_array[5]],
            'Fluid System High Limit (Plenum B Heater High Limit)': a_state[bit_array[6]],
            'Fluid System High Pressure (Plenum B Motor Overload)': a_state[bit_array[7]],
            'Fluid System Low Flow': a_state[bit_array[8]],
            'Door Open': a_state[bit_array[9]],
            '(System B Boiler Low Water)': a_state[bit_array[10]],
            '(not assigned)': a_state[bit_array[11]],
            'Emergency Stop': a_state[bit_array[12]],
            'Power Failure': a_state[bit_array[13]],
            'Transfer Error': a_state[bit_array[14]],
        }
        return name, "status:{}".format(response)

    def refrigeration_alarm_status(self, name, value):
        bit_array = self.bitfield(value)
        response = {
            'System 1(A) High/Low Pressure': a_state[bit_array[0]],
            'System 1(A) Low Oil Pressure': a_state[bit_array[1]],
            'System 1(A) High Discharge Temperature': a_state[bit_array[2]],
            'System 1(A) Compressor Protection Module': a_state[bit_array[3]],
            'Pumpdown Disabled': a_state[bit_array[4]],
            'System 1(A) Floodback Monitor': a_state[bit_array[5]],
            '(not assigned) 1': a_state[bit_array[6]],
            '(not assigned) 2': a_state[bit_array[7]],
            'System 2(B) High/Low Pressure': a_state[bit_array[8]],
            'System 2(B) Low Oil Pressure': a_state[bit_array[9]],
            'System 2(B) High Discharge Temperature': a_state[bit_array[10]],
            'System 2(B) Compressor Protection Module': a_state[bit_array[11]],
            '(not assigned) 3': a_state[bit_array[12]],
            'System B Floodback Monitor': a_state[bit_array[13]],
            '(not assigned) 4': a_state[bit_array[14]],
        }
        return name, "status:{}".format(response)

    def system_status_monitor(self, name, value):
        bit_array = self.bitfield(value)
        response = {
            'Humidity Water Reservoir Low': a_state[bit_array[0]],
            'Humidity Disabled (temperature out-of-range)': a_state[bit_array[1]],
            'Humidity High Dewpoint Limit': a_state[bit_array[2]],
            'Humidity Low Dewpoint Limit': a_state[bit_array[3]],
            'Door Open': a_state[bit_array[4]],
            '(not assigned) 1': a_state[bit_array[5]],
            '(not assigned) 2': a_state[bit_array[6]],
            '(not assigned) 3': a_state[bit_array[7]],
            'Service Air Circulators': a_state[bit_array[8]],
            'Service Heating/Cooling System': a_state[bit_array[9]],
            'Service Humidity System': a_state[bit_array[10]],
            'Service Purge System': a_state[bit_array[11]],
            'Service Altitude System': a_state[bit_array[12]],
            'Service Transfer Mechanism': a_state[bit_array[13]],
            '(not assigned) 4': a_state[bit_array[14]],
        }
        return name, "status:{}".format(response)

    def loop_1_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_2_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_3_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_4_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_5_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_1_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_2_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_3_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_4_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_5_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_1_percent_output(self, name, value):
        return self.get_loop_percent_output(name, value)

    def loop_2_percent_output(self, name, value):
        return self.get_loop_percent_output(name, value)

    def loop_3_percent_output(self, name, value):
        return self.get_loop_percent_output(name, value)

    def loop_4_percent_output(self, name, value):
        return self.get_loop_percent_output(name, value)

    def loop_5_percent_output(self, name, value):
        return self.get_loop_percent_output(name, value)

    def loop_1_autotune_status(self, name, value):
        return self.get_loop_autotune_status(name, value)

    def loop_2_autotune_status(self, name, value):
        return self.get_loop_autotune_status(name, value)

    def loop_3_autotune_status(self, name, value):
        return self.get_loop_autotune_status(name, value)

    def loop_4_autotune_status(self, name, value):
        return self.get_loop_autotune_status(name, value)

    def loop_5_autotune_status(self, name, value):
        return self.get_loop_autotune_status(name, value)

    def loop_1_upper_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_2_upper_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_3_upper_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_4_upper_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_5_upper_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_1_lower_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_2_lower_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_3_lower_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_4_lower_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_5_lower_setpoint_limit(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_1_alarm_type(self, name, value):
        return self.get_loop_alarm_type(name, value)

    def loop_2_alarm_type(self, name, value):
        return self.get_loop_alarm_type(name, value)

    def loop_3_alarm_type(self, name, value):
        return self.get_loop_alarm_type(name, value)

    def loop_4_alarm_type(self, name, value):
        return self.get_loop_alarm_type(name, value)

    def loop_5_alarm_type(self, name, value):
        return self.get_loop_alarm_type(name, value)

    def loop_1_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def loop_2_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def loop_3_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def loop_4_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def loop_5_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def loop_1_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def loop_2_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def loop_3_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def loop_4_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def loop_5_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def loop_1_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_2_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_3_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_4_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_5_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_1_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_2_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_3_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_4_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_5_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_1_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_2_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_3_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_4_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def loop_5_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_1_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_2_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_3_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_4_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_5_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_6_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_7_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_8_process_value(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_1_alarm_type(self, name, value):
        return self.get_monitor_input_alarm_type(name, value)

    def monitor_input_2_alarm_type(self, name, value):
        return self.get_monitor_input_alarm_type(name, value)

    def monitor_input_3_alarm_type(self, name, value):
        return self.get_monitor_input_alarm_type(name, value)

    def monitor_input_4_alarm_type(self, name, value):
        return self.get_monitor_input_alarm_type(name, value)

    def monitor_input_5_alarm_type(self, name, value):
        return self.get_monitor_input_alarm_type(name, value)

    def monitor_input_6_alarm_type(self, name, value):
        return self.get_monitor_input_alarm_type(name, value)

    def monitor_input_7_alarm_type(self, name, value):
        return self.get_monitor_input_alarm_type(name, value)

    def monitor_input_8_alarm_type(self, name, value):
        return self.get_monitor_input_alarm_type(name, value)

    def monitor_input_1_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def monitor_input_2_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def monitor_input_3_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def monitor_input_4_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def monitor_input_5_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def monitor_input_6_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def monitor_input_7_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def monitor_input_8_alarm_mode(self, name, value):
        return self.get_loop_alarm_mode(name, value)

    def monitor_input_1_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def monitor_input_2_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def monitor_input_3_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def monitor_input_4_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def monitor_input_5_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def monitor_input_6_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def monitor_input_7_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def monitor_input_8_alarm_output_assignment(self, name, value):
        return self.get_loop_alarm_output_assignment(name, value)

    def monitor_input_1_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_2_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_3_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_4_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_5_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_6_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_7_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_8_high_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_1_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_2_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_3_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_4_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_5_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_6_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_7_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_8_low_alarm_setpoint(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_1_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_2_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_3_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_4_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_5_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_6_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_7_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def monitor_input_8_alarm_hysteresis(self, name, value):
        return self.get_signed_int_tens_decimal(name, value)

    def profile_step_time_adjustment(self,name, value):
        """
        0 – 32767 minutes
        """
        return name, "minute:{}".format(value)

    def ezt570i_offline_download_profile(self,name, value):
        mode = {
            0: 'Online',
            1: 'Offline/Downloading Profile'
        }
        s = mode.get(value, "{} Not specified in API".format(value))
        return name, "Status:{}".format(s)

class ChamberProfileRegisters(object):
    """Write Registers used in,
    Write Register Commnad (0x10) for profile upload only.
    """
    def __init__(self):
        pass

    # Dictionary map bytes to function
    ctrl = {
        'AUTOSTART': 200,  # w,
        'AUTOSTART_TIME_YY_MM': 201,  # w,
        'AUTOSTART_TIME_DAY_DOW': 202,  # w,
        'AUTOSTART_TIME_HH_MM': 203,  # w,
        'PROFILE_NAME_CH_1_2': 204,  # w,
        'PROFILE_NAME_CH_3_4': 205,  # w,
        'PROFILE_NAME_CH_5_6': 206,  # w,
        'PROFILE_NAME_CH_7_8': 207,  # w,
        'PROFILE_NAME_CH_9_10': 208,  # w,
        'TOTAL_NUMBER_OF_STEPS_IN_PROFILE': 209,  # w,
        'GUARANTEED_SOAK_BAND_LOOP_1': 210,  # w,
        'GUARANTEED_SOAK_BAND_LOOP_2': 211,  # w,
        'GUARANTEED_SOAK_BAND_LOOP_3': 212,  # w,
        'GUARANTEED_SOAK_BAND_LOOP_4': 213,  # w,
        'GUARANTEED_SOAK_BAND_LOOP_5': 214,  # w,
    }

    @staticmethod
    def get_step_regs(step):
        """Send back an ever incrementing Step, stop after 99.
        Each step consists of 15 registers.
        Step 1 has registers 215 to 229
        Step 2 has registers 230 to 244
        Step 3 has registers 245 to 259
        ...
        Step 99 has registers 1685 to 1699
        """
        assert 1 <= step <= 99
        offset = 15 * (step - 1)
        return     {
            'PROFILE_STEP_TIME_HOURS': 215 + offset,  # w,
            'PROFILE_STEP_TIME_MM_SS': 216 + offset,  # w,
            'PROFILE_STEP_CHAMBER_EVENTS': 217 + offset,  # w,
            'PROFILE_STEP_CUSTOMER_EVENTS': 218 + offset,  # w,
            'PROFILE_STEP_GUARANTEED': 219 + offset,  # w,
            'PROFILE_STEP_WAIT_FOR_LOOP_EVENTS': 220 + offset,  # w,
            'PROFILE_STEP_WAIT_FOR_MONITOR_EVENTS': 221 + offset,  # w,
            'PROFILE_STEP_WAIT_FOR_SETPOINT': 222 + offset,  # w,
            'PROFILE_STEP_JUMP_STEP_NUMBER': 223 + offset,  # w,
            'PROFILE_STEP_JUMP_COUNT': 224 + offset,  # w,
            'PROFILE_STEP_TARGET_SETPOINT_FOR_LOOP_1': 225 + offset,  # w,
            'PROFILE_STEP_TARGET_SETPOINT_FOR_LOOP_2': 226 + offset,  # w,
            'PROFILE_STEP_TARGET_SETPOINT_FOR_LOOP_3': 227 + offset,  # w,
            'PROFILE_STEP_TARGET_SETPOINT_FOR_LOOP_4': 228 + offset,  # w,
            'PROFILE_STEP_TARGET_SETPOINT_FOR_LOOP_5': 229 + offset,  # w,
        }
