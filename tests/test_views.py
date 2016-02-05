from django.core.urlresolvers import reverse
from rest_framework.test import APIRequestFactory

from rest_framework_friendly_errors import settings

from tests import BaseTestCase
from tests.models import Snippet
from tests.views import SnippetList, Snippet2List, SnippetDetail


class ListViewTestCase(BaseTestCase):
    def setUp(self):
        super(ListViewTestCase, self).setUp()
        self.factory = APIRequestFactory()

    def test_empty_list_view(self):
        request = self.factory.get(reverse('snippet-list'))
        response = SnippetList.as_view()(request)
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, 200)

    def test_create_a_valid_snippet(self):
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_invalid_boolean(self):
        self.data_set['linenos'] = 'A text instead of a bool'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['BooleanField']['invalid']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'linenos')

    def test_invalid_char_field(self):
        # Too long string
        self.data_set['title'] = 'Too Long Title For Defined Serializer'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['max_length']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'title')

        # Empty string
        self.data_set['title'] = ''
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['blank']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'title')

        # No data provided
        self.data_set.pop('title')
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['required']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'title')

    def test_invalid_choice_field(self):
        # invalid choice
        self.data_set['language'] = 'brainfuck'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['invalid_choice']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'language')

        # empty string
        self.data_set['language'] = ''
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['invalid_choice']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'language')

        # no data provided
        self.data_set.pop('language')
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['required']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'language')

    def test_invalid_decimal_field(self):
        # invalid
        self.data_set['rating'] = 'text instead of float'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['invalid']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'rating')

        # decimal places
        self.data_set['rating'] = 2.99
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['max_decimal_places']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'rating')

        # decimal max digits
        self.data_set['rating'] = 222.9
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['max_digits']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'rating')

    def test_datetime_field_error_content(self):
        # invalid
        self.data_set['posted_date'] = 'text instead of date'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['DateTimeField']['invalid']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'posted_date')

    def test_custom_field_validation_method(self):
        self.data_set['comment'] = 'comment'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors'][0]['field'], 'comment')
        self.assertEqual(response.data['errors'][0]['code'], 5000)

    def test_custom_field_validation_using_validators(self):
        self.data_set['title'] = 'A title'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors'][0]['field'], 'title')
        self.assertEqual(response.data['errors'][0]['code'], 5001)

    def test_field_dependency_validation(self):
        self.data_set['title'] = 'A Python'
        self.data_set['language'] = 'c++'
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.data['errors'][0]['field'])
        self.assertEqual(response.data['errors'][0]['code'], 8000)

    def test_error_registration(self):
        self.data_set['title'] = 'A Python'
        self.data_set['language'] = 'c++'
        request = self.factory.post(reverse('snippet2-list'), data=self.data_set)
        response = Snippet2List.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errors'][0]['field'], 'language')
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['invalid_choice']
        self.assertEqual(
            response.data['errors'][0]['code'], code
        )

    def test_couple_errors(self):
        self.data_set['comment'] = 'comment'
        self.data_set['rating'] = 'Not a number at all'

        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data['errors']), 2)

    def test_unique_constraint(self):
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        SnippetList.as_view()(request)
        request = self.factory.post(reverse('snippet-list'), data=self.data_set)
        response = SnippetList.as_view()(request)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_VALIDATOR_ERRORS['UniqueValidator']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'watermark')


class DetailViewTestCase(BaseTestCase):
    def setUp(self):
        super(DetailViewTestCase, self).setUp()
        self.factory = APIRequestFactory()
        self.snippet = Snippet.objects.create(**self.data_set)

    def test_retrieve_object(self):
        request = self.factory.get(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}))
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 200)

    def test_update_snippet(self):
        self.data_set['code'] = 'def foo(bar):\n\treturn bar'
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['code'], 'def foo(bar):\n\treturn bar')

    def update_invalid_boolean(self):
        self.data_set['linenos'] = 'A text instead of a bool'
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['BooleanField']['invalid']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'linenos')

    def test_upload_invalid_char_field(self):
        # Too long string
        self.data_set['title'] = 'Too Long Title For Defined Serializer'
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['max_length']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'title')

        # Empty string
        self.data_set['title'] = ''
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['blank']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'title')

        # No data provided
        self.data_set.pop('title')
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['required']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'title')

    def test_upload_invalid_choice_field(self):
        # invalid choice
        self.data_set['language'] = 'brainfuck'
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['invalid_choice']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'language')

        # empty string
        self.data_set['language'] = ''
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['invalid_choice']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'language')

        # no data provided
        self.data_set.pop('language')
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['required']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'language')

    def test_upload_invalid_decimal_field(self):
        # invalid
        self.data_set['rating'] = 'text instead of float'
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['invalid']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'rating')

        # decimal places
        self.data_set['rating'] = 2.99
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['max_decimal_places']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'rating')

        # decimal max digits
        self.data_set['rating'] = 222.9
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['max_digits']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'rating')

    def test_datetime_field_error_content(self):
        # invalid
        self.data_set['posted_date'] = 'text instead of date'
        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_FIELD_ERRORS['DateTimeField']['invalid']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'posted_date')

    def test_cannot_update_to_not_unique_watermark(self):
        self.data_set['watermark'] = 'TEST2'
        Snippet.objects.create(**self.data_set)

        request = self.factory.put(reverse('snippet-detail',
                                           kwargs={'pk': self.snippet.pk}),
                                   data=self.data_set)
        response = SnippetDetail.as_view()(request, pk=self.snippet.pk)
        self.assertEqual(response.status_code, 400)
        code = settings.FRIENDLY_VALIDATOR_ERRORS['UniqueValidator']
        self.assertEqual(response.data['errors'][0]['code'], code)
        self.assertEqual(response.data['errors'][0]['field'], 'watermark')
