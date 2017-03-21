import time
from re import match
from datetime import datetime
from dateutil import parser

class Converter:

    def __init__(self):
        self.regex_unix = r'^-?[0-9]+(\.[0-9]+)?$'
        self.regex_rfc = r'^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\.[0-9]+)?(([Zz])|([\+|\-]([01][0-9]|2[0-3]):[0-5][0-9]))$'

    def convert_unix_to_rfc(self,datestr):
        """
        Takes a unix formated datestring and converts it to rfc 3339
        :param datestr:
        :return:
        """
        self._test_date_(datestr,self.regex_unix,'unix')
        return datetime.fromtimestamp(float(datestr)).isoformat('T')+'Z'

    def convert_rfc_to_unix(self,datestr):
        """
        Takes a rfc 3339 formated datestring and converts it to unix time
        :param datestr:
        :return:
        """
        self._test_date_(datestr,self.regex_rfc,'rfc3339')
        try:
            date = parser.parse(datestr)
            unixtime = float(time.mktime(date.timetuple()))
            microseconds = '.'+str(date.microsecond) if date.microsecond != 0 else ''

            #somewhat hacky, but mktime drops the floating precision and micros can't be added mathematically
            return str(unixtime).split('.')[0]+microseconds

        except ValueError:
            raise ConversionException({'date': 'provided date string was not properly rfc3339-formatted'})

    def _test_date_(self,datestr,regex,format):
        if not match(regex, datestr):
            raise ConversionException({'date': 'provided date string was not properly '+format+'-formatted'})

class ConversionException(Exception):

    def __init__(self,errors):
        self.errors = errors