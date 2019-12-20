from django_api.aws.aws_manager import AWS, TransferManager, QueryManager
import unittest

class TestAws(unittest.TestCase):
    def setUp(self):
        manager = AWS()
        self.session = manager.create_session('', '', '')

    def region_name(self):
        print(self.session.region_name)