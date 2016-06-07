class DHT:
    def __init__(self, pin):
        self.pin = pin

    def measure(self):
        pass

    def temperature(self):
        import random
        return random.uniform(-10, 50)

    def humidity(self):
        import random
        return random.uniform(0, 2000)


class DHT22(DHT):
    pass


class DHT11(DHT):
    pass
