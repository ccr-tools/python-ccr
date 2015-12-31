CCR
===

.. image:: https://travis-ci.org/ccr-tools/python-ccr.svg
   :target: https://travis-ci.org/ccr-tools/python-ccr
   :alt: Build Status
.. image:: https://coveralls.io/repos/ccr-tools/python-ccr/badge.png?branch=development
   :target: https://coveralls.io/r/ccr-tools/python-ccr?branch=development
   :alt: Coverage
.. image:: https://api.codacy.com/project/badge/grade/91af4e0a847247aaa5490e699ecfd6ea
   :target: https://www.codacy.com/app/rshipp/python-ccr
   :alt: Codacy Grade

A simple python module for accessing and working with the `Chakra Community
Repository`_.

Installation
------------

If you want to use the KWallet authentication support, you will need to
install the Python 3 KDE bindings for your distro. Assuming you're on
Chakra, that means you'll want to run::

    sudo pacman -S kdebindings-python3

Once the bindings have installed, or if you can do without them, just run::

    sudo pip install -r requirements.txt
    sudo python setup.py install

Contributing
------------

This project follows the git-flow_ branching model. Please submit pull
requests to the *development* branch, not *master*.

.. _Chakra_Community_Repository: https://chakraos.org/ccr/
.. _git-flow: http://nvie.com/posts/a-successful-git-branching-model/
