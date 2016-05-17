import subprocess
import os

port = 'COM4'
baudrate = '115200'
firmware = os.path.join(os.pardir, "firmware", "esp8266-2016-05-03-v1.8.bin")


if not os.path.exists(firmware):
    raise Exception("Firmware not found")

esptool = 'C:\\Python27\\Scripts\\esptool.py'
python = 'C:\\Python27\\python.exe'


subprocess.call([python, esptool, "--port", port, "erase_flash"])
#normal
# subprocess.call([python, esptool,  "--port", port, "--baud", baudrate, "write_flash", "--flash_size=8m", "0", firmware])
#mcu
subprocess.call([python, esptool,  "--port", port, "--baud", baudrate, "write_flash", "--flash_size=8m", "-fm", "dio", "0", firmware])
