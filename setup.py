import io
import os
from pathlib import Path
import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.dist import Distribution
from setuptools import Extension

NAME = "grapemask"
DESCRIPTION = "Instance and panoptic segmentation of grape clusters"
EMAIL = "nathanstrong@terroirai.com"
AUTHOR = "Nathan Strong"
REQUIRES_PYTHON = ">=3.8.0"
VERSION = "0.1.0"

cur_dir = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(cur_dir, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {"__version__": VERSION}


def get_ext_modules():
    ext_modules = []
    if "--platlib-patch" in sys.argv:
        if sys.platform.startswith("linux"):
            # Manylinux2010 requires a patch for platlib
            ext_modules = [Extension("_foo", ["stub.cc"])]
        sys.argv.remove("--platlib-patch")
    return ext_modules


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    packages=find_packages(),
    ext_modules=get_ext_modules(),
    install_requires=Path("requirements.txt").read_text().splitlines(),
    include_package_data=True,
    zip_safe=False,
    distclass=BinaryDistribution,
)
