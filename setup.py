from setuptools import find_packages, setup
from ccr import __version__


setup(name = 'ccr',
      packages = find_packages(),
      version = __version__,
      author = 'ccr-tools',
      # FIXME create a valid ccr-tools support email
      author_email = 'ccr-tools@chakra-project.org',
      url = 'http://github.com/ccr-tools/python-ccr/',
      description = 'Library for accessing and working with the CCR.',
      long_description = open('README.md').read(),
      classifiers = ["Programming Language :: Python",
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
