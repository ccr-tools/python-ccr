python-ccr
==========

A simple python module for accessing and working with the Chakra Community Repository.

[![Build Status](https://travis-ci.org/ccr-tools/python-ccr.svg)](https://travis-ci.org/ccr-tools/python-ccr)
[![Coverage Status](https://coveralls.io/repos/ccr-tools/python-ccr/badge.png?branch=development)](https://coveralls.io/r/ccr-tools/python-ccr?branch=development)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/91af4e0a847247aaa5490e699ecfd6ea)](https://www.codacy.com/app/rshipp/python-ccr)

## Installation

If you want to use the KWallet authentication support, you will need to
install the Python 3 KDE bindings for your distro. Assuming you're on
Chakra, that means you'll want to run

    sudo pacman -S kdebindings-python3

Once the bindings have installed, or if you can do without them, just
run:

    sudo pip install -r requirements.txt
    sudo python setup.py install

## Contributing

This project follows the
[git-flow](http://nvie.com/posts/a-successful-git-branching-model/)
branching model. Please submit pull requests to the `development`
branch, not `master`.
