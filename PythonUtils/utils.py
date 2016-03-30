import inspect
import os
import socket
import sys


def getLocalIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    return s.getsockname()[0]


def getModulePath(frame=None):
    encoding = sys.getfilesystemencoding()
    encoding = encoding if encoding is not None else 'utf-8'
    frame = frame if frame is not None else inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    fileName = info.filename
    return os.path.dirname(os.path.abspath(unicode(fileName, encoding)))


PROGRAM_PATH = os.path.dirname(sys.modules['__main__'].__file__)
os.chdir(PROGRAM_PATH)
