import requests

class Zapier:
    def __init__(self, url, **kwargs):
        response = requests.post(url, data=kwargs)
        if response.status_code == 200:
            self.response = response

class Slack(Zapier):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)

class MailChimp(Zapier):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)
