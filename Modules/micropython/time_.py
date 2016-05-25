from datetime import datetime


def ticks_ms():
    dt = datetime.now() - datetime(1970, 1, 1)
    return (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0

