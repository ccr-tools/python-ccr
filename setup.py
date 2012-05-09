from setuptools import setup
from ccr import __version__

long_description = open('README').read()

setup(name='ccr',
      version=__version__,
      py_modules=['ccr'],
      description='Library for accessing and working with the CCR.',
      author='ccr-tools',
      license='GPL3',
      url='http://github.com/ccr-tools/python-ccr/',
      long_description=long_description,
      platforms=['any'],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GPL3 License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Internet",
                   ]
     )
