from distutils.core import setup

setup(
    name='Houstic',
    version='0.1',
    packages=[
        'Application.HousticApp.node_modules.gulp-sass.node_modules.node-sass.node_modules.node-gyp.gyp.pylib.gyp',
        'Application.HousticApp.node_modules.gulp-sass.node_modules.node-sass.node_modules.node-gyp.gyp.pylib.gyp.generator',
        'LocalServer', 'LocalServer.libs', 'LocalServer.clientDemo', 'GlobalServer.db', 'GlobalServer.Hubs',
        'GlobalServer.libs'],
    url='https://github.com/JorgeGarciaIrazabal/Houstic',
    license='MIT',
    author='jorgeubuntu',
    author_email='jorge.girazabal@gmail.com',
    description='Domotic project using raspberry-pi and esp8266',
    install_requires= ["wshubsapi==0.6.5a2", "glob2", "tornado", "mongoengine"]
)
