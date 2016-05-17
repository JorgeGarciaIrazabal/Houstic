from communication import Communication
from api import Api

a = Api()
a.read_config()

comm = Communication(a)
comm.connect_to_server('192.168.1.6', 7159)

comm.main_loop()
