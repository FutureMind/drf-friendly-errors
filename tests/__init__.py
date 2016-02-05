from datetime import datetime

from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        self.data_set = {'title': 'A Snippet', 'code': 'print "Hello World!"',
                         'linenos': True, 'language': 'python', 'rating': 0.0,
                         'posted_date': datetime.now(), 'comment': 'Comment',
                         'watermark': 'TEST'}
