"""This module allows you to implement responsivity within Django
by detecting if the incoming request comes from mobile.

There are two main functions:
    - Responsive
    - Responsive Context Processor

The Responsive class is the main logic that analyzes the request and
determines if it is a mobile or not.

The Responsive Context Processor is the definition that passes and persists
the result of the first class into the templates.

author: pendenquejohn@gmail.com
"""

import re

class Responsive:
    """A class that detects if a request comes from a mobile
    or not by testing the User-Agent of the request.

    Description
    -----------

        Returns True or False if the request comes from a mobile or not
    """
    def __init__(self, request):
        # Process the user agent from
        # the request
        self.user_agent = request.META.get('HTTP_USER_AGENT')
        
        # Detect if mobile is in the header --
        # General test to check if mobile
        pattern = r'([m|M]obile)'
        is_match = re.search(pattern, self.user_agent)
        if is_match:
            mobile = True
        else:
            mobile = False

        # Additional test. Detect if iPhone
        # or Android. Confirms for sure then
        # that it is indeed a mobile phone
        pattern = r'(i[p|P]hone|Android)'
        is_match = re.search(pattern, self.user_agent)
        if is_match:
            self.mobile_type = is_match.group(1)
            confirmation_test = True
        else:
            confirmation_test = False

        # Now we know if we're dealing with a
        # mobile phone or not
        self.mobile = bool(mobile and confirmation_test)

def responsive_context_processor(request):
    """To persistently serve the response from Responsive() into
    the Django templates, use this definition.

    Parameters
    ----------

        request: incoming request

    Description
    -----------

        {
            is_mobile: True or False
        }
    """
    responsive = Responsive(request)
    return {'is_mobile': responsive.mobile}
