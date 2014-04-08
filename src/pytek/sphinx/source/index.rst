
PyTek Documentation
=================================

**PyTek** provides a python API for interacting with |tek| |oscopes| over a serial
interface. It currently supports some basic commands for the `~pytek.TDS3k` series of
|DPOs|, especially `capturing waveforms <pytek.TDS3k.get_waveform>`
and `screen shots <pytek.TDS3k.screenshot>` from the device.


**To get started**, check out the documentation for the :doc:`pytek`.

.. note:: Serial Port Communications

    PyTek relies on a thirdparty serial port for communications, specifically
    one that matches the `pyserial`_ API. It is recommended that you simply use
    `pyserial` itself.


Project Resources
------------------

* `Project Homepage (bitbucket) <https://bitbucket.org/bmearns/pytek>`_
* `On pypi <https://pypi.python.org/pypi/pytek>`_


External References
---------------------

* `TDS3000, TDS3000B & TDS3000C Series Programmer Manual (Tektronix.com) <tds3k_prog_man_>`_


Contents:
===============

.. toctree::
   :maxdepth: 4

   pytek


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

