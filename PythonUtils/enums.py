from enum import unique, IntEnum


@unique
class ClientType(IntEnum):
    HOUSE = 1
    MOBILE = 2


@unique
class ComponentType(IntEnum):
    DIGITAL_IN = 0
    DIGITAL_OUT = 1
    ANALOG_IN = 2
    ANALOG_OUT = 3
    I2C = 4
    SPI = 5
    DHT11 = 6
    DHT22 = 7
