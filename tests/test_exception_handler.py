from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from rest_framework_friendly_errors import settings

from tests import BaseTestCase
from views import SnippetList


class ExceptionHandlerTestCase(BaseTestCase):
    def setUp(self):
        super(ExceptionHandlerTestCase, self).setUp()
        self.factory = APIRequestFactory()

    def test_server_error(self):
        response = self.client.get(reverse('server-error'))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data['message'], 'APIException')
        self.assertEqual(response.data['status_code'], 500)
        self.assertEqual(response.data['code'],
                         settings.FRIENDLY_EXCEPTION_DICT.get('APIException'))

    def test_handler_do_not_touch_pretty_errors(self):
        self.data_set['language'] = 'node.js'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertNotIn('status_code', response.data)

    def test_not_found(self):
        response = self.client.get(reverse('not-found'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['status_code'], 404)
        self.assertEqual(response.data['code'],
                         settings.FRIENDLY_EXCEPTION_DICT.get('NotFound'))

    def test_method_not_allowed(self):
        response = self.client.get(reverse('not-allowed'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data['status_code'], 405)
        self.assertEqual(
            response.data['code'],
            settings.FRIENDLY_EXCEPTION_DICT.get('MethodNotAllowed')
        )

    def test_not_authenticated(self):
        response = self.client.get(reverse('not-authenticated'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['status_code'], 403)
        self.assertEqual(
            response.data['code'],
            settings.FRIENDLY_EXCEPTION_DICT.get('NotAuthenticated')
        )
