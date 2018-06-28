#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EZT570i Command Register Reference
Translate between packed modbus and register <=> unpacked human readable names, and values
Not all registers have getters and setters.
"""

import sys
import struct
import ctypes

thismodule = sys.modules[__name__]

# Dictionary map registers to function
ctrl_registers = {
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
    'PROFILE_ADVANCE_STEP': 25,  # w,
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
    'EZT570I_ALARM_STATUS': 55,  # r,
    'INPUT_ALARM_STATUS': 56,  # r,
    'CHAMBER_ALARM_STATUS': 57,  # r,
    'REFRIGERATION_ALARM_STATUS': 58,  # r,
    'SYSTEM_STATUS_MONITOR': 59,  # r,
    'LOOP_1_SETPOINT': 60,  # r/w,
    'LOOP_2_SETPOINT': 72,  # r/w,
    'LOOP_3_SETPOINT': 84,  # r/w,
    'LOOP_4_SETPOINT': 96,  # r/w,
    'LOOP_5_SETPOINT': 108,  # r/w,
    'LOOP_1_PROCESS_VALUE': 61,  # r,
    'LOOP_2_PROCESS_VALUE': 73,  # r,
    'LOOP_3_PROCESS_VALUE': 85,  # r,
    'LOOP_4_PROCESS_VALUE': 97,  # r,
    'LOOP_5_PROCESS_VALUE': 109,  # r,
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
    'MONITOR_INPUT_1_PROCESS_VALUE': 120,  # r,
    'MONITOR_INPUT_2_PROCESS_VALUE': 127,  # r,
    'MONITOR_INPUT_3_PROCESS_VALUE': 134,  # r,
    'MONITOR_INPUT_4_PROCESS_VALUE': 141,  # r,
    'MONITOR_INPUT_5_PROCESS_VALUE': 148,  # r,
    'MONITOR_INPUT_6_PROCESS_VALUE': 155,  # r,
    'MONITOR_INPUT_7_PROCESS_VALUE': 162,  # r,
    'MONITOR_INPUT_8_PROCESS_VALUE': 169,  # r,
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


int_to_two_bytes = struct.Struct('!h').pack


state_alarm = {
    0: 'normal',
    1: 'Alarm'
}


state_on_off = {
    0: 'off',
    1: 'on'
}


state_power_recovery_mode = {
    0: 'continue',
    1: 'hold',
    2: 'terminate',
    4: 'reset',
    8: 'resume'
}


state_defrost_operating_mode = {
    0: 'disabled',
    1: 'manual mode selected',
    3: 'auto mode selected'
}


state_get_loop_autotune_status = {
    0: 'autotune off',
    1: 'start autotune',
    2: 'autotune in progress',
    4: 'cancel autotune'
}


state_get_loop_alarm_type = {
    0: 'Alarm Off',
    3: 'Porcess High',
    5: 'Process Low',
    7: 'Process Both',
    24: 'Deviation High',
    40: 'Deviation Low',
    56: 'Deviation Both'
}


state_get_loop_alarm_output_assignment = {
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


state_profile_wait_for_status = {
    0: 'Not Waiting',
    1: 'Input 1',
    2: 'Input 2',
    4: 'Input 3',
    8: 'Input 4',
    16: 'Input 5',
    32: 'Input 6',
    64: 'Input 7',
    128: 'Input 8',
    256: 'Input 9',
    512: 'Input 10',
    1024: 'Input 11',
    2048: 'Input 12',
    4096: 'Input 13',
    8192: 'Digital Input'
}


state_profile_control_status = {
    0: 'stop/off',
    1: 'stop/all off',
    2: 'hold',
    4: 'run/resume',
    8: 'autostart',
    16: 'wait',
    32: 'ramp',
    64: 'soak',
    128: 'guaranteed soak'
}


state_product_control = {
    0: 'off',
    1: 'deviation',
    2: 'process',
    4: 'off',
    5: 'deviation using event for enable',
    6: 'process using event for enable'
}


state_condensation_control_monitor_mode = {
    1: "Use Single Input",
    2: "Use Lowest Input",
    4: "Use Highest Input",
    8: "Use Average of all Inputs"
}


state_get_monitor_input_alarm_type = {
    0: 'Alarm Off',
    3: 'Process High',
    5: 'Process Low',
    7: 'Process Both'
}


def encode_set_value(name, value):
    """
    For setting values, translate human readable to EZT570i protocol.
    :param name: Register name
    :param value: Human understandable value
    :return: 1) EZT570i register, 2) value to write
    """
    reg = name_to_reg(name)
    if not reg:
        return None, None

    setter = "set_{}".format(name.lower())

    try:
        operation = getattr(thismodule, setter)
    except AttributeError:
        return name, "Non Writeable Register"

    if not callable(operation):
        return name, "NO MATCH"

    return reg, operation(value)


def decode_read_value(reg, value):
    """Run method that matches the register name"""
    name = reg_value_to_name(reg)

    if not name:
        return "UNDEFINED", "NO MATCH"

    try:
        operation = getattr(thismodule, name.lower())
    except AttributeError:
        return name, "Non Readable Register"

    if not callable(operation):
        return name, "NO MATCH"

    return operation(name, value)


def bitfield(raw):
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


def reg_value_to_name(search_reg):
    for name, reg in ctrl_registers.iteritems():
        if reg == search_reg:
            return name


def name_to_reg(search_name):
    return ctrl_registers.get(search_name)


def get_loop_autotune_status(name, value):

    s = state_get_loop_autotune_status.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_loop_autotune_status(value):

    value = value.lower()
    for mode_state, mode_name in state_get_loop_autotune_status.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def get_loop_alarm_type(name, value):

    s = state_get_loop_alarm_type.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_loop_alarm_type(value):
    value = value.lower()
    for mode_state, mode_name in state_get_loop_alarm_type.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def get_monitor_input_alarm_type(name, value):
    s = state_get_monitor_input_alarm_type.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_monitor_input_alarm_type(value):
    value = value.lower()
    for mode_state, mode_name in state_get_monitor_input_alarm_type.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def get_signed_int_tens_decimal(name, value):
    """
     -32768 – 32767 (-3276.8 – 3276.7)
     """
    response = value / 10
    return name, "degrees:{:.1f}".format(float(response))


def set_signed_int_tens_decimal(value):
    """
     -32768 – 32767 (-3276.8 – 3276.7)
     """
    response = value * 10
    assert 0 <= response < 2 ** 16
    return response


def get_event_control(name, value):
    bit_array = bitfield(value)
    response = {
        'Event 1': state_alarm[bit_array[0]],
        'Event2': state_alarm[bit_array[1]],
        'Event 3': state_alarm[bit_array[2]],
        'Event 4': state_alarm[bit_array[3]],
        'Event 5': state_alarm[bit_array[4]],
        'Event 6': state_alarm[bit_array[5]],
        'Event 7': state_alarm[bit_array[6]],
        'Event 8': state_alarm[bit_array[7]],
        'Event 9': state_alarm[bit_array[8]],
        'Event 10': state_alarm[bit_array[9]],
        'Event 11': state_alarm[bit_array[10]],
        'Event 12': state_alarm[bit_array[11]],
        'Event 13': state_alarm[bit_array[12]],
        'Event 14': state_alarm[bit_array[13]],
        'Event 15': state_alarm[bit_array[14]]
    }
    return name, "status:{}".format(response)


def get_loop_alarm_output_assignment(name, value):
    s = state_get_loop_alarm_output_assignment.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_loop_alarm_output_assignment(value):
    value = value.lower()
    for mode_state, mode_name in state_get_loop_alarm_output_assignment.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def get_loop_alarm_mode(name, value):
    bit_array = bitfield(value)
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
        'step': bit0[bit_array[0]],
        'door': bit1[bit_array[1]],
        'audible': bit4[bit_array[4]],
        'profile': bit5[bit_array[5]]
    }
    return name, "status:{}".format(response)


def set_loop_alarm_mode(value):
    # TODO: Figure out what to do here.
    # TODO: Takes in what we return above.
    # Packs into ctypes.struct and returns.
    assert 'step' in value \
        and 'door' in value \
        and 'audible' in value \
        and 'profile' in value

    return 0


def get_loop_percent_output(name, value):
    """
    -10000 – 10000 (-100.00 – 100.00)
    """
    response = value / 100
    return name, "%out:{}".format(response)


def set_loop_percent_output(value):
    """
    -10000 – 10000 (-100.00 – 100.00)
    """
    response = value * 100
    return response


def get_minutes(name, value):
    """
        0 - 32767 minutes
    """
    return name, "minutes:{}".format(value)


def set_minutes(value):
    assert 0 <= value <= 32767
    return value

# -------------------------------
# Start register methods
# -------------------------------


def operational_mode(name, value):
    s = state_on_off.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def clock_yy_mm(name, value):
    """
    high byte: Year: 0 to 99
    low byte: Month: 1=Jan, ... 12=Dec
    """
    b_year, b_month = int_to_two_bytes(value & 0xFFFF)
    year = struct.unpack('B', b_year)[0]
    month = struct.unpack('B', b_month)[0]
    return name, "year: 20{}, month:{}".format(year, month)


def clock_day_dow(name, value):
    """
    high byte: Day of Month: 1 to 31
    low byte: Day  of Week: 0=Sun, ... 6=Sat
    """
    b_dom, b_dow = int_to_two_bytes(value & 0xFFFF)
    dom = struct.unpack('B', b_dom)[0]
    dow = struct.unpack('B', b_dow)[0]
    return name, "DayOfMonth:{}, DayOfWeek:{}".format(dom, dow)


def clock_hh_mm(name, value):
    """
    high byte: Hours: 1 to 23
    low byte: Minutes: 0 to 59
    """
    b_hour, b_minutes = int_to_two_bytes(value & 0xFFFF)
    hour = struct.unpack('B', b_hour)[0]
    minutes = struct.unpack('B', b_minutes)[0]
    return name, "Hour:{}, Minute:{}".format(hour, minutes)


def clock_sec(name, value):
    """
    2 bytes: seconds: 0 to 59
    """
    return name, "Seconds:{}".format(value)


def power_recovery_mode(name, value):
    s = state_power_recovery_mode.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_power_recovery_mode(value):
    value = value.lower()
    for mode_state, mode_name in state_power_recovery_mode.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def power_out_time(name, value):
    """
    0 - 32767 seconds
    """
    return name, "Seconds:{}".format(value)


def set_power_out_time(value):
    """
    0 - 32767 seconds
    """
    assert 0 <= value <= 32767
    return value


def defrost_operating_mode(name, value):
    s = state_defrost_operating_mode.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_defrost_operating_mode(value):
    value = value.lower()
    for mode_state, mode_name in state_defrost_operating_mode.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def auto_defrost_temperature_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_auto_defrost_temperature_setpoint(value):
    return set_signed_int_tens_decimal(value)


def auto_defrost_time_interval(name, value):
    return get_minutes(name, value)


def set_auto_defrost_time_interval(value):
    return set_minutes(value)


def defrost_status(name, value):
    state = {
        0: 'Not in Defrost',
        1: 'In Defrost',
        3: 'In Prechill'
    }
    s = state.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def time_remaining_until_next_defrost(name, value):
    return get_minutes(name, value)


def product_control(name, value):
    s = state_product_control.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_product_control(value):
    value = value.lower()
    for mode_state, mode_name in state_product_control.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def product_control_upper_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_product_control_upper_setpoint(value):
    return set_signed_int_tens_decimal(value)


def product_control_lower_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_product_control_lower_setpoint(value):
    return set_signed_int_tens_decimal(value)


def condensation_control(name, value):
    s = state_on_off.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_condensation_control(value):
    value = value.lower()
    for mode_state, mode_name in state_on_off.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def condensation_control_monitor_mode(name, value):
    s = state_condensation_control_monitor_mode.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_condensation_control_monitor_mode(value):
    value = value.lower()
    for mode_state, mode_name in state_condensation_control_monitor_mode.iteritems():
        if mode_name == value:
            return mode_state
    return "NOMATCH"


def condensation_control_input_selection(name, value):
    bit_array = bitfield(value)
    response_condensation_control_input_selection = {
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
    return name, "pv:{}".format(response_condensation_control_input_selection)


def set_condensation_control_input_selection(value):
    # TODO
    value


def condensation_control_temperatore_ramp_rate_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_condensation_control_temperatore_ramp_rate_limit(value):
    return set_signed_int_tens_decimal(value)


def condensation_control_deupoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def condensation_control_duepoint_actual(name, value):
    return get_signed_int_tens_decimal(name, value)


def chamber_light_control(name, value):
    s = state_on_off.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_chamber_light_control(value):
    value = value.lower()
    for state_value, state_name in state_on_off.iteritems():
        if state_name == value:
            return state_value
    return "NOMATCH"


def chamber_manual_event_control(name, value):
    return get_event_control(name, value)


def set_chamber_manual_event_control(value):
    # TODO
    pass


def customer_manual_event_control(name, value):
    return get_event_control(name, value)


def set_customer_manual_event_control(value):
    # TODO
    pass


def profile_control_status(name, value):
    s = state_profile_control_status.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def set_profile_control_status(value):
    value = value.lower()
    for state_value, state_name in state_profile_control_status.iteritems():
        if state_name == value:
            return state_value
    return "NOMATCH"


def set_profile_advance_step(value):
    state = {
        1: 'advance previous step',
        2: 'advance next step'
    }
    value = value.lower()
    for state_value, state_name in state.iteritems():
        if state_name == value:
            return state_value
    return "NOMATCH"


def profile_name_ch_1_2(name, value):
    """
    32 – 126 (high byte)
    32 – 126 (low byte)
    """
    b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
    hch = struct.unpack('B', b_hch)[0]
    lch = struct.unpack('B', b_lch)[0]
    return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))


def profile_name_ch_3_4(name, value):
    """
    32 – 126 (high byte)
    32 – 126 (low byte)
    """
    b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
    hch = struct.unpack('B', b_hch)[0]
    lch = struct.unpack('B', b_lch)[0]
    return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))


def profile_name_ch_5_6(name, value):
    """
    32 – 126 (high byte)
    32 – 126 (low byte)
    """
    b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
    hch = struct.unpack('B', b_hch)[0]
    lch = struct.unpack('B', b_lch)[0]
    return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))


def profile_name_ch_7_8(name, value):
    """
    32 – 126 (high byte)
    32 – 126 (low byte)
    """
    b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
    hch = struct.unpack('B', b_hch)[0]
    lch = struct.unpack('B', b_lch)[0]
    return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))


def profile_name_ch_9_10(name, value):
    """
    32 – 126 (high byte)
    32 – 126 (low byte)
    """
    b_hch, b_lch = int_to_two_bytes(value & 0xFFFF)
    hch = struct.unpack('B', b_hch)[0]
    lch = struct.unpack('B', b_lch)[0]
    return name, "{} {}".format(str(unichr(hch)), str(unichr(lch)))


def profile_start_date_yy_mm(name, value):
    """
    high byte: Year: 0 to 99
    low byte: Month: 1=Jan, ... 12=Dec
    """
    b_year, b_month = int_to_two_bytes(value & 0xFFFF)
    year = struct.unpack('B', b_year)[0]
    month = struct.unpack('B', b_month)[0]
    return name, "year: 20{}, month:{}".format(year, month)


def profile_stop_date_yy_mm(name, value):
    """
    high byte: Year: 0 to 99
    low byte: Month: 1=Jan, ... 12=Dec
    """
    b_year, b_month = int_to_two_bytes(value & 0xFFFF)
    year = struct.unpack('B', b_year)[0]
    month = struct.unpack('B', b_month)[0]
    return name, "year: 20{}, month:{}".format(year, month)


def profile_start_date_day_dow(name, value):
    """
    high byte: Day of Month: 1 to 31
    low byte: Day  of Week: 0=Sun, ... 6=Sat
    """
    b_dom, b_dow = int_to_two_bytes(value & 0xFFFF)
    dom = struct.unpack('B', b_dom)[0]
    dow = struct.unpack('B', b_dow)[0]
    return name, "DayOfMonth:{}, DayOfWeek:{}".format(dom, dow)


def profile_stop_date_day_dow(name, value):
    """
    high byte: Day of Month: 1 to 31
    low byte: Day  of Week: 0=Sun, ... 6=Sat
    """
    b_dom, b_dow = int_to_two_bytes(value & 0xFFFF)
    dom = struct.unpack('B', b_dom)[0]
    dow = struct.unpack('B', b_dow)[0]
    return name, "DayOfMonth:{}, DayOfWeek:{}".format(dom, dow)


def profile_start_date_hh_mm(name, value):
    """
    high byte: Hours: 1 to 23
    low byte: Minutes: 0 to 59
    """
    b_hour, b_minutes = int_to_two_bytes(value & 0xFFFF)
    hour = struct.unpack('B', b_hour)[0]
    minutes = struct.unpack('B', b_minutes)[0]
    return name, "Hour:{}, Minute:{}".format(hour, minutes)


def profile_stop_date_hh_mm(name, value):
    """
    high byte: Hours: 1 to 23
    low byte: Minutes: 0 to 59
    """
    b_hour, b_minutes = int_to_two_bytes(value & 0xFFFF)
    hour = struct.unpack('B', b_hour)[0]
    minutes = struct.unpack('B', b_minutes)[0]
    return name, "Hour:{}, Minute:{}".format(hour, minutes)


def profile_start_step(name, value):
    """0 - 99"""
    return name, "step:{}".format(value)


def set_profile_start_step(value):
    """0 - 99"""
    assert 0 <= value <= 99
    return value


def profile_current_step(name, value):
    """0 - 99"""
    return name, "step:{}".format(value)


def profile_last_step(name, value):
    """0 - 99"""
    return name, "step:{}".format(value)


def profile_time_left_in_current_step_hhh(name, value):
    """1 – 999 Hours"""
    return name, "hours:{}".format(value)


def profile_time_left_in_current_step_mm_ss(name, value):
    """
     high byte: Minutes: 0 to 59
     low byte: Seconds: 0 to 59
     """
    b_minutes, b_seconds = int_to_two_bytes(value & 0xFFFF)
    minutes = struct.unpack('B', b_minutes)[0]
    seconds = struct.unpack('B', b_seconds)[0]
    return name, "Minute:{}, Seconds:{}".format(minutes, seconds)


def profile_wait_for_status(name, value):
    s = state_profile_wait_for_status.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


def profile_wait_for_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def profile_current_jump_step(name, value):
    """0 - 99"""
    return name, "step:{}".format(value)


def profile_jumps_remaining_in_current_step(name, value):
    """0 - 99"""
    return name, "jumps:{}".format(value)


def profile_loop_1_target_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def profile_loop_2_target_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def profile_loop_3_target_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def profile_loop_4_target_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def profile_loop_5_target_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def profile_last_jump_from_step(name, value):
    """0 - 99"""
    return name, "step:{}".format(value)


def profile_last_jump_to_step(name, value):
    """0 - 99"""
    return name, "step:{}".format(value)


def profile_total_jumps_made(name, value):
    """0 – 32767"""
    return name, "jumps:{}".format(value)


def set_alarm_acknowledge(value):
    state = {
        1: 'alarm silence',
        2: 'pumpdown reset'
    }
    value = value.lower()
    for state_value, state_name in state.iteritems():
        if state_name == value:
            return state_value
    return "NOMATCH"


def ezt570i_alarm_status(name, value):
    bit_array = bitfield(value)
    response = {
        'Input1 Sensor Break': state_alarm[bit_array[0]],
        'Input2 Sensor Break': state_alarm[bit_array[1]],
        'Input3 Sensor Break': state_alarm[bit_array[2]],
        'Input4 Sensor Break': state_alarm[bit_array[3]],
        'Input5 Sensor Break': state_alarm[bit_array[4]],
        'Input6 Sensor Break': state_alarm[bit_array[5]],
        'Input7 Sensor Break': state_alarm[bit_array[6]],
        'Input8 Sensor Break': state_alarm[bit_array[7]],
        'Input9 Sensor Break': state_alarm[bit_array[8]],
        'Input10 Sensor Break': state_alarm[bit_array[9]],
        'Input11 Sensor Break': state_alarm[bit_array[10]],
        'Input12 Sensor Break': state_alarm[bit_array[11]],
        'Input13 Sensor Break': state_alarm[bit_array[12]],
        '(not assigned)': state_alarm[bit_array[13]],
        'Loop Communications Failure': state_alarm[bit_array[14]],
    }
    return name, "status:{}".format(response)


def input_alarm_status(name, value):
    bit_array = bitfield(value)
    response = {
        'Input1 Alarm': state_alarm[bit_array[0]],
        'Input2 Alarm': state_alarm[bit_array[1]],
        'Input3 Alarm': state_alarm[bit_array[2]],
        'Input4 Alarm': state_alarm[bit_array[3]],
        'Input5 Alarm': state_alarm[bit_array[4]],
        'Input6 Alarm': state_alarm[bit_array[5]],
        'Input7 Alarm': state_alarm[bit_array[6]],
        'Input8 Alarm': state_alarm[bit_array[7]],
        'Input9 Alarm': state_alarm[bit_array[8]],
        'Input10 Alarm': state_alarm[bit_array[9]],
        'Input11 Alarm': state_alarm[bit_array[10]],
        'Input12 Alarm': state_alarm[bit_array[11]],
        'Input13 Alarm': state_alarm[bit_array[12]],
        '(not assigned 1)': state_alarm[bit_array[13]],
        '(not assigned 2)': state_alarm[bit_array[14]]
    }
    return name, "status:{}".format(response)


def chamber_alarm_status(name, value):
    bit_array = bitfield(value)
    response = {
        'Heater High Limit (Plenum A)': state_alarm[bit_array[0]],
        'External Product Safety': state_alarm[bit_array[1]],
        'Boiler Over-Temp (Plenum A)': state_alarm[bit_array[2]],
        'Boiler Low Water (Plenum A)': state_alarm[bit_array[3]],
        'Dehumidifier System Fault (System B Boiler Over-Temp)': state_alarm[bit_array[4]],
        'Motor Overload (Plenum A)': state_alarm[bit_array[5]],
        'Fluid System High Limit (Plenum B Heater High Limit)': state_alarm[bit_array[6]],
        'Fluid System High Pressure (Plenum B Motor Overload)': state_alarm[bit_array[7]],
        'Fluid System Low Flow': state_alarm[bit_array[8]],
        'Door Open': state_alarm[bit_array[9]],
        '(System B Boiler Low Water)': state_alarm[bit_array[10]],
        '(not assigned)': state_alarm[bit_array[11]],
        'Emergency Stop': state_alarm[bit_array[12]],
        'Power Failure': state_alarm[bit_array[13]],
        'Transfer Error': state_alarm[bit_array[14]],
    }
    return name, "status:{}".format(response)


def refrigeration_alarm_status(name, value):
    bit_array = bitfield(value)
    response = {
        'System 1(A) High/Low Pressure': state_alarm[bit_array[0]],
        'System 1(A) Low Oil Pressure': state_alarm[bit_array[1]],
        'System 1(A) High Discharge Temperature': state_alarm[bit_array[2]],
        'System 1(A) Compressor Protection Module': state_alarm[bit_array[3]],
        'Pumpdown Disabled': state_alarm[bit_array[4]],
        'System 1(A) Floodback Monitor': state_alarm[bit_array[5]],
        '(not assigned) 1': state_alarm[bit_array[6]],
        '(not assigned) 2': state_alarm[bit_array[7]],
        'System 2(B) High/Low Pressure': state_alarm[bit_array[8]],
        'System 2(B) Low Oil Pressure': state_alarm[bit_array[9]],
        'System 2(B) High Discharge Temperature': state_alarm[bit_array[10]],
        'System 2(B) Compressor Protection Module': state_alarm[bit_array[11]],
        '(not assigned) 3': state_alarm[bit_array[12]],
        'System B Floodback Monitor': state_alarm[bit_array[13]],
        '(not assigned) 4': state_alarm[bit_array[14]],
    }
    return name, "status:{}".format(response)


def system_status_monitor(name, value):
    bit_array = bitfield(value)
    response = {
        'Humidity Water Reservoir Low': state_alarm[bit_array[0]],
        'Humidity Disabled (temperature out-of-range)': state_alarm[bit_array[1]],
        'Humidity High Dewpoint Limit': state_alarm[bit_array[2]],
        'Humidity Low Dewpoint Limit': state_alarm[bit_array[3]],
        'Door Open': state_alarm[bit_array[4]],
        '(not assigned) 1': state_alarm[bit_array[5]],
        '(not assigned) 2': state_alarm[bit_array[6]],
        '(not assigned) 3': state_alarm[bit_array[7]],
        'Service Air Circulators': state_alarm[bit_array[8]],
        'Service Heating/Cooling System': state_alarm[bit_array[9]],
        'Service Humidity System': state_alarm[bit_array[10]],
        'Service Purge System': state_alarm[bit_array[11]],
        'Service Altitude System': state_alarm[bit_array[12]],
        'Service Transfer Mechanism': state_alarm[bit_array[13]],
        '(not assigned) 4': state_alarm[bit_array[14]],
    }
    return name, "status:{}".format(response)


def loop_1_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_1_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_2_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_2_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_3_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_3_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_4_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_4_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_5_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_5_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_1_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_1_process_value(value):
    return set_signed_int_tens_decimal(value)


def loop_2_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_2_process_value(value):
    return set_signed_int_tens_decimal(value)


def loop_3_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_3_process_value(value):
    return set_signed_int_tens_decimal(value)


def loop_4_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_4_process_value(value):
    return set_signed_int_tens_decimal(value)


def loop_5_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_5_process_value(value):
    return set_signed_int_tens_decimal(value)


def loop_1_percent_output(name, value):
    return get_loop_percent_output(name, value)


def set_loop_1_percent_output(value):
    return set_loop_percent_output(value)


def loop_2_percent_output(name, value):
    return get_loop_percent_output(name, value)


def set_loop_2_percent_output(value):
    return set_loop_percent_output(value)


def loop_3_percent_output(name, value):
    return get_loop_percent_output(name, value)


def set_loop_3_percent_output(value):
    return set_loop_percent_output(value)


def loop_4_percent_output(name, value):
    return get_loop_percent_output(name, value)


def set_loop_4_percent_output(value):
    return set_loop_percent_output(value)


def loop_5_percent_output(name, value):
    return get_loop_percent_output(name, value)


def set_loop_5_percent_output(value):
    return set_loop_percent_output(value)


def loop_1_autotune_status(name, value):
    return get_loop_autotune_status(name, value)


def set_loop_1_autotune_status(value):
    return set_loop_autotune_status(value)


def loop_2_autotune_status(name, value):
    return get_loop_autotune_status(name, value)


def set_loop_2_autotune_status(value):
    return set_loop_autotune_status(value)


def loop_3_autotune_status(name, value):
    return get_loop_autotune_status(name, value)


def set_loop_3_autotune_status(value):
    return set_loop_autotune_status(value)


def loop_4_autotune_status(name, value):
    return get_loop_autotune_status(name, value)


def set_loop_4_autotune_status(value):
    return set_loop_autotune_status(value)


def loop_5_autotune_status(name, value):
    return get_loop_autotune_status(name, value)


def set_loop_5_autotune_status(value):
    return set_loop_autotune_status(value)


def loop_1_upper_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_1_upper_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_2_upper_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_2_upper_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_3_upper_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_3_upper_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_4_upper_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_4_upper_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_5_upper_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_5_upper_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_1_lower_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_1_lower_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_2_lower_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_2_lower_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_3_lower_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_3_lower_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_4_lower_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_4_lower_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_5_lower_setpoint_limit(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_5_lower_setpoint_limit(value):
    return set_signed_int_tens_decimal(value)


def loop_1_alarm_type(name, value):
    return get_loop_alarm_type(name, value)


def set_loop_1_alarm_type(value):
    return set_loop_alarm_type(value)


def loop_2_alarm_type(name, value):
    return get_loop_alarm_type(name, value)


def set_loop_2_alarm_type(value):
    return set_loop_alarm_type(value)


def loop_3_alarm_type(name, value):
    return get_loop_alarm_type(name, value)


def set_loop_3_alarm_type(value):
    return set_loop_alarm_type(value)


def loop_4_alarm_type(name, value):
    return get_loop_alarm_type(name, value)


def set_loop_4_alarm_type(value):
    return set_loop_alarm_type(value)


def loop_5_alarm_type(name, value):
    return get_loop_alarm_type(name, value)


def set_loop_5_alarm_type(value):
    return set_loop_alarm_type(value)


def loop_1_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_loop_1_alarm_mode(value):
    return set_loop_alarm_mode(value)


def loop_2_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_loop_2_alarm_mode(value):
    return set_loop_alarm_mode(value)


def loop_3_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_loop_3_alarm_mode(value):
    return set_loop_alarm_mode(value)


def loop_4_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_loop_4_alarm_mode(value):
    return set_loop_alarm_mode(value)


def loop_5_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_loop_5_alarm_mode(value):
    return set_loop_alarm_mode(value)


def loop_1_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_loop_1_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def loop_2_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_loop_2_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def loop_3_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_loop_3_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def loop_4_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_loop_4_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def loop_5_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_loop_5_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def loop_1_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_1_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_2_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_2_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_3_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_3_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_4_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_4_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_5_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_5_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_1_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_1_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_2_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_2_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_3_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_3_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_4_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_4_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_5_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_5_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def loop_1_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_1_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def loop_2_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_2_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def loop_3_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_3_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def loop_4_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_4_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def loop_5_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_loop_5_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_1_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def monitor_input_2_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def monitor_input_3_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def monitor_input_4_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def monitor_input_5_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def monitor_input_6_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def monitor_input_7_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def monitor_input_8_process_value(name, value):
    return get_signed_int_tens_decimal(name, value)


def monitor_input_1_alarm_type(name, value):
    return get_monitor_input_alarm_type(name, value)


def set_monitor_input_1_alarm_type(value):
    return set_monitor_input_alarm_type(value)


def monitor_input_2_alarm_type(name, value):
    return get_monitor_input_alarm_type(name, value)


def set_monitor_input_2_alarm_type(value):
    return set_monitor_input_alarm_type(value)


def monitor_input_3_alarm_type(name, value):
    return get_monitor_input_alarm_type(name, value)


def set_monitor_input_3_alarm_type(value):
    return set_monitor_input_alarm_type(value)


def monitor_input_4_alarm_type(name, value):
    return get_monitor_input_alarm_type(name, value)


def set_monitor_input_4_alarm_type(value):
    return set_monitor_input_alarm_type(value)


def monitor_input_5_alarm_type(name, value):
    return get_monitor_input_alarm_type(name, value)


def set_monitor_input_5_alarm_type(value):
    return set_monitor_input_alarm_type(value)


def monitor_input_6_alarm_type(name, value):
    return get_monitor_input_alarm_type(name, value)


def set_monitor_input_6_alarm_type(value):
    return set_monitor_input_alarm_type(value)


def monitor_input_7_alarm_type(name, value):
    return get_monitor_input_alarm_type(name, value)


def set_monitor_input_7_alarm_type(value):
    return set_monitor_input_alarm_type(value)


def monitor_input_8_alarm_type(name, value):
    return get_monitor_input_alarm_type(name, value)


def set_monitor_input_8_alarm_type(value):
    return set_monitor_input_alarm_type(value)


def monitor_input_1_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_monitor_input_1_alarm_mode(value):
    return set_loop_alarm_mode(value)


def monitor_input_2_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_monitor_input_2_alarm_mode(value):
    return set_loop_alarm_mode(value)


def monitor_input_3_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_monitor_input_3_alarm_mode(value):
    return set_loop_alarm_mode(value)


def monitor_input_4_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_monitor_input_4_alarm_mode(value):
    return set_loop_alarm_mode(value)


def monitor_input_5_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_monitor_input_5_alarm_mode(value):
    return set_loop_alarm_mode(value)


def monitor_input_6_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_monitor_input_6_alarm_mode(value):
    return set_loop_alarm_mode(value)


def monitor_input_7_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_monitor_input_7_alarm_mode(value):
    return set_loop_alarm_mode(value)


def monitor_input_8_alarm_mode(name, value):
    return get_loop_alarm_mode(name, value)


def set_monitor_input_8_alarm_mode(value):
    return set_loop_alarm_mode(value)


def monitor_input_1_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_monitor_input_1_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def monitor_input_2_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_monitor_input_2_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def monitor_input_3_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_monitor_input_3_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def monitor_input_4_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_monitor_input_4_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def monitor_input_5_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_monitor_input_5_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def monitor_input_6_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_monitor_input_6_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def monitor_input_7_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_monitor_input_7_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def monitor_input_8_alarm_output_assignment(name, value):
    return get_loop_alarm_output_assignment(name, value)


def set_monitor_input_8_alarm_output_assignment(value):
    return set_loop_alarm_output_assignment(value)


def monitor_input_1_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_1_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_2_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_2_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_3_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_3_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_4_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_4_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_5_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_5_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_6_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_6_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_7_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_7_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_8_high_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_8_high_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_1_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_1_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_2_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_2_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_3_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_3_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_4_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_4_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_5_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_5_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_6_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_6_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_7_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_7_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_8_low_alarm_setpoint(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_8_low_alarm_setpoint(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_1_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_1_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_2_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_2_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_3_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_3_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_4_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_4_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_5_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_5_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_6_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_6_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_7_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_7_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def monitor_input_8_alarm_hysteresis(name, value):
    return get_signed_int_tens_decimal(name, value)


def set_monitor_input_8_alarm_hysteresis(value):
    return set_signed_int_tens_decimal(value)


def set_profile_step_time_adjustment(value):
    """
    0 – 32767 minutes
    """
    assert 0 <= value <= 32767
    return value


def ezt570i_offline_download_profile(name, value):
    state = {
        0: 'Online',
        1: 'Offline/Downloading Profile'
    }
    s = state.get(value, "{} Not specified in API".format(value))
    return name, "Status:{}".format(s)


# Dictionary map bytes to function
ctrl_profile_headr_registers = {
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


def get_profile_step_regs(step):
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
    return {
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
