import subprocess
import time




def Ping__(Command_input):

 subprocess.run(["ping"])

def Net_map(Command_input):
  subprocess.run(["nmap", "-sL"])

def scan_for_open_ports(Command_input):
  subprocess.run(["nmap", "-p-",])

def find_info(Command_input):
    process = subprocess.Popen(
        ["Fern", "Geo", Command_input ],
        stdin=subprocess.PIPE,
        text=True
    )

    time.sleep(2)

    process.communicate(Command_input)
