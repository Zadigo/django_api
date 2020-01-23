import re
import socket

import requests
from bs4 import BeautifulSoup


class IpAnalyzer:
    def __init__(self, request=None):
        # Get the actual IP from the user
        response = requests.get('http://checkip.dyndns.com/')
        if response.status_code == 200:
            response_text = response.content.decode('utf-8')
            # Match the IP from the HTML object
            ip = re.findall(r'(\d+(?=\.)?)', response_text)
            if ip and len(ip) == 4:
                self.full_ip = '.'.join(ip)

                self.host_name = socket.gethostbyaddr(self.full_ip)

                # Send another request to get the IP information
                response = requests.get(f'https://ipinfo.io/{self.full_ip}/json')
                self.ip_infos = response.json()
            else:
                self.ip_infos = {'error': {'message': 'We were not able to get any information'}}
        else:
            pass

    @staticmethod
    def ip_from_request(request):
        ip = request.META
        return ip
