import os
import subprocess
import glob
from os.path import join

files = glob.glob(join(os.pardir, '*.py'))
files = filter(lambda x: "__" not in x, files)
web_cli = join(os.pardir, 'webrepl', 'webrepl_cli.py')

print os.path.exists(web_cli)
print(files, web_cli)
print os.path.basename(files[0])

for f in files:
    f_name = os.path.basename(f)
    subprocess.call(['python', web_cli, f, '192.168.1.138:/' + f_name])
