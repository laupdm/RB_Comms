import serial
import sys
import glob
from adafruit_rockblock import *
class RockBlock:

    def __init__(self):
        # via USB cable:
        baudrate = 19200
        port = self.select_RB_port()

        uart = serial.Serial(port, baudrate) # port = "/dev/ttyUSB0"

        self.rb = RockBlock(uart)

        self.drone_rb_sn = self.rb_serial_num[1]
        self.gcs_rb_sn = self.rb_serial_num[0]

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def select_RB_port(self):
        ports = self.serial_ports()

        if len(ports) > 1:
            #TODO: find the name of the RockBlock that appears and automatize the process
            for port in ports:
                print( ports.index(port) + ":" + port)

            res = input("Type the port number of the RockBlock:")

            while type(res)!= int or res > len(ports):
                print("ERROR: No port "+ res +" found.")
                res = input ("Type port number again:")
            
            port = ports[res]

        elif len(ports) == 1:
            port = ports[1]

        return port

    def send_code(self):
        #TODO: define ERROR codes 
    
    def receive_code(self):
        #TODO: decodification of codes 
    
    def rb_serial_num(self):

        sn_drone = input("Type the drone's RockBlock serial number:")
        sure = input("Drone's RockBlock serial number "+ sn_drone + " is correct? (Y/N):")

        while sure !="Y" or sure!="y":
            sn_drone = input("Type the drone's RockBlock serial number:")
            sure = input("Drone's RockBlock serial number "+ sn_drone + " is correct? (Y/N):")

        sn_gcs = input("Type the computer's RockBlock serial number:")
        sure = input("GCS's RockBlock serial number "+ sn_gcs + " is correct? (Y/N):")

        while sure !="Y" or sure!="y":
            sn_gcs = input("Type the drone's RockBlock serial number:")
            sure = input("Drone's RockBlock serial number "+ sn_drone + " is correct? (Y/N):")

        sn = [sn_gcs,sn_drone]
        return sn
