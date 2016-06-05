import subprocess
import os

port = 'COM4'
baudrate = '115200'
firmware = os.path.join(os.pardir, "firmware", "esp8266-2016-06-03-v1.8.1.bin")


if not os.path.exists(firmware):
    raise Exception("Firmware not found")

esptool = 'C:\\Python27\\Scripts\\esptool.py'
python = 'C:\\Python27\\python.exe'


subprocess.call([python, esptool, "--port", port, "erase_flash"])
#normal
# subprocess.call([python, esptool,  "--port", port, "--baud", baudrate, "write_flash", "--flash_size=8m", "0", firmware])
#mcu
subprocess.call([python, esptool,  "--port", port, "--baud", baudrate, "write_flash", "--flash_size=8m", "-fm", "dio", "0", firmware])



# to connect to wifi
# import network
# wlan = network.WLAN(network.STA_IF) # create station interface
# wlan.active(True)       # activate the interface
# wlan.scan()             # scan for access points
# wlan.isconnected()      # check if the station is connected to an AP
# wlan.connect('JAZZTEL_9A3B', 'FA020156120757200985040689')
