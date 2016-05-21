STA_IF = 0

class WLAN:
    def __init__(self, type_):
        self.is_active = False
        self.type = type_

    def active(self, value):
        self.is_active = value
        return self.is_active

    def connect(self, essid, password):
        pass

    def isconnected(self):
        return True

