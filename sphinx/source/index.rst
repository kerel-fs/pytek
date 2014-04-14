
|version-badge| |license-badge|

=================================================================
PyTek Documentation
=================================================================

**PyTek** provides a python API for interacting with |tek| |oscopes| over a serial
interface. It currently supports some basic commands for the `~pytek.TDS3k` series of
|DPOs|, especially `capturing waveforms <pytek.TDS3k.get_waveform>`
and `screen shots <pytek.TDS3k.screenshot>` from the device.

.. note:: **Serial Port not Included**

    PyTek relies on a thirdparty serial port for communications, specifically
    one that matches the `pyserial`_ API. It is recommended that you simply use
    `pyserial`_ itself.


Getting Started
----------------

To get started, try the :doc:`README`, or for complete documentation, 
check out the :doc:`pytek` API documentation page.


Documentation Contents:
--------------------------

.. toctree::
   :maxdepth: 2

   README

   pytek
   util
   version

   LICENSE


Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Version
----------

|version-badge|

This documentation is for PyTek |release|.

Project Resources
------------------

* `PyTek project homepage (bitbucket) <https://bitbucket.org/bmearns/pytek>`_
* `PyTek on pypi <https://pypi.python.org/pypi/pytek>`_
* Online documentation:
    * `Read The Docs (.org) <http://pytek.readthedocs.org/>`_
    * `Python Hosted (.org) <http://pythonhosted.org/pytek/>`_


External References
---------------------

* `TDS3000, TDS3000B & TDS3000C Series Programmer Manual (Tektronix.com) <tds3k_prog_man_>`_


