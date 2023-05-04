"""Installation script for python"""

from setuptools import setup, find_packages
import os
import re

PACKAGE = "movespad"

def get_version():
    VERSIONFILE  = os.path.join("src", PACKAGE, "__init__.py")
    initfile_lines = open(VERSIONFILE, "rt").readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=PACKAGE,
    version=get_version(),
    description="SPAD simulation for Move-X",
    author="Andrea Sala",
    author_email="andrea.sala@movesolutions.it",
    url="https://github.com/AndSalaMove/movespad",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={'console_scripts': ['spad-run = movespad.gui:gui',
                                        ]},
    classifiers=[
        "Progeamming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ],
    install_requires = [
        "numpy",
        "matplotlib",
        "PySimpleGUI",
        "pvlib",
        "scipy"
    ],
    python_requires = ">=3.8",
    long_description=long_description,
    long_description_content_type = "text/markdown",
)
