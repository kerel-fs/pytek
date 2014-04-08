=================================================================
PyTek - Python API for Tektronix oscilloscopes' serial interface
=================================================================


.. contents:: Contents
    :depth: 3

TL;DR
---------------

What?
~~~~~~~~~~~~~~
A python package that gives you an API for interacting with supported Tektronix
oscilloscopes over a serial interace.

Install?
~~~~~~~~~~~~~

::

    pip install pytek

Serial?
~~~~~~~~~~~~~

We don't provide a serial port implementation. We suggest, `pyserial`_::

    pip install pyserial

Getting Started?
~~~~~~~~~~~~~~~~~~

::

    >>> from serial import Serial
    >>> from pytek.pytek import TDS3k
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
    >>> waveform = tds.get_waveform(start=100, stop=500)
    >>> for x,y in tuple(waveform)[:10]:
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


Docs?
~~~~~~~~

* `Read The Docs (.org) <http://pytek.readthedocs.org/>`_
* `Python Hosted (.org) <http://pythonhosted.org/pytek/>`_


Misc.
---------------


Contact Information
~~~~~~~~~~~~~~~~~~~~~~~~

This project is currently hosted on `bitbucket <https://bitbucket.org>`_, 
at `https://bitbucket.org/bmearns/pytek/ <https://bitbucket.org/bmearns/pytek/>`_. The primary author is Brian Mearns:
you can contact Brian through bitbucket at `https://bitbucket.org/bmearns <https://bitbucket.org/bmearns>`_. 


Copyright and License
~~~~~~~~~~~~~~~~~~~~~~~~~~

\ ``PyTek``\  is \ *free software*\ : you can redistribute it and/or modify
it under the terms of the \ **GNU Affero General Public License**\  as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. 



\ ``PyTek``\  is distributed in the hope that it will be useful,
but \ **without any warranty**\ ; without even the implied warranty of
\ *merchantability*\  or \ *fitness for a particular purpose*\ .  See the
GNU Affero General Public License for more details. 



A copy of the GNU Affero General Public License is available in the templ
distribution under the file LICENSE.txt. If you did not receive a copy of
this file, see `http://www.gnu.org/licenses/ <http://www.gnu.org/licenses/>`_. 

