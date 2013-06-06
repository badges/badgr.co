from setuptools import setup, find_packages


def get_version():
    try:
        fp = open('version.txt')
        return fp.read().strip()
    except OSError:
        return 'n/a'


setup( name='badgr.co'
     , version=get_version()
     , packages=find_packages()
      )
