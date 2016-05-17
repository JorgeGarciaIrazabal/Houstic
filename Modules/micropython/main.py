from communication import Communication
from api import Api
from machine import Pin, unique_id

TYPE = "CALDERA"

a = Api()
a.read_config()

comm = Communication(a, unique_id(), TYPE)
comm.connect_to_server('192.168.1.6', 7159)

comm.main_loop()


# pins = [Pin(i, Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]
#
# for pin in pins:
#     print(pin.value())