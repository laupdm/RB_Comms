import json
import sys
import serial
import glob
import time

def configure(filename,action):
    # Recoje la información del archivo de la configuración
    if not filename:
        filename = "config.json" # a no ser que le cambiemos el nombre del archivo, va a utilizar el que creamos

    try:
        with open( filename , action) as myfile:
            
            if action == 'r':
                data = myfile.read()
                cfg = json.loads(data)
            return cfg #parte del json que tiene la info

    except FileNotFoundError:   
        return None

def serial_ports():
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

if __name__ == "__main__":

    # filename = None
    # config = configure(filename,'r')
    

    # config['parameters']['rb_com'] = "COM167"

    # a_file = open("config.json", "w")
    # json.dump(config, a_file)

    # from serial.tools.list_ports import comports  # import serial module
    # comPorts = list(serial.tools.list_ports.comports()) 
    # ports = comPorts
    # port = ""
    # if len(ports) > 0:
    #     #TODO: find the name of the RockBlock that appears and automatize the process
    #     print("\nList number : PORT")
    #     for port in ports:
    #         print( "   ",ports.index(port), "      :" , port , "\n")
    #         print(port[1])
    #         print(port[2])

    #     #print("You can check RB port nº at: Administrador de dispositivos/Puertos COM y LPT \n")
    #     res = ""
    #     while True:
    #         try:
    #             res = int(input("Type the list number corresponding to RockBlock's port:"))

    #             if (ports[res] in ports):
    #                 print("Port ",ports[res]," selected.")
    #                 break
    #             print("ERROR: No port ", res ," found.")
    #         except Exception as e:
    #             print("ERROR:",e)
        
    #     port = ports[res]
    
    # while len(ports) == 0:
    #     print("Please connect the RockBlock...")
    #     time.sleep(15)
    #     comPorts = list(serial.tools.list_ports.comports()) 
    #     ports = comPorts
    #     port = ""

    # Make sure the user has connected the RB:
    # ports = list(comports()) 
    # rb_port = False

    # port = "COM13"
    
    # while (rb_port == False):
    #     ports = list(comports())

    #     while (len(ports) == 0):
    #         print("Please connect the RockBlock...")
    #         time.sleep(3)
    #         ports = list(serial.tools.list_ports.comports())
    #         print("\nList number : PORT")
    #         for port in ports:
    #             print( "   ", ports.index(port) , "      :" , port , "\n")

    #     for p in ports:

    #         if port in p:
    #             print(p)
    #             print(port)
                
    #             rb_port = True

    #         elif p[1].startswith("USB Serial Port"):
    #             print("USB Serial Port")
    #             print(p)
    #             rb_port = True
    #         elif p[2].startswith("USB VID:PID=0403:6001 SER=FTB"):
    #             print("USB VID:PID=0403:6001 SER=FTB")
    #             print(p)
    #             rb_port = True
            

    

    

    ports = list(comports()) 
    port = ""
            
    while len(ports) == 0:
        print("Please connect the RockBlock...")
        time.sleep(3)
        ports = list(comports())  
                
    if len(ports) > 0:
        print("\nList number : PORT")
        for port in ports:
            print( "   ",ports.index(port), "      :" , port , "\n")

            if port[2].startswith("USB VID:PID=0403:6001 SER=FTB"):
                print("USB VID:PID=0403:6001 SER=FTB")
                print(port)
                port_name = str(port[0])

    #     #print("You can check RB port nº at: Administrador de dispositivos/Puertos COM y LPT \n")
    #     res = ""
    #     while True:
    #         try:
    #             res = int(input("Type the list number corresponding to RockBlock's port:"))


    #             if (ports[res] in ports):
    #                 port = list(ports[res])
    #                 port_name = port[0]
    #                 port_description = port[1]
    #                 port_x = port[2]

    #                 print("Port", port_name ,"has been selected.")
    #                 break
    #             print("ERROR: No list number", res ," has been found.")
    #         except Exception as e:
    #             print("ERROR:",e)
        
    # port = list(ports[res])

    # port_name = port[0]
    print("Port:", port)
    print("Port name:", port_name)