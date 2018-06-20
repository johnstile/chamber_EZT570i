#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for talking to the ESZ Cincinnati Sub-Zero (EZT-570i) chamber over Modbus

The chamber speaks ModBus protocol over RS323 and RS485
Over RS232 can control 1 chamber, 
Over RS485 can control 31 chambers
Over ethernet, use ethernet-to-serial adapter (by gridconnect.com GC-FB-430)

The chamber rs232 requires specific serial port settings:
 baud:9600
 data bits: 8
 stop bits: 1
 flow control: none
 parity: Even

The Touch Screen on the front of the chamber is connected to a Windows CE computer.
The Windows CE computer saves the Profiles to compact flash.
The Windows CE computer does not offer a network share to access the files.
One must manually get the files from the computer.
We store the files on a nework file share:
\\fa.ms.msli.com\users\Engineering\Saturn\workspace\CSZ_CHAMBERS
"""

import binascii  # for human readable access to bit packed data
import ctypes  # to access binary packed data in calibration file
import struct  # for crc and message packing
import socket  # for tcp communication

import itertools
import serial  # for rs232 communication
import logging  # for log facility
import time

import modbus_packets


def int_or_float(s):
    """
    Modbus can't handle decimals, so we multiply any float by 10.
    :param s: string representation of a numeric value.
    :return: int
    """
    try:
        return int(s)
    except ValueError:
        # if we have a float,
        # protocol requires multiply by 10 and cast to int
        return int(float(s) * 10)


class ChamberCommunication(object):
    """Communication with EZT570i"""

    def __init__(self, comm_type='dummy', comm_params={}, log=None, chamber_number=1):
        self.log = log
        self.comm = None
        self.crc = None
        self.comm_type = comm_type
        self.comm_params = comm_params
        self.chamber_number  = chamber_number
        # Factory to abstract how we talk to the chamber
        self.comm_func = {
            'serial': {  # over rs232
                'connect': self.create_com_serial,
                'disconnect': self.disconnect_com_serial,
                'write': self.write_com_serial,
                'read': self.read_com_serial,
            },
            'network': {  # over network-to-rs232 adapter
                'connect': self.create_com_network,
                'disconnect': self.disconnect_com_network,
                'write': self.write_com_network,
                'read': self.read_com_network
            },
            'dummy': {  # when not connected, for development
                'connect': self.create_com_dummy,
                'disconnect': self.disconnect_com_dummy,
                'write': self.write_com_dummy,
                'read': self.read_com_dummy
            }
        }
        self.command = {
            "read_regs": 0x03,
            "write_reg": 0x06,
            "write_profile_reg": 0x10
        }
        # Get crc class
        self.crc = CRC16()
        # Messages are sent in packets that must be delimited by a pause at least as long as the time it
        # takes to send 28 bits (3.5 characters). To determine this time in seconds, divide 28 by the baud
        # rate. In the case of EZT-570i communications at 9600 baud, this calculates to a minimum period
        # of 3ms.
        #
        # In addition, the EZT’s timeout period must be added to that, in order to properly time the send and
        # receive messages between the host computer and multiple EZT’s on the serial link. With a
        # default timeout period in the EZT-570i of 200ms, it makes a total pause of 203ms minimum.
        self.comm_wait_time = 0.203

    def connect(self):
        if self.comm_type == 'network':
            assert self.comm_params['net_port'] and self.comm_params['net_addr'] and self.comm_params['net_timeout']
        elif self.comm_type == 'serial':
            assert self.comm_params['serial_port']

        # Get communication
        self.comm_func[self.comm_type]['connect']()
    
    def disconnect(self):
        # Get communication
        self.comm_func[self.comm_type]['disconnect']()

    def write_register(self, register, value):
        """
        Set the value of a register
        :param register: Address of register
        :param value: Value of to write.
        :return:
        """
        self.log.info(
            "\n"
            "# =========================================\n"
            "# Write Register\n"
            "# ========================================="
        )

        # --------------------------------------
        # PACKET HEADER FOR WRITE REGISTER
        # --------------------------------------
        # e.g. 0x01 0x06 0x0015 0x0001
        fmt = '!2B2H'
        packed_header = struct.pack(
            fmt,
            self.chamber_number,
            self.command['write_reg'],
            register,
            value
        )
        self.log.debug(
            "{:<80}:packed header".format(
                [hex(a) for a in struct.unpack(fmt, packed_header)]
            )
        )

        # Add CRC
        modbus_msg_as_bytes = self.crc.add_crc(packed_header)

        data_hexstring = binascii.hexlify(modbus_msg_as_bytes)
        self.log.debug("{:<20}:message + crc".format(data_hexstring))

        # load byte array into structure
        modbus_write_request = modbus_packets.WriteRegister()
        ctypes.memmove(
            ctypes.addressof(modbus_write_request),
            modbus_msg_as_bytes,
            len(modbus_msg_as_bytes)
        )

        # Print structure
        self.log.debug(
            (
                "Modbus Request: {}"
            ).format(
                modbus_write_request
            )
        )
        # --------------------------------------
        # Send request
        # --------------------------------------
        self.comm_func[self.comm_type]['write'](modbus_write_request)

        # --------------------------------------
        # Read response
        # --------------------------------------

        # Create response Structure sized for expected data
        modbus_write_response = modbus_packets.WriteRegister()

        modbus_response = self.read_response(modbus_write_response)

        self.log.debug(
            (
                "Modbus Request: {}"
            ).format(
                modbus_response
            )
        )

    def read_registers(self, register, quanity):
        """
        Read the value of a series of registers
        :param register: Starting register
        :param quanity: How many registers to read
        """
        self.log.info(
            (
                "\n# =========================================\n"
                "# Read Registers: reg:{}, quanity:{}\n"
                "# ========================================="
            ).format(
                register,
                quanity
            )
        )

        # --------------------------------------
        # PACKET HEADER READ REGISTERS
        # --------------------------------------
        # e.g. 0x01 0x03 0x003D 0x0001
        fmt = '!2B2H'
        packed_header = struct.pack(
            fmt,
            self.chamber_number,
            self.command['read_regs'],
            register,
            quanity
        )
        self.log.debug(
            (
                "{:<80}:packed header"
            ).format(
                [hex(a) for a in struct.unpack(fmt, packed_header)]
            )
        )

        # Add CRC
        modbus_msg_as_bytes = self.crc.add_crc(packed_header)

        data_hexstring = binascii.hexlify(modbus_msg_as_bytes)
        self.log.debug("{:<20}:message + crc".format(data_hexstring))

        # load structure
        modbus_read_request = modbus_packets.ReadRegistersSend()
        ctypes.memmove(
            ctypes.addressof(modbus_read_request),
            modbus_msg_as_bytes,
            len(modbus_msg_as_bytes)
        )
        self.log.debug(
            (
                "Modbus Request:{}"
            ).format(
                modbus_read_request
            )
        )

        # Send modbus request
        self.comm_func[self.comm_type]['write'](modbus_read_request)

        # Create response Structure sized for expected data
        modbus_read_response = modbus_packets.read_response_factory(quanity)

        # Read modbus response
        modbus_response = self.read_response(modbus_read_response)

        return modbus_response

    def read_response(self, modbus_response):

        size_read_response = ctypes.sizeof(modbus_response)

        # Read response to read request
        modbus_response_msg_as_bytes = \
            self.comm_func[self.comm_type]['read'](size_read_response)

        if self.comm_type is not 'dummy':
            # Validate response
            self.crc.validate_crc(modbus_response_msg_as_bytes)

        # Convert string to bytes to string of hex
        modebus_response_msg_as_hex = binascii.hexlify(modbus_response_msg_as_bytes)
        self.log.debug("{:<20} : response msg".format(modebus_response_msg_as_hex))

        # Populate the structure
        ctypes.memmove(
            ctypes.addressof(modbus_response),
            modbus_response_msg_as_bytes,
            len(modbus_response_msg_as_bytes)
        )

        # Print structure
        self.log.debug(
            (
                "Modbus Response:{}"
            ).format(
                modbus_response
            )
        )
        return modbus_response

    def load_profile(self, project_file):
        """
        Load a CSZ Profile file into the chamber.
        :param project_file: path to file
        :return:
        """
        self.log.info(
            (
                "\n"
                "# =========================================\n"
                "# WRITE PROFILE: {}\n"
                "# ========================================="
            ).format(
                project_file
            )
        )

        steps_tot = 0  # Steps in profile, read from first line
        step_counter = 0  # Track when to stop reading file

        # Read file into list of profile steps
        with open(project_file) as fh:

            # Harvest the first line
            profile_header = self.read_profile_lines(fh, 1)
            self.log.info("Profile Header:{}".format(profile_header))

            # Determine how many steps to read from file
            steps_tot = profile_header[0][9]
            self.log.info("Steps in Profile:{}".format(steps_tot))

            # Read steps from file
            profile_steps = self.read_profile_lines(fh, steps_tot)
            self.log.info("Steps loaded:{}".format(len(profile_steps)))
            # TODO: print each step in the profile

        self.log.info("Convert profile header+steps into list of modbus packets")
        # Convert profile header+steps into list of modbus packets
        modebus_packed_profile = self.profile_to_modbus_packets(
            profile_header, profile_steps
        )

        self.log.debug("Profile Packets")
        for i in modebus_packed_profile:
            self.log.debug("Packet:{}".format(i))

        self.write_profile_to_modbus(modebus_packed_profile)

    def write_profile_to_modbus(self, modebus_packed_profile):
        """
        Write profile packets to modbus
        :param modebus_packed_profile:
        :return:
        """
        self.log.info("Write profile to Modbus")

        for i, packet in enumerate(modebus_packed_profile):
            self.log.info("--------------Line:{} --------------".format(i))
            self.log.debug(
                'WriteProfileSend:{}'.format(packet)
            )
            # --------------------------------------
            # Send request
            # --------------------------------------
            self.comm_func[self.comm_type]['write'](packet)

            # --------------------------------------
            # Mandatory wait between each write
            # --------------------------------------
            time.sleep(self.comm_wait_time)

            # --------------------------------------
            # Read response
            # --------------------------------------

            # Create response Structure sized for expected data
            modbus_write_profile_response = modbus_packets.WriteProfileResponse()

            modbus_response = self.read_response(modbus_write_profile_response)

            # Print structure
            self.log.debug(
                (
                    "WriteProfileResponse:{}"
                ).format(
                    modbus_response
                )
            )
        self.log.info("Profile upload complete")

    def read_profile_lines(self, fh, lines):
        """
        Read the profile file, converting to list of int
        :param fh:
        :param lines:
        :return:
        """
        self.log.info("Read the profile file, converting to list of int")
        data_all_lines = []
        for i in xrange(lines):
            # Convert comma separated text to array of int, with 15 elements
            data_int_array = []
            data_list = fh.readline().strip().split(',')[:15]
            self.log.debug("data_str:{}".format(data_list))
            for val in data_list:
                # Convert string to int, floats are multiplied by 10
                val = int_or_float(val)
                # Finally add to the array
                data_int_array.append(val)

            self.log.debug("data_int_array:{}".format(data_int_array))
            data_all_lines.append(data_int_array)
        return data_all_lines

    def profile_to_modbus_packets(self, profile_header, profile_steps):
        """
        Convert list of int to list of modbus packets
        :param profile_header:
        :param profile_steps:
        :return:
        """
        self.log.info("Convert list of int to list of modbus packets")
        modebus_packed_profile = []

        register_start = 200  # First Register Address 0x00c8
        registers_to_write = 15  # data registers per packet
        bytes_written = 30   # data bytes in each packet

        for line, data_int_array in enumerate(itertools.chain(profile_header, profile_steps)):
            # Increment the starting register address by 15 for consecutive elements
            # First is 200, second is 215, third is 230, ....
            if line:
                register_start += registers_to_write

            # --------------------------------------
            # Convert array of int to packed data
            # --------------------------------------
            data_bytearray = bytearray()
            for i in data_int_array:
                s = struct.pack('!h', i)
                data_bytearray += s

            data_hexstring = binascii.hexlify(data_bytearray)
            self.log.debug("{:<80}:data_bytearray".format(data_hexstring))

            # --------------------------------------
            # PACKET HEADER FOR PROFILE WRITE
            # --------------------------------------
            fmt = '!2B2HB'
            packed_header = struct.pack(
                fmt,
                self.chamber_number,
                self.command['write_profile_reg'],
                register_start,
                registers_to_write,
                bytes_written
            )
            self.log.debug(
                "{:<80}:packed header".format(
                    [hex(a) for a in struct.unpack(fmt, packed_header)]
                )
            )

            # --------------------------------------
            # JOIN HEADER + DATA
            # --------------------------------------
            msg_as_bytes = bytes(packed_header) + bytes(data_bytearray)

            data_hexstring = binascii.hexlify(msg_as_bytes)
            self.log.debug("{:<80}:msg_as_bytes".format(data_hexstring))

            # --------------------------------------
            # Add CRC
            # --------------------------------------
            modbus_msg_as_bytes = self.crc.add_crc(msg_as_bytes)

            data_hexstring = binascii.hexlify(modbus_msg_as_bytes)
            self.log.debug("{:<80}:msg_as_bytes + crc".format(data_hexstring))

            # --------------------------------------
            # Load ctypes.Structure
            # --------------------------------------
            modbus_profile_request = modbus_packets.write_profile_factory(registers_to_write)
            ctypes.memmove(
                ctypes.addressof(modbus_profile_request),
                modbus_msg_as_bytes,
                len(modbus_msg_as_bytes)
            )
            # --------------------------------------
            # Append to list of packed data
            # --------------------------------------
            modebus_packed_profile.append(modbus_profile_request)

        return modebus_packed_profile

    def create_com_network(self):
        """Network Setup"""
        self.log.debug("Create tcp scoket communication object")
        self.log.debug("Opening socket")
        net_port = self.comm_params['net_port']
        net_addr = self.comm_params['net_addr']
        net_timeout = self.comm_params['net_timeout']
        self.comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm.connect((net_addr, net_port))
        self.comm.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.comm.settimeout(net_timeout)

    def create_com_serial(self):
        """Serial Port Setup"""
        self.log.debug("Create serial communication object")
        self.comm = serial.Serial(
            port= self.comm_params['serial_port'],
            baudrate=9600,
            timeout=1,
            parity=serial.PARITY_EVEN,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )

    def create_com_dummy(self):
        """Dummy Setup"""
        self.log.debug("Creating dummy communicaiton object")
        self.comm = ""

    def disconnect_com_network(self):
        self.comm.close()

    def disconnect_com_serial(self):
        self.comm.close()

    def disconnect_com_dummy(self):
        self.comm = None

    def write_com_serial(self, buffer):
        """Send request over Serial"""
        self.log.info("Send request")
        if not (self.comm and self.comm.is_open):
            self.comm.open()
        self.comm.write(buffer)
        time.sleep(self.comm_wait_time)

    def write_com_network(self, buffer):
        """Send request over Ethernet"""
        self.log.info("Send request")
        self.comm.sendall(buffer)
        time.sleep(self.comm_wait_time)

    def write_com_dummy(self,buffer):
        """Send request over Ethernet"""
        self.log.info("Send request")
        time.sleep(self.comm_wait_time)

    def read_com_serial(self, size_read_response):
        """Read serial port, return stuff"""
        self.log.info("Read response")
        return self.comm.read(size_read_response)

    def read_com_network(self, size_read_response):
        """Read network socket, return stuff"""
        self.log.info("Read response")
        chunks = []
        bytes_recd = 0
        while bytes_recd < size_read_response:
            self.log.debug("bytes_recd:{}".format(bytes_recd))
            chunk = self.comm.recv(1024)
            self.log.debug("chunk:{}".format(chunk))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

    def read_com_dummy(self, size_read_response):
        """Read nothing, return empty"""
        return ''

class CRC16(object):
    """
    Working with CRC16
    Most code is taken from: 
      https://github.com/pyhys/minimalmodbus/blob/e99f4d74c83258c6039073082955ac9bed3f2155/minimalmodbus.py  # NOQA
    """
    def __init__(self):
        self.look_up_table = self.generate_look_up_table()

    def generate_look_up_table(self):
        """ Generate look up table.

        :return: List
        """
        poly = 0xA001
        table = []

        for index in range(256):

            data = index << 1
            crc = 0
            for _ in range(8, 0, -1):
                data >>= 1
                if (data ^ crc) & 0x0001:
                    crc = (crc >> 1) ^ poly
                else:
                    crc >>= 1
            table.append(crc)

        return table

    def get_crc(self, msg):
        """ Return CRC of 2 byte for message.

        >>> assert self.get_crc(b'\x02\x07') == struct.unpack('<H', b'\x41\x12')

        :param msg: bytes.
        :return: 2 bytes.
        """
        register = 0xFFFF

        for byte_ in msg:
            try:
                val = struct.unpack('<B', byte_)[0]
            # Iterating over a bit-like objects in Python 3 gets you ints.
            except TypeError:
                val = byte_

            register = \
                (register >> 8) ^ self.look_up_table[(register ^ val) & 0xFF]

        # CRC is little-endian!
        return struct.pack('<H', register)

    def add_crc(self, msg):
        """ Append CRC to message.

        :param msg: bytes.
        :return: bytes.
        """
        return msg + self.get_crc(msg)

    def validate_crc(self, msg):
        """ Validate CRC of message.

        :param msg: bytes, message with CRC.
        :raise: CRCError.
        """
        if not struct.unpack('<H', self.get_crc(msg[:-2])) ==\
                struct.unpack('<H', msg[-2:]):
            raise CRCError('CRC validation failed.')


class CRCError(Exception):
    """ Valid error to raise when CRC isn't correct. """
    pass




if __name__ == '__main__':
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

    from chamber_commands import ChamberCommandRegisters
    commands = ChamberCommandRegisters()
    light_control = commands.ctrl['CHAMBER_LIGHT_CONTROL']

    chamber = ChamberCommunication(comm_type='dummy', log=log)
    chamber.connect()

    # Chamber "Profile" file
    project_file = 'GALILEO.txt'

    chamber.load_profile(project_file)

    state = {
        'Off' : 0,
        'On' : 1
    }
    chamber.read_registers(light_control)
    chamber.write_register(light_control, state['On'])
    chamber.read_registers(light_control)
    chamber.write_register(light_control, state['Off'])
    chamber.read_registers(light_control)
