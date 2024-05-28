import serial.tools.list_ports
import serial
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print (p.serial_number)
    if "Arduino" in p.description:
        print ("This is an Arduino!")