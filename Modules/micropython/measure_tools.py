import os


def read(pin, times):
    return (pin.read() for i in range(times))


def safe_in_file(data, f='data.txt'):
    os.remove(f)
    with open(f, 'a') as f:
        for i in data:
            f.write(str(i) + ",")

