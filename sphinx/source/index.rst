.. PyTek documentation master file, created by
   sphinx-quickstart on Tue Apr 08 10:01:17 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


PyTek Documentation
=================================

:mod:`pytek` is a module for interacting with Tektronix oscilloscopes over a serial
interface. It currently supports some basic commands for the TDS3xxx series of
:abbr:`DSO's (Digital Phosphor Oscilloscopes)`, especially capturing waveforms
and screen shots from the device.


To get started, check out the documentation for the :doc:`pytek`.

.. note:: Serial Port Communications

    :mod:`pytek` relies on a thirdparty serial port for communications, specifically
    one that matches the `pyserial`_ API. It is recommended that you simply use
    `pyserial` itself.



External References
---------------------

* `TDS3000, TDS3000B & TDS3000C Series Programmer Manual (Tektronix.com) <http://www.tek.com/oscilloscope/tds3014b-manual/tds3000-tds3000b-tds3000c-series>`_


Contents:
===============

.. toctree::
   :maxdepth: 2

   pytek


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

