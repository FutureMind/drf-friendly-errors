REST framework friendly errors
==============================

**Extension for Django REST framework error display**

Overview
--------

This package extends default error JSON body providing configurable error codes
and more consumable response structure.

It turns default JSON body of HTTP 400 response, which look like this

.. code:: python

    {
        "name": ["This field is required."],
        "password": ["This field may not be blank."]
        "age": ["This field may not be null."]
        "description": ["Ensure this field has no more than 100 characters."]
    }

into

.. code:: python

    {
        "code" : 1001,
        "message" : "Validation Failed",
        "errors" : [
            {
                "code" : 2002,
                "field" : "name",
                "message" : "This field is required."
            },
            {
                "code" : 2031,
                "field" : "password",
                "message" : "This field may not be blank."
            },
            {
                "age" : 2023,
                "field" : "age",
                "message" : "This field may not be null."
            },
            {
                "age" : 2041,
                "field" : "description",
                "message" : "Ensure this field has no more than 100 characters."
            },
        ]
    }

Library handles all `Django REST framework`_ built-in serializer validation.

Requirements
------------
-  Python (2.7, 3.4)
-  Django (1.8, 1.9)
-  Django REST framework (3.3)

Installation
------------

By running installation script

.. code:: bash

    $ python setup.py install

Or directly from this repository using ``pip``\...

.. code:: bash

    $ pip install git+https://tlaszczuk@bitbucket.org/tlaszczuk/rest-framework-friendly-errors.git

Usage
-----

Simply add a FriendlyErrorMessagesMixin to your serializer or model serializer class

.. code:: python

    from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

    class MySerializer(FriendlyErrorMessagesMixin, ModelSerializer):

If you want to change default library settings and provide your own set of error codes just add following in your
settings.py

.. code:: python

    FRIENDLY_ERRORS = {
        FIELD_ERRORS = {
            'CharField': {'required': 10, 'null':11, 'blank': 12, 'max_length': 13, 'min_length': 14}
        }
        VALIDATOR_ERRORS = {
            'UniqueValidator': 50
        },
        EXCEPTION_DICT = {
            'PermissionDenied': 100
        }
    }

Custom serializer validation
----------------------------

If you need custom field validation or validation for whole serializer register your validation in serializer class

