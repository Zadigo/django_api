import os
import re

import requests


class LaPosteAPI:
    """This API uses La Poste's address verification
    service in order to determine wheter an address
    exists or not.
    """
    base_url = 'https://api.laposte.fr/controladresse/v1/adresses?q='

    def __init__(self, url, *args):
        """Create an API request to La Poste.
        """
        secret_key = os.environ.get('LA_POSTE_SECRET_KEY', None)
        if not secret_key:
            raise KeyError('You have not provided any secret key')

        try:
            # Create the request with the mandatory headers
            response = requests.get(url, headers={'X-Okapi-Key': secret_key})
        except requests.HTTPError:
            raise
        else:
            self.response = response.json()

class CheckAddress(LaPosteAPI):
    """
    Check that the provided address exists and receive a dictionnary 
    if there are multiple addresses.
    """
    def __init__(self, address):
        super().__init__(self.base_url + address)

    def __str__(self):
        return str(self.response)

    @property
    def count(self):
        return len(self.response)

    @property
    def addresses(self):
        return (item['adresse'] for item in self.response)

    def address(self):
        if self.count == 1:
            address = self.response[0]['adresse']

            # REGEX the address
            groups = re.search(r'^(\d+)\s+(.*)\s+(\d{5})\s+(.*)$', address)
            if groups:
                class Address:
                    def __init__(self, number, name, post_code, city):
                        self.street_number = number
                        self.street_name = name
                        self.zip_code = post_code
                        self.city = city

                    @property
                    def group(self):
                        return [self.street_number, self.street_name, self.zip_code, self.city]

                return Address(groups.group(1), groups.group(2), groups.group(3), groups.group(4))
        else:
            raise ValueError('.address() got multiple addesses. Needed 1.')



a='36 RUE DE SUEDE AVENUE LELIEVRE 59120 LOOS'
b='36 BIS RUE DE SUEDE 37100 TOURS'

w = CheckAddress(b)
print(w.address().group)
