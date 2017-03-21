from re import match
from datetime import datetime

class Converter:

    def convert_unix_to_rfc(self,datestr):
        if not match(r'[0-9]+(\.[0-9]+)?', datestr):
            raise ConversionException({'date': 'provided date string was not unix formatted'})
        return datetime.fromtimestamp(float(datestr))

    def convert_rfc_to_unix(self):
        return None

class ConversionException(Exception):

    def __init__(self,errors):
        self.errors = errors