import serial
from serial.tools.list_ports import comports
import time
import sys
import json
import glob
from adafruit_rockblock import *
class RockBlocks:
    def __init__(self, filename = None):
        # RockBlock configuration and connection:
        self.config = self.configure(filename)
               
        config = self.config['parameters']

        self.baudrate = config["rb_baud"]
        self.port = config["rb_com"]
        self.sn = config["gcs_sn"]

        self.ensure_connection()
            
    def check_connection(self, rb):

        resp = rb._uart_xfer("+CSQ")

        if resp[-1].strip().decode() == "OK":
            status = int(resp[1].strip().decode().split(":")[1])

        else:
            quality = False

        signal_strength = status

        print("Signal strength:", signal_strength)

        if signal_strength >= 1:
            quality = True

        else:
            quality = False

        return quality

    def ensure_connection(self):
        print("Ensuring connection...")
        baudrate = self.baudrate
        port1 = self.port

        # Make sure the user has connected the RB:
        ports = list(comports()) 
        rb_port = False

        for p in ports:
            
            if port1 in p:
                rb_port = True
            else:
                rb_port = False

        # RB Port correct 
        if (rb_port == True):
            uart = serial.Serial(port1, baudrate)
            rb = RockBlock(uart)
            print("RockBlock connected!")
            return rb

        # RB Port not correct 
        elif (rb_port == False):
            port2 = (self.select_RB_port())

            # RB Port correction in config 
            self.config['parameters']['rb_com'] = port2

            a_file = open("config.json", "w")
            json.dump(self.config, a_file)

            uart = serial.Serial(port2, baudrate)
            rb = RockBlock(uart)
            print("RockBlock connected!")
            return rb

    def configure(self, filename):
        
        if not filename:
            filename = "config.json" 

        try:
            with open(filename, "r") as myfile:
                data = myfile.read()
                cfg = json.loads(data)
                return cfg 

        except FileNotFoundError:
            return None

    def select_RB_port(self):
        ports = list(comports()) 
        port_name = ""
            
        while len(ports) == 0:
            print("Please connect the RockBlock...")
            time.sleep(3)
            ports = list(comports())  
                    
        if len(ports) > 0:
            print("\nPORT number : PORT name")
            for port in ports:
                print( "   ",ports.index(port)+1, "      :" , port , "\n")

                if port[2].startswith("USB VID:PID=0403:6001 SER=FTB"):
                    
                    port_name = str(port[0])
                    
        # if len(ports) > 0:
        #     print("\nList number : PORT")
        #     for port in ports:
        #         print( "   ",ports.index(port), "      :" , port , "\n")

        #     #print("You can check RB port nº at: Administrador de dispositivos/Puertos COM y LPT \n")
        #     res = ""
        #     while True:
        #         try:
        #             res = int(input("Type the list number corresponding to RockBlock's port:"))

        #             if (ports[res] in ports):
        #                 port = list(ports[res])
        #                 port_name = port[0]
        #                 print("Port", port_name ,"has been selected.")
        #                 break
        #             print("ERROR: No list number", res ," has been found.")
        #         except Exception as e:
        #             print("ERROR:",e)
            
        # port = list(ports[res])
        # port_name = port[0]
        # print("Port:", port)
        # print("Port name:", port_name)
        return port_name
    
    @property
    def get_time(self):
        rb = self.connect_rockblock()
        resp = rb._uart_xfer("+CCLK?")  # 20/09/26,12:07:13

        if resp[-1].strip().decode() == "OK":
            status = tuple(resp[1].decode().split(","))
            date = (status[0].split(":"))[1]

            year = str(int(date.split("/")[0]) + 2000)
            month = date.split("/")[1]
            day = date.split("/")[2]

            time = status[1]
            hour = int(time.split(":")[0]) + 2  # UTC +2 for Spain
            min = time.split(":")[1]
            # sec = time.split(":")[2]

            timestamp = str(year) + "_" + str(month) + "_" + \
                str(day) + "-" + str(hour) + "_" + str(min)

            return timestamp

    def receive_msg(self):
        pass
    
    def send_msg(self):

        pass
    
    def codification(self,msg):
        # [drone_id, status, type, homeLat, homeLon, heading, distance(km), *width(km)]
        # status = 2 MISSION
        # TYPE -> 0: Rectangle (* parameters are needed)
        # TYPE -> 1: Zigzag (* parameters are needed)
        # TYPE -> 2: Straight
        pass

    def decodification(self,msg):
        # [drone_id, status, type, homeLat, homeLon, heading, distance(km), *width(km)]
        # status = 2 MISSION
        # TYPE -> 0: Rectangle (* parameters are needed)
        # TYPE -> 1: Zigzag (* parameters are needed)
        # TYPE -> 2: Straight
        pass

if __name__ == "__main__":
    
    r = RockBlocks()
