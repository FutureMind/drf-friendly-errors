from django.template.defaultfilters import title
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from tests.models import LANGUAGE_CHOICES, Snippet


def is_proper_title(value):
    if value and value != title(value):
        raise ValidationError('Incorrect title')


class SnippetSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=10, validators=[is_proper_title])
    comment = serializers.CharField(max_length=255)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    posted_date = serializers.DateTimeField()

    def validate_comment(self, value):
        if value[0] != value[0].upper():
            raise ValidationError('First letter must be an uppercase')
        return value

    def validate(self, attrs):
        # if phrase python is in title, language must be python as well
        language = attrs.get('language')
        title = attrs.get('title')
        if 'python' in title.lower() and language != 'python':
            raise ValidationError('Must be a python language')
        return attrs

    FIELD_VALIDATION_ERRORS = {'validate_comment': 5000,
                               'is_proper_title': 5001}

    NON_FIELD_ERRORS = {'Must be a python language': 8000}


class AnotherSnippetSerializer(FriendlyErrorMessagesMixin,
                               serializers.Serializer):
    """
    Mirror snippet for test register error mixin method
    """
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=10, validators=[is_proper_title])
    comment = serializers.CharField(max_length=255)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)
    posted_date = serializers.DateTimeField()

    def validate_comment(self, value):
        if value[0] != value[0].upper():
            raise ValidationError('First letter must be an uppercase')
        return value

    def validate(self, attrs):
        # if phrase python is in title, language must be python as well
        language = attrs.get('language')
        title = attrs.get('title')
        if 'python' in title.lower() and language != 'python':
            self.register_error(error_message='Python, fool!',
                                error_key='invalid_choice',
                                field_name='language')
        return attrs

    FIELD_VALIDATION_ERRORS = {'validate_comment': 5000,
                               'is_proper_title': 5001}

    NON_FIELD_ERRORS = {'Must be a python language': 8000}


class SnippetModelSerializer(FriendlyErrorMessagesMixin,
                             serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = '__all__'

    def validate_comment(self, value):
        if value[0] != value[0].upper():
            raise ValidationError('First letter must be an uppercase')
        return value

    def validate(self, attrs):
        # if phrase python is in title, language must be python as well
        language = attrs.get('language')
        title = attrs.get('title')
        if 'python' in title.lower() and language != 'python':
            raise ValidationError('Must be a python language')
        return attrs

    FIELD_VALIDATION_ERRORS = {'validate_comment': 5000,
                               'is_proper_title': 5001}

    NON_FIELD_ERRORS = {'Must be a python language': 8000}


class AnotherSnippetModelSerializer(FriendlyErrorMessagesMixin,
                                    serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = '__all__'

    def validate_comment(self, value):
        if value[0] != value[0].upper():
            raise ValidationError('First letter must be an uppercase')
        return value

    def validate(self, attrs):
        # if phrase python is in title, language must be python as well
        language = attrs.get('language')
        title = attrs.get('title')
        if 'python' in title.lower() and language != 'python':
            self.register_error(error_message='Python, fool!',
                                error_key='invalid_choice',
                                field_name='language')
        return attrs

    FIELD_VALIDATION_ERRORS = {'validate_comment': 5000,
                               'is_proper_title': 5001}

    NON_FIELD_ERRORS = {'Must be a python language': 8000}


class ThirdSnippetSerializer(
    FriendlyErrorMessagesMixin,
    serializers.ModelSerializer
):
    class Meta:
        model = Snippet
        fields = '__all__'

    def validate_comment(self, value):
        if value[0] != value[0].upper():
            self.register_error(
                'First letter must be an uppercase', field_name='comment',
                error_key='blank'
            )
        return value
