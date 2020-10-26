import sys
from RockClient import *

if __name__ == "__main__":
    
    r = RockBlocks()    

    while True:

        message = r.get_message()
        print("Received message:", message)

        if not message is None:  # Si ha algun msg
            print("Processing messages...")
            r.process_message(message)
        
        sender = r.check_sender()

        if sender:
            # ASK user what message wants to send:

            while(True):

                res = str(input("Type the message you want to send:"))

                try:
                    if( len(res) < 111 ):
                        print("Apparently correct typed message.")
                        msg_text = res
                        r.send_msg(msg_text)
                        break

                    print("ERROR: text length is ", len(res) ," bytes and should be 111 bytes maximum.\n")
                    print("Try to erase", ( len(res)-111 ), "bytes from your text")

                except Exception as e:
                    print("ERROR:",e)