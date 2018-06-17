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

    def __init__(self, comm_type='dummy', log=None):
        self.log = log
        self.comm = None
        self.crc = None
        self.comm_type = comm_type
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
            "# =========================================\n"
        )

        # --------------------------------------
        # PACKET HEADER
        # --------------------------------------
        # e.g. 0x01 0x06 0x0015 0x0001
        fmt = '!2B2H'
        packed_header = struct.pack(
            fmt,
            0x01,  # Device number
            0x06,  # Command
            register,
            value
        )
        self.log.info(
            "{:<80}:packed header".format(
                [hex(a) for a in struct.unpack(fmt, packed_header)]
            )
        )

        # Add CRC
        modbus_msg_as_bytes = self.crc.add_crc(packed_header)

        data_hexstring = binascii.hexlify(modbus_msg_as_bytes)
        self.log.info("{:<20}:message + crc".format(data_hexstring))

        # load byte array into structure
        modbus_write_request = modbus_packets.WriteRegister()
        ctypes.memmove(
            ctypes.addressof(modbus_write_request),
            modbus_msg_as_bytes,
            len(modbus_msg_as_bytes)
        )

        # Print structure
        self.log.info(
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
        size_read_response = ctypes.sizeof(modbus_write_response)

        # Read response to read request
        modbus_response_msg_as_bytes = \
            self.comm_func[self.comm_type]['read'](size_read_response)

        data_hexstring = binascii.hexlify(modbus_response_msg_as_bytes)
        self.log.info("string_read_response hexlify: {}".format(data_hexstring))

        if self.comm_type is not 'dummy':
            # Validate response
            self.crc.validate_crc(modbus_response_msg_as_bytes)

        # Populate the structure
        ctypes.memmove(
            ctypes.addressof(modbus_write_response),
            modbus_response_msg_as_bytes,
            len(modbus_response_msg_as_bytes)
        )

        self.log.info(
            (
                "Modbus Request: {}"
            ).format(
                modbus_write_response
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
                "\n"
                "# =========================================\n"
                "# Read Registers: reg:{}, quanity:{}\n"
                "# ========================================="
            ).format(
                register,
                quanity
            )
        )

        # --------------------------------------
        # PACKET HEADER
        # --------------------------------------
        # e.g. 0x01 0x03 0x003D 0x0001

        fmt = '!2B2H'
        packed_header = struct.pack(
            fmt,
            0x01,  # Device number
            0x03,  # Command
            register,
            quanity
        )
        self.log.info(
            "{:<80}:packed header".format(
                [hex(a) for a in struct.unpack(fmt, packed_header)]
            )
        )

        # Add CRC
        modbus_msg_as_bytes = self.crc.add_crc(packed_header)

        data_hexstring = binascii.hexlify(modbus_msg_as_bytes)
        self.log.info("{:<20}:message + crc".format(data_hexstring))

        # load structure
        modbus_read_request = modbus_packets.ReadRegistersSend()
        ctypes.memmove(
            ctypes.addressof(modbus_read_request),
            modbus_msg_as_bytes,
            len(modbus_msg_as_bytes)
        )
        self.log.info(
            (
                "Modbus Request:{}"
            ).format(
                modbus_read_request
            )
        )

        # --------------------------------------
        # Send request
        # --------------------------------------
        self.comm_func[self.comm_type]['write'](modbus_read_request)

        # Create response Structure sized for expected data
        modbus_read_response = modbus_packets.read_response_factory(quanity)
        size_read_response = ctypes.sizeof(modbus_read_response)

        # --------------------------------------
        # Read response
        # --------------------------------------
        modbus_response_msg_as_bytes = \
            self.comm_func[self.comm_type]['read'](size_read_response)

        if self.comm_type is not 'dummy':
            # Validate response
            self.crc.validate_crc(modbus_response_msg_as_bytes)

        # Convert string to bytes to string of hex
        modebus_response_msg_as_hex = binascii.hexlify(modbus_response_msg_as_bytes)
        self.log.info("{:<20} : response msg".format(modebus_response_msg_as_hex))

        # Populate the structure
        ctypes.memmove(
            ctypes.addressof(modbus_read_response),
            modbus_response_msg_as_bytes,
            len(modbus_response_msg_as_bytes)
        )

        # Print structure
        # self.log.debug(repr(modbus_read_response))
        self.log.info(
            (
                "Modbus Response:{}"
            ).format(
                modbus_read_response
            )
        )
        return modbus_read_response

    def load_profile(self, project_file):
        """
        Load a CSZ Profile file into the chamber.
        :param project_file: path to file
        :return:
        """
        with open(project_file) as fh:

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

            register_start = 200  # First Register Address 0x00c8
            register_count = 15  # number of registers per packet
            steps_tot = 0  # Steps in profile, read from first line
            step_counter = 0  # Track when to stop reading file

            line_counter = 0
            # Read file one line at a time
            for profile_line in fh:
                # Only used for log
                line_counter += 1
                self.log.info("--------------Line:{} --------------".format(line_counter))

                # --------------------------------------
                # LINE PARSER CODE:
                # ---------------------------------------

                # Convert comma separated text to array of int
                data_int_array = []
                for index, val in enumerate(profile_line.split(',')[:15]):
                    # Convert string to int, floats are multiplied by 10
                    val = int_or_float(val)

                    # Finally add to the array
                    data_int_array.append(val)

                self.log.info("data_int_array:{}".format(data_int_array))

                # First line of file, harvest number of steps in profile
                if not steps_tot:
                    steps_tot = data_int_array[9]

                # Stop reading file after steps are completes
                # The file has 100 lines, but upload only wants steps_tot.
                if step_counter > steps_tot:
                    self.log.info(
                        "Break: step_counter:{} > steps_tot:{}".format(
                            step_counter,
                            steps_tot
                        )
                    )
                    break

                # Handle counter management close to evaluation
                step_counter += 1

                # Convert array of int to packed data
                data_bytearray = bytearray()
                for i in data_int_array:
                    s = struct.pack('!h', i)
                    data_bytearray += s

                data_hexstring = binascii.hexlify(data_bytearray)
                self.log.debug("{:<80}:data_bytearray".format(data_hexstring))

                # --------------------------------------
                # PACKET HEADER
                # --------------------------------------
                # 0x01 0x10 0x00C6 0x000F 0x1E
                fmt = '!2B2HB'
                packed_header = struct.pack(
                    fmt,
                    0x01,  # Device number
                    0x10,  # Command
                    register_start,
                    0x00F,  # number of registers
                    0x1E  # bytes of data
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
                modbus_profile_request = modbus_packets.write_profile_factory(register_count)
                ctypes.memmove(
                    ctypes.addressof(modbus_profile_request),
                    modbus_msg_as_bytes,
                    len(modbus_msg_as_bytes)
                )
                self.log.info(
                    'WriteProfileSend:{}'.format(modbus_profile_request)
                )
                # --------------------------------------
                # Send request
                # --------------------------------------
                self.comm_func[self.comm_type]['write'](modbus_profile_request)

                # --------------------------------------
                # Mandatory 1 second sleep between each write
                # --------------------------------------
                time.sleep(1)

                # --------------------------------------
                # Read response
                # --------------------------------------

                # Create response Structure sized for expected data
                modbus_write_response = modbus_packets.WriteProfileResponse()
                size_read_response = ctypes.sizeof(modbus_write_response)

                # Read response to read request
                modbus_response_msg_as_bytes = \
                    self.comm_func[self.comm_type]['read'](size_read_response)

                data_hexstring = binascii.hexlify(modbus_response_msg_as_bytes)
                self.log.debug(
                    "string_read_response hexlify: {}".format(data_hexstring)
                )

                if self.comm_type is not 'dummy':
                    # Validate response
                    self.crc.validate_crc(modbus_response_msg_as_bytes)

                # Populate the structure
                ctypes.memmove(
                    ctypes.addressof(modbus_write_response),
                    modbus_response_msg_as_bytes,
                    len(modbus_response_msg_as_bytes)
                )

                # Print structure
                self.log.info(
                    (
                        "WriteProfileResponse:{}"
                    ).format(
                        modbus_write_response
                    )
                )

                # Increment the Register address by 15 for the next line of file
                register_start += register_count

    def create_com_network(self):
        """Network Setup"""
        self.log.debug("Create tcp scoket communication object")
        self.log.debug("Opening socket")
        net_port = 50000
        net_addr = '192.168.0.36'
        net_timeout = 20
        self.comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm.connect((net_addr, net_port))
        self.comm.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.comm.settimeout(net_timeout)

    def create_com_serial(self):
        """Serial Port Setup"""
        self.log.debug("Create serial communication object")
        self.comm = serial.Serial(
            port='/dev/ttyUSB0',
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
    project_file = '/home/jstile/chamber/our_files/Profiles_09-01-2017-09-53-40/GALILEO.txt'

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
