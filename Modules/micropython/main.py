import sys
from communication import CommunicationHandler
from machine import Pin, unique_id, reset
import network


def resetting(p):
    print('pin change', p)
    reset()


button = Pin(4, Pin.IN)
button.irq(trigger=Pin.IRQ_RISING, handler=resetting)

sta_if = network.WLAN(network.STA_IF)
print("waiting wifi connection...")
while not sta_if.isconnected():
    pass

house_ip = '192.168.1.29' if len(sys.argv) < 2 else sys.argv[1]
port = 7160

TYPE = "CALDERA"
module_id = "-".join([str(i) for i in unique_id()])
print(module_id)
comm = CommunicationHandler(module_id, TYPE)
comm.connect_to_server(house_ip, port)

comm.main_loop()
