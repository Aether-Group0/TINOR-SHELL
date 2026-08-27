from Utils.__Net_Util__ import Ping__, Net_map, scan_for_open_ports,find_info
from Utils.__Web_Util__ import Lookup
from Utils.__Notification_Util__ import Error_Notification
from Utils.__LANC_UTIL__ import send_handling, Startff
from Utils.__WANC_UTIL__ import send_handling_W, Startff_W
from Utils.SF_Source.__Main__ import start
from Utils.__ssh_Util__ import START_SERVER, Messaging_system
from Utils.___Find_info__.__GEO__ import find_info
from Utils.__FINDI_Util__ import geo
import subprocess
import os




def Run_find_info(Command_input):
    try:
        geo(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification
        return False
    
def Run_SSH_Client(Command_input):
    try:
        Messaging_system(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification
        return False

def Run_SSH_Server(Command_input):
    try:
        START_SERVER(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification
        return False

def Run_Social_Finder():
    try:
        start()
        return True
    except subprocess.CalledProcessError:
        Error_Notification
        return False


def Run_WANC_Server(Command_input):
    try:
        Startff_W(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification
        return False

def Run_WANC_Client(Command_input):
    try:
        send_handling_W(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification()
        return False

def Run_LANC_Server(Command_input):
    try:
        Startff(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification
        return False

def Run_LANC_Client(Command_input):
    try:
        send_handling(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification()
        return False

def Run_Ping(Command_input):
    try:
        Ping__(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification()
        return False

def Run_lookup(Command_input):
    try:
        Lookup(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification()
        return False

def Run_Command(Command_input):
    try:
        subprocess.run(Command_input,check = True, shell=True)
        return True
    except subprocess.CalledProcessError:
        Error_Notification()
        return False

def Run_scan_for_open_ports(Command_input):
    try:
        scan_for_open_ports(Command_input)
        return True
    except subprocess.CalledProcessError:
        Error_Notification()
        return False



def clear_screen():
    os.system("cls")

def main_name():
  print(r"""
  ████████╗██╗███╗   ██╗ ██████╗ ██████╗
  ╚══██╔══╝██║████╗  ██║██╔═══██╗██╔══██╗
     ██║   ██║██╔██╗ ██║██║   ██║██████╔╝
     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗
     ██║   ██║██║ ╚████║╚██████╔╝██║  ██║
     ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝

  ███████╗██╗  ██╗███████╗██╗     ██╗
  ██╔════╝██║  ██║██╔════╝██║     ██║
  ███████╗███████║█████╗  ██║     ██║
  ╚════██║██╔══██║██╔══╝  ██║     ██║
  ███████║██║  ██║███████╗███████╗███████╗
  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
              Tinor Shell.
        To replace plain old cmd.
  """)

def main_process():
    
    while True:\
    
        Command_input = input("\n> ").strip()

        if Command_input.lower() == "ping":
            Run_Ping(Command_input)

        elif "SSH -c" in Command_input:
            Run_SSH_Client(Command_input)

        elif "SSH -s" in Command_input:
            Run_SSH_Server(Command_input)

        elif "SF -s" in Command_input:
            Run_Social_Finder()

        elif "nm" in Command_input:
            Net_map(Command_input)

        elif "LANC -c" in Command_input:
            Run_LANC_Client(Command_input)

        elif "LANC -s" in Command_input:
            Run_LANC_Server(Command_input)

        elif "WAN -c" in Command_input:
            Run_WANC_Client(Command_input)

        elif "WAN -s" in Command_input:
            Run_WANC_Server(Command_input)

        elif "sop" in Command_input:
            Run_scan_for_open_ports(Command_input)

        elif "lp" in Command_input.split():
            Run_lookup(Command_input)

        elif "clear" in Command_input:
            clear_screen()
            main_name()

        elif "fi" in Command_input.split():
            Run_find_info(Command_input)

        elif "help" in Command_input:
            print(r""" Commands:
                  fi (in progress)
                  nm  (in progress)
                  sop (scan for open ports)
                  lp (lookup something)
                  clear (clear cache)
                  LANC -c (Starts LANC Client)
                  LANC -s (Starts LANC Server)
                  WAN -c  (Starts WAN Client)
                  WAN -s  (Starts WAN Server)
                  SF -s   (Starts Soicial Finder)
                  ssh -s  (Start SSH Server)
                  ssh -c  (Start SSH Client)
                  

                  """)


        elif Command_input.lower() == "exit":
            break

        elif Command_input == "":
            continue
        else:
            Run_Command(Command_input)
            

if __name__ == "__main__":
    clear_screen()
    main_name()
    main_process()