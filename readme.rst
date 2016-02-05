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
                "code" : 2001,
                "field" : "name",
                "message" : "This field is required."
            },
            {
                "code" : 2004,
                "field" : "password",
                "message" : "This field may not be blank."
            },
            {
                "age" : 2003,
                "field" : "age",
                "message" : "This field may not be null."
            },
            {
                "age" : 2005,
                "field" : "description",
                "message" : "Ensure this field has no more than 100 characters."
            },
        ]
    }

Library handles all `Django Rest framework`_ built-in serializer validation.

Requirements
------------
-  Python (2.7, 3.4)
-  Django (1.8, 1.9)
-  Django REST Framework (3.3)

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

If you want to change default library settings and provide your own set of error codes for validators or fields,
configure your own settings

.. code:: python

    FIELD_ERRORS = {
        'CharField': {'required': 10, 'null':11, 'blank': 12, 'max_length': 13, 'min_length': 14}
    }
    VALIDATOR_ERRORS = {
        'UniqueValidator': 50
    }

List of default settings provided by library is listed below:

// TBD

`settings`_

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

        FIELD_VALIDATION_ERRORS = {'validate_title': 5000} # register your own validation method and assnng it to error code
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

.. _Django Rest framework: http://django-rest-framework.org/
.. _settings: https://bitbucket.org/snippets/tlaszczuk/gk4Xz