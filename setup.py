import os
from setuptools import setup
import ConfigParser


def load_metadata(ini_file):
    config = ConfigParser.ConfigParser()
    read_files = config.read(ini_file)
    if len(read_files) == 0:
        raise Exception("Failed to read %s" % ini_file)
    meta = {}
    for item in config.options("meta"):
        meta[item] = config.get("meta", item)
    return meta

METADATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'django_ini_settings/METADATA')
META = load_metadata(METADATA_PATH)


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except:
        return ""

setup(
    name=META["name"],
    version=META["version"],
    author="Sebastian Phelps",
    author_email="sebastian.phelps@gmail.com",
    description=META["description"],
    packages=['django_ini_settings'],
    keywords=META["keywords"],
    include_package_data=True,
    package_data={'django_ini_settings': ['METADATA', ]},
    long_description=read('README.md'),
)