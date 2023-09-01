import string
import random
import hashlib
import os
from datetime import datetime

__version__ = '1.0.0'


class TestDataGenerator(object):
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    """
    This library is only used in TSF framework for custom keywords.
    """

    
    def randomString(size):
        """Takes one *argument* size  and return random string of same size .

        Example:
        | Your Keyword   5 | return --> app12
        | Your Keyword   6 | return --> lit123
        """
        return hashlib.md5(os.urandom(128)).hexdigest()[:int(size)]
    
    def get_random_name(self, length):
        """Takes one *argument* length  and return random alphabet string of same size .

        Example:
        | Your Keyword   5 | return --> apple
        | Your Keyword   6 | return --> little
        """
        letters = string.ascii_lowercase[:12]
        return ''.join(random.choice(letters) for i in range(length))
    
   
    def generate_random_emails(self, length):
        """Takes one *argument* length  and return random email with any domains where username will of length passed.
           ["hotmail.com", "gmail.com", "aol.com","mail.com", "mail.kz", "yahoo.com"]
        Example:
        | Your Keyword   5 | return --> abcde@gmail.com
        | Your Keyword   6 | return --> abcdef@hotmail.com
        """
        domains = ["hotmail.com", "gmail.com", "aol.com",
                   "mail.com", "mail.kz", "yahoo.com"]

        return [self.get_random_name(length)
                + '@'
                + random.choice(domains)]
    
    def generate_random_mobile(self,countryCode='91'):
        """Takes one *argument* countryCode  and return random mobile number with pased countrycode of default is 91.
        Supported countryCode : 91,92
        Example:
        | Your Keyword   92 | return --> 928745678***
        | Your Keyword    | return --> 9188998765**
        """
        if countryCode == '91':
            return countryCode + str(random.randint(7000000000, 8999999999))
    
    def generate_random_name(self,size=7):
        """Takes one *argument* length  and return random alphabet string of same size .

        Example:
        | Your Keyword   5 | return --> apple
        | Your Keyword   6 | return --> little
        """
        return self.get_random_name(size)
    
    def get_today_datetime(self,format="%Y-%m-%d %H:%M:%S"):
        """Takes one *argument* format(default : *%Y-%m-%d %H:%M:%S*)  and return current time in same format.
        
        Example:
        | Your Keyword    | return --> 2023-08-18 12:22:00
        | Your Keyword    "%m-%Y-%d %H:%M:%S" | return --> 08-2023-18 12:22:00 
        """
        now = datetime.now()
        dt_string = now.strftime(format)
        return dt_string
    
   