# chamber_EZT570i
Python API to control EZT570i environmental chamber


# File summery:
```
 EZT570i User Communication Reference Manual revA.pdf:
   Communication Reference

 GALAXY.txt:
   Newer profile with 17 items per line

 GALILEO.txt:
   Older profile with 15 items per line

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

