from rest_framework import serializers
from rest_framework_friendly_errors import settings
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from tests import BaseTestCase
from tests.serializers import SnippetSerializer, AnotherSnippetSerializer
from tests.utils import run_is_valid


class SimpleSerializerClass(FriendlyErrorMessagesMixin, serializers.Serializer):
    text_field = serializers.CharField(max_length=255)
    integer_field = serializers.IntegerField()
    boolean_field = serializers.BooleanField(default=True)


class SanityTestCase(BaseTestCase):

    def test_serializer_valid(self):
        s = SimpleSerializerClass(data={'text_field': 'TEST',
                                        'integer_field': 0,
                                        'boolean_field': False})
        self.assertTrue(s.is_valid())

    def test_serializer_invalid(self):
        s = SimpleSerializerClass(data={'text_field': 'TEST',
                                        'integer_field': 'TEST',
                                        'boolean_field': False})
        self.assertFalse(s.is_valid())


class SerializerErrorsTestCase(BaseTestCase):

    def test_serializer_is_valid(self):
        s = SnippetSerializer(data=self.data_set)
        self.assertTrue(s.is_valid())

    def test_serializer_invalid(self):
        self.data_set['linenos'] = 'A text instead of a bool'
        s = SnippetSerializer(data=self.data_set)
        self.assertFalse(s.is_valid())

    def test_error_message(self):
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        self.assertFalse(s.errors)

        self.data_set['linenos'] = 'A text instead of a bool'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        self.assertTrue(s.errors)
        self.assertTrue(type(s.errors), dict)

    def test_error_message_content(self):
        self.data_set['linenos'] = 'A text instead of a bool'
        s = run_is_valid(SnippetSerializer, data=self.data_set)

        self.assertEqual(s.errors['message'],
                         settings.VALIDATION_FAILED_MESSAGE)
        self.assertEqual(s.errors['code'], settings.VALIDATION_FAILED_CODE)
        self.assertEqual(type(s.errors['errors']), list)
        self.assertTrue(s.errors['errors'])

    def test_boolean_field_error_content(self):
        self.data_set['linenos'] = 'A text instead of a bool'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['BooleanField']['invalid']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'linenos')

    def test_char_field_error_content(self):
        # Too long string
        self.data_set['title'] = 'Too Long Title For Defined Serializer'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['max_length']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'title')

        # Empty string
        self.data_set['title'] = ''
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['blank']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'title')

        # No data provided
        self.data_set.pop('title')
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['CharField']['required']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'title')

    def test_choice_field_error_content(self):
        # invalid choice
        self.data_set['language'] = 'brainfuck'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['invalid_choice']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'language')

        # empty string
        self.data_set['language'] = ''
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['invalid_choice']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'language')

        # no data provided
        self.data_set.pop('language')
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['required']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'language')

    def test_decimal_field_error_content(self):
        # invalid
        self.data_set['rating'] = 'text instead of float'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['invalid']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'rating')

        # decimal places
        self.data_set['rating'] = 2.99
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['max_decimal_places']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'rating')

        # decimal max digits
        self.data_set['rating'] = 222.9
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['DecimalField']['max_digits']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'rating')

    def test_datetime_field_error_content(self):
        # invalid
        self.data_set['posted_date'] = 'text instead of date'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        code = settings.FRIENDLY_FIELD_ERRORS['DateTimeField']['invalid']
        self.assertEqual(s.errors['errors'][0]['code'], code)
        self.assertEqual(s.errors['errors'][0]['field'], 'posted_date')

    def test_custom_field_validation_method(self):
        self.data_set['comment'] = 'comment'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        self.assertEqual(s.errors['errors'][0]['field'], 'comment')
        self.assertEqual(s.errors['errors'][0]['code'], 5000)

    def test_custom_field_validation_using_validators(self):
        self.data_set['title'] = 'A title'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        self.assertEqual(s.errors['errors'][0]['field'], 'title')
        self.assertEqual(s.errors['errors'][0]['code'], 5001)

    def test_field_dependency_validation(self):
        self.data_set['title'] = 'A Python'
        self.data_set['language'] = 'c++'
        s = run_is_valid(SnippetSerializer, data=self.data_set)
        self.assertIsNone(s.errors['errors'][0]['field'])
        self.assertEqual(s.errors['errors'][0]['code'], 8000)

    def test_error_registration(self):
        self.data_set['title'] = 'A Python'
        self.data_set['language'] = 'c++'
        s = run_is_valid(AnotherSnippetSerializer, data=self.data_set)
        self.assertEqual(s.errors['errors'][0]['field'], 'language')
        code = settings.FRIENDLY_FIELD_ERRORS['ChoiceField']['invalid_choice']
        self.assertEqual(s.errors['errors'][0]['code'], code)
