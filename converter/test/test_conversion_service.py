import unittest
from converter.app.conversion_service import ConversionException, Converter

class TestConversionService(unittest.TestCase):

    def setUp(self):
        self.conv = Converter()

    def test_unix_ZeroValue(self):
        self.conv.convert_unix_to_rfc('0')

    def test_unix_InvalidAlphabeticTextAsInput(self):
        with self.assertRaises(ConversionException):
            self.conv.convert_unix_to_rfc('letters')

    def test_unix_TimeWithoutMicroseconds(self):
        self.assertEqual(self.conv.convert_unix_to_rfc('1490107042'),'2017-03-21T15:37:22Z')

    def test_unix_TimeWithMicroseconds(self):
        self.assertEqual(self.conv.convert_unix_to_rfc('1490107042.1234343'), '2017-03-21T15:37:22.123434Z')

    def test_unix_InvalidDotWithoutMicrosecondsAsInput(self):
        with self.assertRaises(ConversionException):
            self.conv.convert_unix_to_rfc('1490107042.')

    def test_unix_InvalidAlphabeticTextAsInput(self):
        with self.assertRaises(ConversionException):
            self.conv.convert_rfc_to_unix('letters')

    def test_unix_InputWithMissingT(self):
        with self.assertRaises(ConversionException):
            self.conv.convert_rfc_to_unix('2017-03-21 15:37:22Z')

    def test_rfc_TimeWithoutMicroseconds(self):
         self.assertEqual(self.conv.convert_rfc_to_unix('2017-03-21T15:37:22-00:00'), '1490107042')

    def test_rfc_TimeWithMicroseconds(self):
        self.assertEqual(self.conv.convert_rfc_to_unix('2017-03-21T15:37:22.123434Z'),'1490107042.123434')

if __name__ == '__main__':
    unittest.main()