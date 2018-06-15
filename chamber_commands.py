#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EZT570i Command Register Reference"""
import struct


class ChamberCommandRegisters(object):
    """Read and Write Registers
    Used in Read Registers Command (0x03) for multi register read.
    Used in Write Register Commnad (0x06) for single register write.
    """

    def __init__(self):
        pass

    # Dictionary map bytes to function
    ctrl = {
        'OPERATIONAL_MODE': 0,  # r,
        'CLOCK_YY_MM': 1,  # r, Clock (Year, Month)
        'CLOCK_DAY_DOW': 2,  # r, Clock (Day, DOE)
        'CLOCK_HH_MM': 3,  # r, Clock (Hours, Min)
        'CLOCK_SEC': 4,  # r, Clock (Seconds)
        'POWER_RECOVERY_MODE': 5,  # r/w, Power Recovery Mode
        'POWER_OUT_TIME': 6,  # r/w,
        'DEFROST_OPERATING_MODE': 7,  # r/w,
        'AUTO_DEFROST_TEMPERATUR_SETPOINT': 8,  # r/w,
        'AUTO_DEFROST_TIME_INTERVAL': 9,  # r/w,
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
        'EZT-570I_ALARM_STATUS': 55,  # w,
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
        'LOOP_1 LOW_ALARM_SETPOINT': 70,  # r/w,
        'LOOP_2 LOW_ALARM_SETPOINT': 82,  # r/w,
        'LOOP_3 LOW_ALARM_SETPOINT': 94,  # r/w,
        'LOOP_4 LOW_ALARM_SETPOINT': 106,  # r/w,
        'LOOP_5 LOW_ALARM_SETPOINT': 118,  # r/w,
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
    def reg_value_to_name(self, search_reg):
        response = None
        for name, reg in self.ctrl.iteritems():  # for name, age in list.items():  (for Python 3.x)
            if reg == search_reg:
                response = name
        return response

    def name_to_reg(self, search_name):
        response = None
        if search_name in self.ctrl:
            response = self.ctrl[search_name]
        return response

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
        name = self.reg_value_to_name(reg)
        response = None
        int_to_two_bytes = struct.Struct('!H').pack

        if name is not None:
            if name == 'OPERATIONAL_MODE':
                if value == 0:
                    response = 'off'
                elif value == 1:
                    response = 'on'

            elif name == 'CLOCK_YY_MM':
                """
                high byte: Year: 0 to 99
                low byte: Month: 1=Jan, ... 12=Dec
                """
                b_year, b_month = int_to_two_bytes(value & 0xFFFF)
                year = struct.unpack('B', b_year)[0]
                month = struct.unpack('B', b_month)[0]
                return name, "year: 20{}, month:{}".format(year, month)

            elif name == 'CLOCK_DAY_DOW':
                """
                high byte: Day of Month: 1 to 31
                low byte: Day  of Week: 0=Sun, ... 6=Sat
                """
                b_dom, b_dow = int_to_two_bytes(value & 0xFFFF)
                dom = struct.unpack('B', b_dom)[0]
                dow = struct.unpack('B', b_dow)[0]
                return name, "DayOfMonth:{}, DayOfWeek:{}".format(dom, dow)

            elif name == 'CLOCK_HH_MM':
                """
                high byte: Hours: 1 to 23
                low byte: Minutes: 0 to 59
                """
                b_hour, b_minutes = int_to_two_bytes(value & 0xFFFF)
                hour = struct.unpack('B', b_hour)[0]
                minutes = struct.unpack('B', b_minutes)[0]
                return name, "Hour:{}, Minute:{}".format(hour, minutes)

            elif name == 'CLOCK_SEC':
                """
                2 bytes: seconds: 0 to 59
                """
                _, b_seconds = int_to_two_bytes(value & 0xFFFF)
                seconds = struct.unpack('B', b_seconds)[0]
                return name, "Seconds:{}".format(seconds)

            elif name == 'CHAMBER_LIGHT_CONTROL':
                if value == 0:
                    response = 'off'
                elif value == 1:
                    response = 'on'

        return name, response

class ChamberProfileRegisters(object):
    """Write Registers used in,
    Write Register Commnad (0x10) for profile upload only.
    """
    def __init__(self):
        self.step = 0

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
    def setp(step):
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