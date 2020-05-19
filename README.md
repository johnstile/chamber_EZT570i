# chamber_EZT570i
[Cincinnati Sub-Zero (CSZ) EZT-570i](https://www.cszindustrial.com/Products.aspx) 
```.
Python API to control the environmental chamber by Cincinnati Sub-Zero (CSZ) EZT-570i
The environmental chamber has a RS-232 serial port on the back of the unit.
This assumes a Serial To Ethernet Adapter is attached to the RS-232 port

This can load and start a profile, and read and write individual registers
```

## Hardware:
```.
Environmental Chamber:
  Cincinnati Sub-Zero (CSZ) MCB Climate chambers EZT-570i 

Serial To Ethernet Adapter: 
  www.gridconnect.com
  Part Number: GC-BF-430
  https://www.gridconnect.com/products/industrial-serial-rs232-ethernet-rs485-converter-bf-430
  Listed price on that page: $62.50
  SETTING: Parity=Even, Baud Rate=9600, Keep connection alive
```

## Quick Start:
```.
For demo edit chamber_control.py
Set: comm_params with the IP of the Serial To Ethernet Adapter
Run. 
```


# File summery:
```
 EZT570i User Communication Reference Manual revA.pdf:
   Defines the API for Communication

 GALAXY.txt:
   Newer profile from a newer chamber (with 17 items per line)

 GALILEO.txt:
   Older profile from a older chamber (with 15 items per line)

 chamber_control.py:
   Most programs would create an instance of the top level class Chamber, found in this file.
   main() method demonstrates the functional convenience methods.  
   This class uses:
     chamber_commands.py to make modbus get/set requests 
     chamber_communication.py: to talk to modbus
     modbus_packets.py: to generate the packets

 chamber_commands.py:
   Mapps Chamber Control Registers to human readable values.
   For a given regiester there is a human readable string
   For a given registers there are allowed values and translation to human readable meaning.
   Functions named the same as the human readable string, are for constructing a getter call.
   Functions named the same as the human readable string, with prefix 'set_', are for setting value calls.

 chamber_communication.py:
   implement communication for read, write, and profile upload

 modbus_packets.py: 
   Classes represent ModBus Packets

 output.txt:
   sample output from running chamber_control.py as a program
```

