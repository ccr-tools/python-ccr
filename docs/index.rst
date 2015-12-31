.. CCR documentation master file, created by
   sphinx-quickstart on Thu Dec 31 21:32:10 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CCR
===

Contents:

.. toctree::
   :maxdepth: 2


Description
-----------

``ccr`` is a Python library for interacting with the Chakra Community
Repository, or CCR.

Functions
---------

.. autofunction:: ccr.search
.. autofunction:: ccr.info
.. autofunction:: ccr.msearch
.. autofunction:: ccr.list_orphans
.. autofunction:: ccr.getlatest
.. autofunction:: ccr.geturl
.. autofunction:: ccr.getpkgurl
.. autofunction:: ccr.getpkgbuild
.. autofunction:: ccr.getpkgbuildraw
.. autofunction:: ccr.getfileraw

Session Management
------------------

.. autoclass:: ccr.Session

Custom Exceptions
-----------------

.. autoclass:: ccr.PackageNotFound
.. autoclass:: ccr.InvalidPackage
.. autoclass:: ccr.CCRWarning

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
