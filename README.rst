=================================================================
PyTek - Python API for Tektronix oscilloscopes' serial interface
=================================================================

.. # POST TITLE

.. _pyserial: http://pyserial.sourceforge.net/
.. _sphinx_rtd_theme: https://github.com/snide/sphinx_rtd_theme

**PyTek** provides a python API for interacting with Tektronix oscilloscopes over a serial
interface. It currently supports some basic commands for the TDS3000
series of Digital Phosphor Oscilloscopes, especially *capturing waveforms*
and *screen shots* from the device.

.. note:: **Serial Port not Included**

    PyTek relies on a thirdparty serial port for communications, specifically
    one that matches the `pyserial`_ API. It is recommended that you simply use
    `pyserial`_ itself.


.. contents:: **Page Contents**
    :local:
    :depth: 2
    :backlinks: top

tl;dr
---------------

What?
~~~~~~~~~~~~~~
A python package that gives you an API for interacting with supported Tektronix
oscilloscopes over a serial interace.

Install?
~~~~~~~~~~~~~

.. code:: bash

    $ pip install pytek

Or, from source:

.. code:: bash

    $ python setup.py install


Serial?
~~~~~~~~~~~~~

We don't provide a serial port implementation. We suggest, `pyserial`_:

.. code:: bash

    $ pip install pyserial

Examples?
~~~~~~~~~~~~~~~~~~

.. code:: pycon

    >>> from serial import Serial
    >>> from pytek import TDS3k
    >>>
    >>> port = Serial("COM1", 9600, timeout=1)
    >>> tds = TDS3k(port)
    >>>
    >>>
    >>> # Make the scope identify itself.
    ...
    >>> tds.identify()
    'TEKTRONIX,TDS 3034,0,CF:91.1CT FV:v2.11 TDS3GM:v1.00 TDS3FFT:v1.00 TDS3TRG:v1.00'
    >>>
    >>>
    >>>
    >>> # Capture waveform data
    ...
    >>> waveform = tds.get_waveform(start=100, stop=109)
    >>> waveform
    <generator object <genexpr> at 0x0238B8A0>
    >>
    >>> for x,y in waveform:
    ...     print x, y
    ...
    -0.0045 -0.16
    -0.004499 -0.04
    -0.004498 -0.04
    -0.004497 -0.12
    -0.004496 -0.12
    -0.004495 -0.08
    -0.004494 -0.12
    -0.004493 -0.16
    -0.004492 -0.2
    -0.004491 -0.08
    >>>
    >>> tds.x_units()
    's'
    >>> tds.y_units()
    'V'
    >>>
    >>>
    >>>
    >>> # Grab a screen shot (this will take a few minutes).
    ...
    >>> ofile = open("screenshot.tiff", "wb")
    >>> tds.screenshot(ofile, "tiff")
    >>>
    >>>
    >>>
    >>>
    >>> #Fin.
    ...
    >>> tds.close()
    >>>

Dependencies?
~~~~~~~~~~~~~~~~

You'll need a serial port interface. See the "`Serial?`_" section, above.

To build the sphinx docs from source (as is), you'll need the `sphinx_rtd_theme`_:

.. code:: bash

    $ pip install sphinx_rtd_theme


Extras?
~~~~~~~~~~~~

PyTek package includes the following extras (optional installs):

serial
    Adds `pyserial`_ package as a requirement, the recommended serial port interface.

docs
    Adds `sphinx_rtd_theme`_ package as a requirement, needed for building sphinx docs.


Docs?
~~~~~~~~

* `Read The Docs (.org) <http://pytek.readthedocs.org/>`_
* `Python Hosted (.org) <http://pythonhosted.org/pytek/>`_


Misc.
---------------


Contact Information
~~~~~~~~~~~~~~~~~~~~~~~~

This project is currently hosted on `bitbucket <https://bitbucket.org>`_, 
at `https://bitbucket.org/bmearns/pytek/ <https://bitbucket.org/bmearns/pytek/>`_.
The primary author is Brian Mearns: you can contact Brian through bitbucket at
`https://bitbucket.org/bmearns <https://bitbucket.org/bmearns>`_. 


Copyright and License
~~~~~~~~~~~~~~~~~~~~~~~~~~

\ ``PyTek``\  is \ *free software*\ : you can redistribute it and/or modify
it under the terms of the \ **GNU General Public License**\  as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. 



\ ``PyTek``\  is distributed in the hope that it will be useful,
but \ **without any warranty**\ ; without even the implied warranty of
\ *merchantability*\  or \ *fitness for a particular purpose*\ .  See the
GNU General Public License for more details. 



A copy of the GNU General Public License is available in the PyTek
distribution under the file LICENSE.txt. If you did not receive a copy of
this file, see `http://www.gnu.org/licenses/ <http://www.gnu.org/licenses/>`_. 

