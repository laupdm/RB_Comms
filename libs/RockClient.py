import serial
from serial.tools.list_ports import comports
import time
import sys
import json
import glob
import keyboard  # using module keyboard
from adafruit_rockblock import *
class RockBlocks:
    def __init__(self, filename = None):
        # RockBlock configuration and connection:
        self.config = self.configure(filename)
               
        config = self.config['parameters']

        self.baudrate = config["rb_baud"]
        self.port = config["rb_com"]
        self.gcs_sn = config["gcs_sn"]

        self.rb = self.ensure_connection()

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
    
    def get_time(self):
        rb = self.rb
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

    def send_msg(self, msg):
        text = self.codification(msg)

        if text is not None:
            data = text
            cc = self.check_connection(self.rb)
        
            previous = time.perf_counter()
            timer = 0

            while cc is not True:
                current = time.perf_counter()
                timer += current - previous
                previous = current

                print("Checking again...")
                cc = self.check_connection(self.rb)

                if timer > 15:
                    print('Im tired of checking signal')
                    break

            if cc is not False:
                print("Ready to send message!")

                # put data in outbound buffer
                self.rb.text_out = data

                # try a satellite Short Burst Data transfer
                print("Talking to satellite...")

                status = self.rb.satellite_transfer()
                print("Try num:", 1)
                print("Satellite status:", status)

                if( status[0] > 8 ):
                    print("The communication has failed")
                else:
                    print("\nDONE.")

        elif text is None:
            print("Try again...") 

        return None

    def get_message(self):
        rb = self.rb

        cc = self.check_connection(self.rb)
        
        previous = time.perf_counter()
        timer = 0

        while cc is not True:
            current = time.perf_counter()
            timer += current - previous
            previous = current

            print("Checking again...")
            cc = self.check_connection(self.rb)

            if timer > 15:
                print('Im tired of checking signal')
                break

        if cc is not False:
            # try a satellite Short Burst Data transfer
            print("Talking to satellite...")

            status = self.rb.satellite_transfer()
            print("Try num:", 1)
            print("Satellite status:", status)

            if( status[0] > 8 ):
                print("The communication has failed")
            else:
                # get the text
                message = rb.text_in
                print("\nMessage has arrived.")
        
        return message

    def process_message(self, msg):
        data = self.decodification(msg)
        print(json.dumps(data, indent=4))
        
        return None

    def codification(self, msg):
        print("Codification...")
        sn = str(self.gcs_sn)
        # Ensure Serial number is 7 bytes:
        if len(sn) < 7:
            zeros = 7 - len(sn)
            while zeros > 0:
                sn = "0" + sn
                zeros = zeros - 1
            
            # RB serial number correction in config: 
            self.config['parameters']['gcs_sn'] = sn
            a_file = open("config.json", "w")
            json.dump(self.config, a_file)

            # Write text message with correct prefix:
            prefix = "RB" + sn
            txt = prefix + msg     
            txt = str.encode(txt)   
            return txt

        elif len(sn) == 7:
            # Write text message with correct prefix:
            prefix = "RB" + sn
            txt = prefix + msg     
            txt = str.encode(txt)   
            return txt
            
        elif len(sn) > 7:
            print("ERROR: Serial number has more than 7 characters, check at config.json")      
            return None
    
    def decodification(self,msg):
        values = msg.split(",")
        landing = 0
        flying = 1        
        drone_id = values[0]
        status = int(values[1])
        lat = (int(values[2])) / 100000
        lon = (int(values[3])) / 100000
        alt = (int(values[4])) / 10
        flight_time = values[5]

        data = {}
        
        if status == landing: 
            data['Landing'] = []
            data['Landing'].append({'drone_id': drone_id,
                'status':"Landing",
                'latitude': lat,
                'longitude': lon,
                'altitude': alt,
                'mission time': flight_time})  

        elif status == flying:
            heading = values[6]
            mission_type = values[7]
            data['Flying'] = []
            data['Flying'].append({
                'drone_id': drone_id,
                'status':"Flying",
                'latitude': lat,
                'longitude': lon,
                'altitude': alt,
                'mission time': flight_time,
                'heading': heading,
                'mission': mission_type  
            } )

        return data
    
    def check_sender(self):
        # SENDER:
        sender = False
        print("Press S at Keyboard if you want to send a message.")
        time.sleep(2)       
        #used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('s'):  # if key 's' is pressed 
            
            print('Sender has been activated...\n')
            sender  = True

        else:
            sender = False

        return sender



        
        