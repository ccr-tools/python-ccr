.. CCR documentation master file, created by
   sphinx-quickstart on Thu Dec 31 21:32:10 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CCR Documentation
=================

.. automodule:: ccr

.. toctree::
   :maxdepth: 3


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
   :members:

Authentication
--------------

.. autoclass:: ccrauth.AuthFile
   :members:

.. autoclass:: ccrauth.AuthDB
   :members:

Custom Exceptions
-----------------

.. autoexception:: ccr.PackageNotFound
.. autoexception:: ccr.InvalidPackage
.. autoexception:: ccr.CCRWarning

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