.. code:: python

    class PostSerializer(FriendlyErrorMessagesMixin,
                         serializers.ModelSerializer):
        class Meta:
            model = Comment

        def validate_title(self, value):
            if value[0] != value[0].upper():
                raise ValidationError('First letter must be an uppercase')
            return value

        def validate(self, attrs):
            category = attrs.get('category)
            title = attrs.get('title')
            if category and category not in title:
                raise ValidationError('Title has to include category')
            return attrs

        FIELD_VALIDATION_ERRORS = {'validate_title': 5000} # register your own validation method and assign it to error code
        NON_FIELD_ERRORS = {'Title has to include category': 8000} # register non field error messages and assign it to error code

If you want to raise field error in validate method use register_error method provided by a mixin

.. code:: python

    class PostSerializer(FriendlyErrorMessagesMixin,
                         serializers.ModelSerializer):
        class Meta:
            model = Comment

        def validate(self, attrs):
            category = attrs.get('category')
            title = attrs.get('title')
            if category and category not in title:
                self.register_error(error_message='Title has to include category',
                                    error_code=8000,
                                    field_name='title')
            return attrs

Error codes not related to serializer validation
------------------------------------------------

To turn other type of errors responses into friendly errors responses with error codes
add this exception handler to your REST_FRAMEWORK settings

.. code:: python

    REST_FRAMEWORK = {
        'EXCEPTION_HANDLER':
        'rest_framework_friendly_errors.handlers.friendly_exception_handler'
    }

Default error codes
-------------------

Following conventions were used:

1xxx - Are reserved for non field errors

2xxx - Are reserved for field errors

3xxx - Are reserved for validator errors

4xxx - Are reserved for other errors not related to serializer validation

Default field error codes
-------------------------

Field is required

- 2001: BooleanField, NullBooleanField
- 2002: CharField, EmailField, RegexField, SlugField, URLField, UUIDField, FilePathField, IPAddressField
- 2003: IntegerField, FloatField, DecimalField
- 2004: ChoiceField, MultipleChoiceField
- 2005: FileField, ImageField
- 2006: ListField, DictField, JSONField
- 2007: StringRequiredField, PrimaryKeyRelatedField, HyperlinkedRelatedField, SlugRelatedField, HyperlinkedIdentityField, ManyRelatedField
- 2008: ReadOnlyField, HiddenField, ModelField, SerializerMethodField

Field data is invalid (invalid regex, string instead of number, date, etc.)

- 2011: BooleanField, NullBooleanField
- 2012: EmailField, RegexField, SlugField, URLField, UUIDField, IPAddressField
- 2013: IntegerField, FloatField, DecimalField
- 2014: FileField, ImageField
- 2015: DateTimeField, DateField, TimeField, DurationField

Field data cannot be null

- 2021: BooleanField, NullBooleanField
- 2022: CharField, EmailField, RegexField, SlugField, URLField, UUIDField, FilePathField, IPAddressField
- 2023: IntegerField, FloatField, DecimalField
- 2024: ChoiceField, MultipleChoiceField
- 2025: FileField, ImageField
- 2026: ListField, DictField, JSONField
- 2027: StringRequiredField, PrimaryKeyRelatedField, HyperlinkedRelatedField, SlugRelatedField, HyperlinkedIdentityField, ManyRelatedField
- 2028: ReadOnlyField, HiddenField, ModelField, SerializerMethodField

Field data cannot be blank

- 2031: CharField, EmailField, RegexField, SlugField, URLField, UUIDField, IPAddressField

Field data is too long string

- 2041: CharField, EmailField, RegexField, SlugField, URLField, UUIDField, IPAddressField
- 2042: IntegerField, FloatField, DecimalField
- 2043: FileField, ImageField

Field data is too short string

- 2051: CharField, EmailField, RegexField, SlugField, URLField, UUIDField, IPAddressField

Field data is too big number

- 2061: IntegerField, FloatField, DecimalField

Field data is too small number

- 2071: IntegerField, FloatField, DecimalField

Field data do not match any value from available choices

- 2081: ChoiceField, MultipleChoiceField
- 2082: FilePathField
- 2083: ManyRelatedField

Field is empty

- 2091: FileField, ImageField
- 2092: MultipleChoiceField
- 2093: ManyRelatedField

File has no name

- 2101: FileField, ImageField

File is an invalid image

- 2111: ImageField

Field is not a list

- 2121: MultipleChoiceField
- 2122: ListField
- 2123: ManyRelatedField

Field is not a dict

- 2131: DictField

Field is not a json

- 2141: JSONField

Field does not exist (invalid hyperlink, primary key, etc.)

- 2151: PrimaryKeyRelatedField, HyperlinkedRelatedField, SlugRelatedField, HyperlinkedIdentityField

Incorrect type for relation key

- 2161: PrimaryKeyRelatedField, HyperlinkedRelatedField, SlugRelatedField, HyperlinkedIdentityField

Couldn't match url or name to a view

- 2171: HyperlinkedRelatedField, HyperlinkedIdentityField

Expected a DateTime, got Date

- 2181: DateTimeField

Excpected a Date, got DateTime

- 2191: DateField

Too many digits for defined Decimal

- 2201: DecimalField

Too many whole digits for defined Decimal

- 2211: DecimalField

Too many decimal digits for defined Decimal

- 2221: DecimalField

Default built-in validators error codes
---------------------------------------

- UniqueValidator: 3001
- UniqueTogetherValidator: 3003
- UniqueForDateValidator: 3004
- UniqueForMonthValidator: 3004
- UniqueForYearValidator: 3005
- RegexValidator: 3006
- EmailValidator: 3007
- URLValidator: 3008
- MaxValueValidator: 3009
- MinValueValidator: 3010
- MaxLengthValidator: 3011
- MinLengthValidator: 3012
- DecimalValidator: 3013
- validate_email: 3014
- validate_slug: 3015
- validate_unicode_slug: 3016
- validate_ipv4_address: 3017
- validate_ipv46_address: 3018
- validate_comma_separated_integer_list: 3019
- int_list_validator: 3020

Other error codes not related to serializer validation
------------------------------------------------------
- Server Error: 4000
- Parser Error (exception was raised by Parser class): 4001,
- Authentication Failed (invalid credentials were provided): 4002,
- Not Authenticated (no credentials were provided): 4003,
- Not Found: 4004,
- Permission Denied: 4005,
- Method Not Allowed (invalid HTTP method): 4006,
- Not Acceptable (Could not satisfy the request Accept header): 4007,
- Unsupported Media-Type: 4008,
- Throttled (Too many requests): 4009

.. _Django Rest framework: http://django-rest-framework.org/