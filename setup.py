from distutils.core import setup

setup(
    name='Houstic',
    version='0.1',
    packages=[],
    url='https://github.com/JorgeGarciaIrazabal/Houstic',
    license='MIT',
    author='jorgeubuntu',
    author_email='jorge.girazabal@gmail.com',
    description='Domotic project using raspberry-pi and esp8266',
    install_requires= ["wshubsapi==0.6.5a2", "glob2", "tornado", "mongoengine"]
)
