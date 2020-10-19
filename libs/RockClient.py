import serial
import serial.tools.list_ports 
import time
import sys
import json
import glob
from adafruit_rockblock import *
class RockBlocks:

    def __init__(self, filename = None):

        self.config = self.configure(filename)
        # Make sure the user has connected the RB:
        ports = list(serial.tools.list_ports.comports())                         
        while len(ports) == 0:
            print("Please connect the RockBlock...")
            time.sleep(3)
            ports = list(serial.tools.list_ports.comports()) 
        
        # Ask the user if there has been any change on the RB devices
        while True:
            try:
                res = str(input("Has any of the RockBlock devices changed? (Y/N):"))

                if (res == "Y") or (res == "y") or (res == "N") or (res == "n"):
                    break
                print("ERROR: Response has to be of type Y/N.")
            except Exception as e:
                print(e)
                
        if (res == "Y") or (res == "y"):

            baudrate = self.config['parameters']['rb_baud']
            port = self.select_RB_port()

            uart = serial.Serial(port, baudrate) # port = "/dev/ttyUSB0"

            self.rb = RockBlock(uart)
            print("RockBlock connected!")
            list_sn = self.rb_serial_num()

            self.drone_sn = list_sn[1]
            self.gcs_sn = list_sn[0]

            # Change settings for the next time:
            self.config['parameters']['drone_sn'] = self.drone_sn
            self.config['parameters']['gcs_sn'] = self.gcs_sn
            self.config['parameters']['rb_com'] = port
            a_file = open("config.json", "w")
            json.dump(self.config, a_file)
            print("RockBlock settings changed for the next time")

        elif (res == "N") or (res == "n"):

            config = self.config['parameters']

            baudrate = config["rb_baud"]
            port = config["rb_com"]
            
            uart = serial.Serial(port, baudrate)

            self.drone_sn = config['drone_sn']
            self.gcs_sn = config['gcs_sn']
            

            self.rb = RockBlock(uart)
            print("RockBlock connected!")
                   
    def configure(self, filename):
        # Recoje la información del archivo de la configuración
        if not filename:
            filename = "config.json" # a no ser que le cambiemos el nombre del archivo, va a utilizar el que creamos

        try:
            with open(filename, "r") as myfile:
                data = myfile.read()
                cfg = json.loads(data)
                return cfg 

        except FileNotFoundError:
            return None

    def select_RB_port(self):
        comPorts = list(serial.tools.list_ports.comports()) 
        ports = comPorts
        port = ""
                
        while len(ports) == 0:
            print("Please connect the RockBlock...")
            time.sleep(3)
            ports = list(serial.tools.list_ports.comports()) 
        
            
        if len(ports) > 0:
            #TODO: find the name of the RockBlock that appears and automatize the process
            print("\nList number : PORT")
            for port in ports:
                print( "   ",ports.index(port), "      :" , port , "\n")

            #print("You can check RB port nº at: Administrador de dispositivos/Puertos COM y LPT \n")
            res = ""
            while True:
                try:
                    res = int(input("Type the list number corresponding to RockBlock's port:"))

                    if (ports[res] in ports):
                        port = list(ports[res])
                        port_name = port[0]
                        print("Port", port_name ,"has been selected.")
                        break
                    print("ERROR: No list number", res ," has been found.")
                except Exception as e:
                    print("ERROR:",e)
            
        port = list(ports[res])
        port_name = port[0]
        # print("Port:", port)
        # print("Port name:", port_name)

        return port_name

    def send_code(self):
        #TODO: define ERROR codes 
        pass
    
    def receive_code(self):
        #TODO: decodification of codes 
        pass

    def rb_serial_num(self):

        # Ask the user the serial number of the drone's RockBlock 
        while True:
            try:
                res = int(input("Type the drone's RockBlock serial number:"))
                sn_drone = res

                if (len(str(abs(res))) == 6):

                    while True:
                        try:
                            res2 = input("Drone's RockBlock serial number"+ sn_drone + "is correct? (Y/N):")

                            if (res2 =="y" or res2 == "Y"):
                                break
                            sn_drone = int(input("Type the drone's RockBlock serial number:"))
                        except Exception as e:
                            print(e)
                                
                    break

                print("ERROR: RockBlock serial numbers have always 6 digits")
            except Exception as e:
                print(e)
        
      






        while sure !="Y" or sure!="y":
            sn_drone = input("Type the drone's RockBlock serial number:")
            sure = input("Drone's RockBlock serial number "+ sn_drone + " is correct? (Y/N):")

        sn_gcs = input("Type the GCS's RockBlock serial number:")
        sure = input("GCS's RockBlock serial number "+ sn_gcs + " is correct? (Y/N):")

        while sure !="Y" or sure!="y":
            sn_gcs = input("Type the GCS's RockBlock serial number:")
            sure = input("GCS's RockBlock serial number "+ sn_drone + " is correct? (Y/N):")

        sn = [sn_gcs,sn_drone]
        return sn

if __name__ == "__main__":
    
    r = RockBlocks()
