from django.conf import settings

USER_SETTINGS = getattr(settings, 'FRIENDLY_ERRORS', {})

USER_FRIENDLY_FIELD_ERRORS = USER_SETTINGS.get('FIELD_ERRORS', {})
USER_NON_FIELD_ERRORS = USER_SETTINGS.get('NON_FIELD_ERRORS', {})
USER_VALIDATOR_ERRORS = USER_SETTINGS.get('VALIDATOR_ERRORS', {})

VALIDATION_FAILED_CODE = USER_SETTINGS.get('VALIDATION_FAILED_CODE', 1000)
VALIDATION_FAILED_MESSAGE = USER_SETTINGS.get('VALIDATION_FAILED_MESSAGE',
                                              'Validation Failed')

FRIENDLY_FIELD_ERRORS = {
    'BooleanField': {'required': 2001, 'invalid': 2002, 'null': 2003},
    'NullBooleanField': {'required': 2001, 'invalid': 2002, 'null': 2003},

    'CharField': {'required': 2001, 'null': 2003, 'blank': 2004,
                  'max_length': 2005, 'min_length': 2006},
    'EmailField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                   'blank': 2004, 'max_length': 2005, 'min_length': 2006},
    'RegexField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                   'blank': 2004, 'max_length': 2005, 'min_length': 2006},
    'SlugField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                  'blank': 2004, 'max_length': 2005, 'min_length': 2006},
    'URLField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                 'blank': 2004, 'max_length': 2005, 'min_length': 2006},
    'UUIDField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                  'blank': 2004, 'max_length': 2005, 'min_length': 2006},
    'FilePathField': {'required': 2001, 'null': 2003, 'invalid_choice': 2007},
    'IPAddressField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                       'blank': 2004, 'max_length': 2005, 'min_length': 2006},

    'IntegerField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                     'max_string_length': 2008, 'min_value': 2009,
                     'max_value': 2010},
    'FloatField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                   'max_string_length': 2008, 'min_value': 2009,
                   'max_value': 2010},
    'DecimalField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                     'max_string_length': 2008, 'min_value': 2009,
                     'max_value': 2010, 'max_whole_digits': 2011,
                     'max_digits': 2012, 'max_decimal_places': 2013},

    'ChoiceField': {'required': 2001, 'null': 2003, 'invalid_choice': 2007},
    'MultipleChoiceField': {'required': 2001, 'null': 2003,
                            'invalid_choice': 2007, 'not_a_list': 2014,
                            'empty': 2015},

    'FileField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                  'max_length': 2005, 'empty': 2015, 'no_name': 2016},
    'ImageField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                   'max_length': 2005, 'empty': 2015, 'no_name': 2016,
                   'invalid_image': 2017},

    'ListField': {'required': 2001, 'null': 2003, 'not_a_list': 2014,
                  'empty': 2015},
    'DictField': {'required': 2001, 'null': 2003, 'not_a_dict': 2016,
                  'empty': 2015},
    'JSONField': {'required': 2001, 'invalid': 2002, 'null': 2003},

    'StringRequiredField': {'required': 2001, 'null': 2003},
    'PrimaryKeyRelatedField': {'required': 2001, 'null': 2003,
                               'does_not_exist': 2017, 'incorrect_type': 2018},
    'HyperlinkedRelatedField': {'required': 2001, 'null': 2003,
                                'does_not_exist': 2017, 'incorrect_type': 2018,
                                'incorrect_match': 2019, 'no_match': 2020},
    'SlugRelatedField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                         'does_not_exist': 2017, 'incorrect_type': 2018},
    'HyperlinkedIdentityField': {'required': 2001, 'null': 2003,
                                 'does_not_exist': 2017, 'incorrect_type': 2018,
                                 'incorrect_match': 2019, 'no_match': 2020},
    'ManyRelatedField': {'required': 2001, 'null': 2003,
                         'invalid_choice': 2007, 'not_a_list': 2014,
                         'empty': 2015},

    'ReadOnlyField': {'required': 2001, 'null': 2003},
    'HiddenField': {'required': 2001, 'null': 2003},
    'ModelField': {'required': 2001, 'null': 2003, 'max_length': 2005},
    'SerializerMethodField': {'required': 2001, 'null': 2003},

    'DateTimeField': {'invalid': 2002, 'date': 2021},
    'DateField': {'invalid': 2002, 'date': 2022},
    'TimeField': {'invalid': 2002},
    'DurationField': {'invalid': 2002},
}

FRIENDLY_FIELD_ERRORS.update(USER_FRIENDLY_FIELD_ERRORS)

INVALID_DATA_MESSAGE = 'Invalid data. Expected a dictionary, but got {data_type}.'

FRIENDLY_NON_FIELD_ERRORS = {
    'invalid': 1001
}

FRIENDLY_NON_FIELD_ERRORS.update(USER_NON_FIELD_ERRORS)


FRIENDLY_VALIDATOR_ERRORS = {
    'RegexValidator': 9000,
    'UniqueValidator': 9001,
    'UniqueTogetherValidator': 9002,
    'UniqueForDateValidator': 9003,
    'UniqueForMonthValidator': 9004,
    'UniqueForYearValidator': 9005,
    'EmailValidator': 9006,
    'URLValidator': 9007,
    'MaxValueValidator': 9008,
    'MinValueValidator': 9009,
    'MaxLengthValidator': 9010,
    'MinLengthValidator': 9011,
    'DecimalValidator': 9012,
    'validate_email': 9006,
    'validate_slug': 9000,
    'validate_unicode_slug': 9000,
    'validate_ipv4_address': 9000,
    'validate_ipv46_address': 9000,
    'validate_comma_separated_integer_list': 9000,
    'int_list_validator': 9000,
}
FRIENDLY_VALIDATOR_ERRORS.update(USER_VALIDATOR_ERRORS)
