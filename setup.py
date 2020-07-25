from setuptools import setup

setup(
    name='qtile-widget-unitstatus',
    packages=['unitstatus'],
    version='0.1.0',
    description='A widget to show status of systemd unit',
    author='elParaguayo',
    url='https://github.com/elparaguayo/qtile-widget-unitstatus',
    license='MIT',
    install_requires=['qtile>0.14.2', 'pydbus']
)
