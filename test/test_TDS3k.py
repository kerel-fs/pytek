import unittest2 as unittest
# from unittest.mock import Mock
from mock import Mock, call

from pytek import TDS3k


class TestTDS3k(unittest.TestCase):
    def setUp(self):
        # port = serial.Serial("COM1", 9600, timeout=1)
        self.port = Mock()
        self.scope = TDS3k(self.port)

    def test_initialization(self):
        self.assertEqual(self.scope.port, self.port)

    def test_close(self):
        self.scope.close()

        self.port.close.assert_called_once_with()

    def test_send_command(self):
        self.scope.send_command("HEADER", "OFF")
        self.port.write.assert_called_with("HEADER OFF\r")

    def test_send_query(self):
        self.port.readline.return_value = "TEKTRONIX,TDS 3034,0,CF:91.1CT FV:v2.11 TDS3GM:v1.00 TDS3FFT:v1.00 TDS3TRG:v1.00"

        idn = self.scope.send_query("*IDN")

        self.port.write.assert_called_with("*IDN?\r")
        self.assertEqual(idn, self.port.readline.return_value)

    def test_query_quoted_string(self):
        self.port.readline.return_value = "\"V\""

        y_unit = self.scope.query_quoted_string("WFMPRE:YUNIT")

        self.port.write.assert_called_with("WFMPRE:YUNIT?\r")
        self.assertEqual(y_unit, "V")

    def test_get_response(self):
        # TODO: Refine this test.
        self.port.read.side_effect = ["a", "b", ""]

        response = self.scope.get_response()

        self.assertEqual(response, "ab")
        self.port.read.assert_has_calls([call(1), call(1), call(1)])
