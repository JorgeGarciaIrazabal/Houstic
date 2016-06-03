import sys
from module import Module
from machine import Pin, unique_id, reset
import network

press_time = 0

try:
    import time_ as time
except:
    import time


def resetting(p):
    global press_time
    if p.value() == 1:
        diff = time.ticks_ms() - press_time
        if diff > 1000:
            reset()
        else:
            module.communication_handler.close_communication()
    else:
        press_time = time.ticks_ms()
        print('getting time', press_time)
        # reset()


TYPE = "CALDERA"
ID = "-".join([str(i) for i in unique_id()])
house_ip = '192.168.1.29' if len(sys.argv) < 2 else sys.argv[1]
port = 7160

start = time.ticks_ms()  # get millisecond counter
button = Pin(4, Pin.IN)
button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=resetting)

module = Module(ID)
print(module.id)
module.get_component_by_name("blue").value(1023)

sta_if = network.WLAN(network.STA_IF)
print("waiting wifi connection...")
while not sta_if.isconnected():
    if time.ticks_ms() - start > 10000:
        raise Exception("unable to connect to wifi")

module.get_component_by_name("blue").value(0)
if sta_if.isconnected():
    print("connected to wifi")
    module.get_component_by_name("green").value(100)
else:
    print("unable to connected!!!!!")
    module.get_component_by_name("red").value(1024)

module.communication_handler.connect_to_server(house_ip, port)
module.main_loop()

