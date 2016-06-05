def reset():
    pass


def reset_cause():
    pass


def disable_irq():
    pass


def enable_irq(state: bool = True):
    pass


def freq():
    return 16000,


def idle():
    pass


def sleep():
    pass


def main(filename: str):
    pass


def rng():
    pass


def unique_id():
    return '12353AF234'


IDLE = 0
SLEEP = 0
DEEPSLEEP = 0
POWER_ON = 0
HARD_RESET = 0
WDT_RESET = 0
DEEPSLEEP_RESET = 0
SOFT_RESET = 0
WLAN_WAKE = 0
PIN_WAKE = 0
RTC_WAKE = 0


class ADC:
    def __init__(self, id_: int, bits=12):
        self.id = id_

    def read(self):
        import random
        return random.uniform(0, 1024)


class Pin:
    IN, OUT, PULL_UP, PULL_DOWN, OUT_PP, IRQ_FALLING, IRQ_RISING = range(7)

    def __init__(self, pin: int, mode=IN, value=None):
        self.value(value)
        self.pin = pin
        self.mode = mode

    def high(self):
        return

    def low(self):
        return

    def value(self, value=None):
        if value is None:
            return 1
        if value == 0:
            self.low()
        else:
            self.high()

    def irq(self, trigger, handler):
        pass


class Timer:
    ONE_SHOT, PERIODIC, PWM, A, B = range(5)

    def __init__(self, id_):
        self.id = id_

    def init(self, mode, width=16, period=None, callback=None):
        pass

    def deinit(self):
        pass

    def channel(self, timer, freq):
        class Channel:
            def __init__(self, timer_mode, frequency):
                self.frequency = frequency
                self.timer_mode = timer_mode

            def irq(self, handler, trigger, duty_cycle=5000):
                pass

            def freq(self, freq):
                self.frequency = freq
                return self.frequency

            def period(self, period):
                self.frequency = 1.0 / period
                return 1.0 / self.frequency

        return Channel(timer, freq)


class PWM:
    def __init__(self, pin):
        self._freq = 0
        self._duty = 0
        self._pin = pin

    def freq(self, frequency=None):
        self._freq = frequency if frequency is not None else self._freq
        return self._freq

    def duty(self, duty=None):
        self._duty = duty if duty is not None else self._duty
        return self._duty



