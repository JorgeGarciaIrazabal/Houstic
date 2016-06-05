import os
import subprocess
import glob
from os.path import join
import time


files = []

# files += glob.glob(join(os.pardir, 'module.init'))
# files += glob.glob(join(os.pardir, 'api.py'))

files = [join(os.pardir, f) for f in ['communication.py', 'main.py', 'api.py', 'module.init', 'module.py']]

files = filter(lambda x: "__" not in x, files)
web_cli = join(os.pardir, 'webrepl', 'webrepl_cli.py')

print(os.path.exists(web_cli))

for f in files:
    f_name = os.path.basename(f)
    subprocess.call(['python', web_cli, f, '192.168.1.145:/' + f_name])
    time.sleep(0.2)
