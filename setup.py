from setuptools import setup, find_packages

setup(
    name='Houstic',
    version='0.1',
    packages=find_packages(exclude=()),
    url='https://github.com/JorgeGarciaIrazabal/Houstic',
    license='MIT',
    author='jorge',
    author_email='jorge.girazabal@gmail.com',
    description='Domotic project using raspberry-pi and esp8266',
    install_requires=["wshubsapi>=0.7.0", "glob2", "tornado", "mongoengine", 'xmlrunner']
)
