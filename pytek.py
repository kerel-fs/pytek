"""
:mod:`tektronix` -- Serial interface for Tektronix oscilloscopes

.. module:: tektronix
    :synopsis: Interface with supported Tektronix oscilloscopes over a serial interface.
.. moduleauthor:: Brian Mearns <brian.mearns@schneider-electric.com>

"""


import time
import re


class TDS3xxx(object):
    __ID_TDS_3000_REGEX = re.compile(r'^TEKTRONIX,TDS 3\d{3},')

    def __init__(self, port):
        self.port = port

    def close(self):
        """
        Closes the object's `port`.
        """
        self.port.close()

    def send_command(self, command, *args):
        """
        Sends a command and any number of arguments. Does not wait for response.
        """
        args = [command] + list(args)
        self.port.write("%s\r" % " ".join(args))


    def headers_off(self):
        """
        Sends the command "HEADER OFF" to the device, to disable echoing of headers (command names)
        in query responses from the device. Most methods that query the device will cause this
        to be sent. You can turn it back on with `headers_on`, or by sending the "HEADER ON" command.
        """
        self.send_command("HEADER", "OFF")

    def heders_on(self):
        """
        Sends the "HEADER ON" command to the device. See `headers_off` for details.
        """
        self.send_command("HEADER", "ON")

    def send_query(self, query):
        """
        Sends a query to the device and reads back one line, returning that
        line (stripped of trailing whitespace).

        A '?' and a linebreak are automatically appended to the end of what
        you send.

        E.g.:

        >>> tek.send_query("*IDN")
        'TEKTRONIX,TDS 3034,0,CF:91.1CT FV:v2.11 TDS3GM:v1.00 TDS3FFT:v1.00 TDS3TRG:v1.00'
        >>>

        .. warning::

            This method turns off header echoing from the device. I.e., it sends "HEADER OFF"
            before anything else (through the `headers_off` method). If you're expecting headers
            to be on subsequently, you will need to turn them on with "HEADER ON", or with the
            `headers_on` command.

        """
        self.headers_off()
        self.send_command("%s?" % query)
        return self.port.readline().rstrip()

    def identify(self):
        """
        Convenience function for sending the "*IDN" query, with `send_query`.
        """
        return self.send_query("*IDN")

    def sanity_check(self):
        """
        Does a sanity check on the device to make sure that the way it identifies
        itself matches the expected response. Returns True if the sanity check passes,
        otherwise False.
        
        See also: `identify` and `force_sanity`.
        """
        id = self.identify()
        return TDS3xxx.__ID_TDS_3000_REGEX.match(id)

    def force_sanity(self):
        """
        Does the `sanity_check` on the device, and raises an exception if the check fails.
        """
        if not self.sanity_check():
            raise Exception("Unexpected string returned by identify.")

    def get_num_points(self):
        """
        Queries the number of points that will be sent in a waveform or curve query,
        based on the current settings.
        """
        return int(self.send_query("WFMPRE:NR_PT"))

    def query_quoted_string(self, query):
        """
        Like `send_query`, but expects a quoted string as a response, and strips
        the quotes off the response before returning. Raises a `ValueError` if the
        response is not quoted.
        """
        resp = self.send_query(query)
        if resp[0] == '"' and resp[-1] == '"':
            return resp[1:-1]
        raise ValueError("Expected a quoted string, received: %r" % resp)
        
    def y_units(self):
        """
        Returns a string giving the units of the Y axis based on the current waveform settings.
        """
        resp = self.query_quoted_string("WFMPRE:YUNIT")

    def x_units(self):
        """
        Returns a string giving the units of the X axis based on the current waveform settings.
        """
        resp = self.query_quoted_string("WFMPRE:XUNIT")



    def get_waveform_preamble(self):
        """
        Queries the waveform preamble from the device, which details how a waveform or curve will be transferred
        from the device based on the current settings (as with `get_curve`). Returns a dictionary of preamble values.
        """
        
        wfm = self.send_query("WFMPRE").split(';')
        d = dict(zip(
            ('bytes_per_sample', 'bits_per_sample', 'encoding', 'binary_format', 'byte_order', 'number_of_points',
            'waveform_id', 'point_format', 'x_incr', 'pt_offset', 'xzero', 'x_units', 'y_scale', 'y_zero', 'y_offset', 'y_unit'),
            wfm
        ))
        return d


    def get_waveform(self, source="CH1", double=True, start=1, stop=10000, preamble=False, timing=False):
        """
        Similar to `get_curve`, but uses waveform permable data to properly scale the received data.

        If `preamble` or `timing` are True, returns a tuple: (preamble_data, data, timing_data), where the
        `preamble_data` and `timing_data` are only present if the corresponding flag is set.

        If neither `preamble` nor `timing` is True, then just returns as the sole argument `data` (i.e., 
        `data`, not `(data,)`).

        Data is a sequence of two tuples, giving the X and Y value for each point, in order across the X-acis
        from left to right. These are properly scaled based on the waveform settings, usually giving a value
        in Volts versus Seconds, but check `x_units` and `y_units` to be sure.
        """
        curve = self.get_curve(source=source, double=double, start=start, stop=stop, preamble=True, timing=True)
        wfm = self.get_waveform_preamble()
        xzero = float(wfm["xzero"])
        dx = float(wfm["x_incr"])
        ym = float(wfm["y_scale"])
        yoff = float(wfm["y_offset"])
        yzero = float(wfm["y_zero"])

        points = curve[1]
        data = (
            (xzero + i*dx, ((points[i] - yoff) * ym) + yzero)
                for i in xrange(len(points))
        )
        if preamble or timing:
            if preamble:
                ret = [curve[0], data]
            else:
                ret = [data]
            if timing:
                ret.append(curve[2])
            return ret
        return data


    def get_response(self):
        """
        Simply reads data from the port, one byte at a time until it times out, then
        returns the data as a `str`.

        Waits indefinitely for the first byte.
        """
        while True:
            data = self.port.read(1)
            if len(data):
                break
        while True:
            c = self.port.read(1)
            if len(c) == 0:
                break
            data += c
        return data


    def get_curve(self, source="CH1", double=True, start=1, stop=10000, preamble=False, timing=False):
        """
        Queries a curve (waveform) from the device and returns it as a set of data points. Note that the
        points are simply unsigned integers over a fixed range (depending on the `double` parameter), they
        are not voltage values or similar. Use `get_waveform` to get scaled values in the proper units.

        .. warning::

            Note that this method will set waveform preamble and data parameters on the device, which have
            a persistent effect which could alter the behavior of future commands.

        If `preamble` or `timing` are True, returns a tuple: (preamble_data, data, timing_data), where the
        `preamble_data` and `timing_data` are only present if the corresponding flag is set.

        If neither `preamble` nor `timing` is True, then just returns as the sole argument `data` (i.e., 
        `data`, not `(data,)`).

        In either case, `data` will be a sequence of data points for the curve. If the `double` parameter is
        True (the default), data points are each double-byte wide, in the range from 0 through 65535 (inclusive).
        This gives you maximum resolution on your data, but takes longer to transfer. Also note that the device
        does not necessarily have 16 bits of precision in measurement, but data will be right-aligned.

        If `double` is False, then the data points are single-byte each, in the range from 0 through 255 (inclusive).
        
        Regardless of `double`, the minimum value corresponds to one vertical division *below* the bottom of
        the screen, and the maximum value corresponds to one vertical division *above* the top of the screen.

        :param str source:      Optional, specify the channel to copy the waveform from. Default is "CH1".

        :param bool double:     Optional, if True (the default), data points are transferred 16-bits per
                                point, otherwise they are transferred 8-bits per point, which may cut off
                                least significant bits but will transfer faster.

        :param int start:       Optional, the data point to start at. The waveforms contains up to 10000
                                data points, the first point is 1. The default value is 1. If you set this
                                param to None, it has the same effect as a 1.

        :param int stop:        Optional, the data point to stop at. See `start` for details. The default
                                value is 10000 to transfer the entire waveform. If you set this to None,
                                it has the same effect as 10000.

        :param bool paramable:  Controls whether or not the curve's preamble is included in the return value.
                                The curve's preamble is not the same as the waveform preamble that configures
                                the data. The curve's preamble is a string that is transmitted prior to the
                                curve's data points. I'm honestly not sure what it is, but it increases with
                                the number of data points transferred.

        :param bool timing:     Controls whether or not timing information is included in the return value.
                                Timing gives the number of seconds it took to transfer the data, as a floating
                                point value.

        """
        width = 1
        if double:
            width = 2

        if start is None:
            start = 1
        if stop is None:
            stop = 10000

        #Configure the waveform the way we want it for transfer.
        self.headers_off()
        self.send_command("DATA:SOURCE", source)
        self.send_command("DATA:WIDTH", str(width))
        self.send_command("DATA:ENCDG", "RPBinary")
        self.send_command("WFMPRE:PT_Fmt", "Y")
        self.send_command("DATA:START", str(start))
        self.send_command("DATA:STOP", str(stop))

        #Check how many points it's going to send.
        point_count = self.get_num_points()

        start_time = time.time()
        self.send_command("CURVE?")
        data = self.get_response()

        stop_time = time.time()

        #Strip trailing linebreak.
        if(ord(data[-1]) == 0x0A):
            data = data[:-1]

        length = len(data)
        preamble_len = length - width*point_count
        preamble_data = data[:preamble_len]

        points = []
        if width == 2:
            for i in xrange(preamble_len, len(data), 2):
                msB = ord(data[i])
                lsB = ord(data[i+1])
                points.append(msB << 8 | lsB)
        else:
            points = [ord(b) for b in data[preamble_len:]]

        assert(len(points) == point_count)

        if preamble or timing:
            if preamble:
                ret = [preamble_data, points]
            else:
                ret = [points]
            if timing:
                ret.append(stop_time - start_time)
            return ret

        return points


    def screenshot(self, ofile=None, fmt="TIFF", inksaver=True, landscape=False):
        """
        Grabs a hardcopy/screenshot from the device.

        If `ofile` is None (the default), simply returns the data as a string. Otherwise, it
        writes the data to the given output stream.

        :param str fmt:     Optional, specify the format for the image. Valid values will vary
                            by device, but will be a subset of the following: TDS3PRT, BMP,
                            BMPColor, DESKJET, DESKJETC, EPSColor, EPSMono, EPSOn, INTERLEAF, 
                            LASERJET, PCX, PCXcolor, RLE, THINKJET, TIFF, DPU3445, BJC80, PNG.
                            The default is "TIFF".

        """
        self.send_command("HARDCOPY:FORMAT", str(fmt))
        self.send_command("HARDCOPY:LAYOUT", "landscape" if landscape else "portrait")
        self.send_command("HARDCOPY:INKSAVER", "on" if inksaver else "off")
        self.send_command("HARDCOPY:PORT", "RS232")
        self.send_command("HARDCOPY", "START")
        data = self.get_response()
        if ofile is not None:
            ofile.write(data)
            return None
        else:
            return data



if __name__ == '__main__':
    import serial
    
    start = time.time()

    port = serial.Serial("COM1", 9600, timeout=2)
    tek = TDS3xxx(port)

    print tek.identify()
    tek.force_sanity()

    ### Capture waveform points
    if 0:

        points = tuple(tek.get_waveform(double=False))

        with open("waveform2.dat", "w") as ofile:
            ofile.write("\n".join("%f %f" % pt for pt in points))

        stop = time.time()
        print "Captured %d points in %.2f seconds." % (len(points), stop - start)

    ### Capture screenshot
    else:
        formats = (
            ("TIFF", "tiff"),
            ("RLE", "rel.bmp"),
            ("BMP", "bw.bmp"),
            ("BMPColor", "color.bmp"),
            ("EPSColor", "color.eps"),
            ("EPSMono", "mono.eps"),
        )


        times = {}
        for fmt, ext in formats:

            ofile = open("screenshot." + ext, "wb")
            start = time.time()
            tek.screenshot(ofile, fmt=fmt)
            ofile.close()
            stop = time.time()
            times[fmt] = stop - start
            print "Captured %s screenshot in %.2f seconds." % (fmt, stop - start)
            


