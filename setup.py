from setuptools import setup, find_packages


setup(
    name='Houstic',
    version='0.1',
    packages=find_packages(exclude=()),
    url='https://github.com/JorgeGarciaIrazabal/Houstic',
    license='MIT',
    author='jorgeubuntu',
    author_email='jorge.girazabal@gmail.com',
    description='Domotic project using raspberry-pi and esp8266',
    install_requires= ["wshubsapi>=0.6.6", "glob2", "tornado", "mongoengine", 'xmlrunner']
)
