#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""EZT570i Modbus packets
By John Stile At Meyer Sound Laboratories Inc.
this is distributed under a MIT license, see LICENSE
"""

import binascii  # for human readable access to bit packed data
import ctypes  # to access binary packed data in calibration file


def write_profile_factory(register_count):
    """Use factory to return properly sized structure
     which depends on the register_count parameter"""

    class WriteProfileSend(ctypes.BigEndianStructure):
        """For Profile Download only, to transmit profile data one step at a time.
        SEE "Profile Parameters" section for a list of all registers.
        The EZT-570i will respond to each message received, but not executed.

            Write Register Send Packet:
                   nn | nn | nn nn | nn  nn  | nn  | nn nn ... nn nn | nn nn
                  0x01 0x10  |  |   0x00 0x0F 0x1E   |  |      |  |    |  |
        address ___|    |    |  |    |   |     |     |  |      |  |    |  |
        command ________|    |  |    |   |     |     |  |      |  |    |  |
        reg high byte _______|  |    |   |     |     |  |      |  |    |  |
        reg low  byte __________|    |   |     |     |  |      |  |    |  |
        quantity to write high byte _|   |     |     |  |      |  |    |  |
        quantity to write low byte ______|     |     |  |      |  |    |  |
        quantity of data bytes ________________|     |  |      |  |    |  |
        data 1 high byte ____________________________|  |      |  |    |  |
        data 1 low byte ________________________________|      |  |    |  |
        ...                                                    |  |    |  |
        ...                                                    |  |    |  |
        data 15 high byte _____________________________________|  |    |  |
        data 15 low byte _________________________________________|    |  |
        crc low byte___________________________________________________|  |
        crc high byte ____________________________________________________|

        """
        _pack_ = 1  # Do not align on word boundary, interferes with debug logs
        _fields_ = [
            ("address",  ctypes.c_uint8),   # Address
            ("command",  ctypes.c_uint8),   # Command
            ("reg",      ctypes.c_uint16),  # Register
            ("quantity", ctypes.c_uint16),  # Quantity of registers (15)
            ("dsize",    ctypes.c_uint8),   # Data size in bytes (30)
            ("data",     ctypes.c_int16 * register_count),  # Dynamic
            ("crc",      ctypes.c_uint16),  # 16bit crc
        ]

        def __init__(self, data_count):
            super(WriteProfileSend, self).__init__()
            self.data_count = data_count

        def __repr__(self):
            return (
                (
                    "\n"
                    "address:{}\n"
                    "command:{}\n"
                    "reg:{}\n"
                    "quantity:{}\n"
                    "dsize:{}\n"
                    "data:{}\n"
                    "crc:{}"
                ).format(
                    self.address,
                    self.command,
                    self.reg,
                    self.quantity,
                    self.dsize,
                    self.data,
                    self.crc
                )
            )

        def __str__(self):
            """human readable data"""
            data_hex_string = binascii.hexlify(self.data)

            return (
                (
                    '\n'
                    '\tAddress: {:02X}\n'
                    '\tCommand: {:02X}\n'
                    '\tRegister:{:04X}\n'
                    '\tQuantity:{:04X}\n'
                    '\tDSize:   {:02X}\n'
                    '\tData:    {}\n'
                    '\tCRC:     {:04X}'
                ).format(
                    self.address,
                    self.command,
                    self.reg,
                    self.quantity,
                    self.dsize,
                    data_hex_string,
                    self.crc
                )
            )

    return WriteProfileSend(register_count)


class WriteProfileResponse(ctypes.Structure):
    """For Profile Download only, response packet from valid write:
                   nn | nn | nn nn | nn  nn   | nn nn
                  0x01 0x10  |  |   0x00 0x0F   |  |
        address ___|    |    |  |    |   |      |  |
        command ________|    |  |    |   |      |  |
        reg high byte _______|  |    |   |      |  |
        reg low  byte __________|    |   |      |  |
        quantity to write high byte _|   |      |  |
        quantity to write low byte ______|      |  |
        crc low byte ___________________________|  |
        crc high byte _____________________________|

    """
    _pack_ = 1  # Do not align on word boundary, interferes with debug logs
    _fields_ = [
        ("address",  ctypes.c_uint8),  # Address
        ("command",  ctypes.c_uint8),  # Command
        ("reg", ctypes.c_uint16),      # Register
        ("qty", ctypes.c_uint16),      # Number written
        ("crc", ctypes.c_uint16),      # 16bit
    ]

    def __repr__(self):
            return (
                (
                    "\n"
                    "address:{}\n"
                    "command:{}\n"
                    "reg:{}\n"
                    "qty:{}\n"
                    "crc:{}"
                ).format(
                    self.address,
                    self.command,
                    self.reg,
                    self.qty,
                    self.crc
                )
            )

    def __str__(self):
        """human readable data"""
        return (
            (
                '\n'
                '\tAddress: {:02X}\n'
                '\tCommand: {:02X}\n'
                '\tRegister:{:04X}\n'
                '\tQty:     {:04X}\n'
                '\tCRC:     {:04X}'
            ).format(
                self.address,
                self.command,
                self.reg,
                self.qty,
                self.crc
            )
        )


class WriteRegister(ctypes.BigEndianStructure):
    """Write value to single register, for setting control values.
    To set multiple values, repeat the command for each data location.
    Since Send and Response packets are the same format,
    use this class for both

    Write Register Send Packet:
               nn | nn | nn nn | nn nn | nn nn
              0x01 0x06  |  |    |  |    |  |
    address ___|    |    |  |    |  |    |  |
    command ________|    |  |    |  |    |  |
    reg high byte _______|  |    |  |    |  |
    reg low  byte __________|    |  |    |  |
    data high byte ______________|  |    |  |
    data low byte __________________|    |  |
    crc low byte_________________________|  |
    crc high byte __________________________|

    Example 1: Write register 60 (temperature set point) of address 01 to 20 degrees.
    Sent: 01  06   00 3C   00 C8   48 50

    NOTE: might want to test with light, as it won't effect running test.
    --> r/w 21 (0x0015), Chamber Light Control, 0 = Light Off, 1=Light On
    Sent: 01  06   00 15   00 01  <crc>
    """
    _pack_ = 1  # Do not align on word boundary, interferes with debug logs
    _fields_ = [
        ("address", ctypes.c_uint8),  # Address
        ("command", ctypes.c_uint8),  # Command
        ("reg", ctypes.c_uint16),     # Register
        ("value", ctypes.c_uint16),   # Set Value
        ("crc", ctypes.c_uint16),     # 16bit crc
    ]

    def __repr__(self):
        return (
            (
                "\n"
                "address:{}\n"
                "command:{}\n"
                "reg:{}\n"
                "value:{}\n"
                "crc:{}"
            ).format(
                self.address,
                self.command,
                self.reg,
                self.value,
                self.crc
            )
        )

    def __str__(self):
        """human readable data"""
        return (
            (
                '\n'
                '\tAddress: {:02X}\n'
                '\tCommand: {:02X}\n'
                '\tRegister:{:04X}\n'
                '\tValue:   {:04X}\n'
                '\tCRC:     {:04X}\n'
            ).format(
                 self.address,
                 self.command,
                 self.reg,
                 self.value,
                 self.crc
            )
        )


class ReadRegistersSend(ctypes.BigEndianStructure):
    """Read Register Send packet:
               nn | nn | nn nn nn nn | nn nn
              0x01 0x03  |  |  |  |    |  |
    address ___|    |    |  |  |  |    |  |
    command ________|    |  |  |  |    |  |
    start reg high byte _|  |  |  |    |  |
    start reg low  byte ____|  |  |    |  |
    quantity to read high byte |  |    |  |
    quantity to read low byte ____|    |  |
    crc low byte ______________________|  |
    crc high byte ________________________|

    Example 1: Read register 61 (chamber temperature) of controller at address 1.
    Sent:     01  03  00 3D 00 01  15 C6
    """
    _pack_ = 1  # Do not align on word boundary, interferes with debug logs
    _fields_ = [
        ("address",  ctypes.c_uint8),   # Address
        ("command",  ctypes.c_uint8),   # Command
        ("reg",      ctypes.c_uint16),  # Register
        ("quantity", ctypes.c_uint16),  # Quantity of Registers to read
        ("crc",      ctypes.c_uint16),  # 16bit crc
    ]

    def __repr__(self):
        return (
            (
                "\n"
                "address:{}\n"
                "command:{}\n"
                "reg:{}\n"
                "quantity:{}\n"
                "crc:{}"
            ).format(
                self.address,
                self.command,
                self.reg,
                self.quantity,
                self.crc
            )
        )

    def __str__(self):
        """human readable data"""
        return (
            (
                '\n'
                '\tAddress: {:02X}\n'
                '\tCommand: {:02X}\n'
                '\tRegister:{:04X}\n'
                '\tQuantity:{:04X}\n'
                '\tCRC:     {:04X}'
            ).format(
                 self.address,
                 self.command,
                 self.reg,
                 self.quantity,
                 self.crc
            )
        )


def read_response_factory(quantity):
    """Use factory to return properly sized structure
     which depends on the byte_count parameter"""

    class ReadRegisterReceive(ctypes.BigEndianStructure):
        """Read Register Receive Packet:
                   nn | nn | nn | nn nn .. .. | nn nn
                  0x01 0x03  |    |  |  |  |    |  |
        address ___|    |    |    |  |  |  |    |  |
        command ________|    |    |  |  |  |    |  |
        number of of bytes __|    |  |  |  |    |  |
        value reg high byte ______|  |  |  |    |  |
        value reg low  byte _________|  |  |    |  |
        ... next value reg high ________|  |    |  |
        ... next value reg low ____________|    |  |
        crc low byte ___________________________|  |
        crc high byte _____________________________|

        Example 1: Read register 61 (chamber temperature) of controller at address 1.
        Received: 01  03  02 00 EC     B9 C9
        """
        _pack_ = 1  # Do not align on word boundary, interferes with debug logs
        _fields_ = [
            ("address",  ctypes.c_uint8),  # Address
            ("command",  ctypes.c_uint8),  # Command
            ("number",   ctypes.c_uint8),  # Number of values
            ("data",     ctypes.c_int16 * quantity),  # Dynamic
            ("crc",      ctypes.c_uint16),  # 16bit crc
        ]

        def __init__(self, quantity):
            super(ReadRegisterReceive, self).__init__()
            self.quantity = quantity

        def __repr__(self):
            return (
                (
                    "\n"
                    "address:{}\n"
                    "command:{}\n"
                    "number:{}\n"
                    "data:{}\n"
                    "crc:{}"
                ).format(
                    self.address,
                    self.command,
                    self.number,
                    self.data,
                    self.crc
                )
            )

        def __str__(self):
            """human readable data"""
            #TODO: NEED BETTER WAY TO HANDLE DYNAMIC NATURE OF THIS
            #data_hex_string = ''.join('{}'.format(b) for b in self.data)
            #data_celcius = int(data_hex_string)/10.0
            #data_hex_string = ''.join('{}'.format(b) for b in self.data)
            data_hex_string = binascii.hexlify(self.data)

            return (
                (
                    '\n'
                    '\tAddress:{:02X}\n'
                    '\tCommand:{:02X}\n'
                    '\tNumber: {:02X}\n'
                    '\tData:   {}\n'
                    '\tCRC:    {:04X}'
                ).format(
                    self.address,
                    self.command,
                    self.number,
                    data_hex_string,
                    self.crc
                )
            )

    return ReadRegisterReceive(quantity)
