import inspect
import os
import socket
import sys


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    return s.getsockname()[0]


def get_module_path(frame=None):
    encoding = sys.getfilesystemencoding()
    encoding = encoding if encoding is not None else 'utf-8'
    frame = frame if frame is not None else inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    file_name = info.filename
    return os.path.dirname(os.path.abspath(file_name))


def set_program_path(path):
    os.chdir(path)
    return os.getcwd()
