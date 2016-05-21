from communication import CommunicationHandler
from machine import Pin, unique_id
import network

sta_if = network.WLAN(network.STA_IF)
print("waiting wifi connection...")
while not sta_if.isconnected():
    pass

TYPE = "CALDERA"
module_id = "-".join([str(i) for i in unique_id()])
print(module_id)
comm = CommunicationHandler(module_id, TYPE)
comm.connect_to_server('192.168.1.6', 7159)

comm.main_loop()