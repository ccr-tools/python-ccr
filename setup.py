from setuptools import find_packages, setup
import os
from ccr import __version__

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = open(os.path.join(os.path.dirname(__file__),
            'requirements.txt')).read()
requires = requirements.strip().split('\n')

setup(
    name = 'ccr',
    packages = find_packages(),
    install_requires=requires,
    version = __version__,
    author = 'ccr-tools',
    # FIXME create a valid ccr-tools support email
    author_email = 'rshipp@chakralinux.org',
    url = 'http://github.com/ccr-tools/python-ccr/',
    description = 'Library for accessing and working with the CCR.',
    long_description = open('README.rst').read(),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv2 or any later version",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
    ],
    license = 'GPLv2 or any later version',
    platforms = ['any'],
    test_suite = 'tests'
)
