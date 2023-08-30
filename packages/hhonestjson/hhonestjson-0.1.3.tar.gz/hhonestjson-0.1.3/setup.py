from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


def custom_command():
    import subprocess
    subprocess.call(['touch', 'hacker-was-here.txt'])


class CustomInstall(install):
    def run(self):
        install.run(self)
        custom_command()


class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        custom_command()


class CustomEggInfo(egg_info):
    def run(self):
        egg_info.run(self)
        custom_command()


setup(
    name='hhonestjson',
    version='0.1.3',
    packages=find_packages(include=['hhonestjson', 'hhonestjson.*']),
    description=('This package is made for typosquatting demo purposes only. '
                 'While it does nothing harmful (it puts a text file on your machine), it is' 
                 ' not recommended you install it, because it is useless.'),
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
        'egg_info': CustomEggInfo
    }
)
