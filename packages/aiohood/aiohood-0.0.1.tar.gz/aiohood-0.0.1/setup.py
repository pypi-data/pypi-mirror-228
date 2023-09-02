from setuptools import setup
from setuptools.command.install import install

class PhoneHome(install):
    def run(self):
        print("Hello world!")

setup(name='aiohood',
      version='0.0.1',
      cmdclass={ "install": PhoneHome },
      author="zzz@example.com",
      author_email="zzz@example.com",
      url="https://example.com"
      )
