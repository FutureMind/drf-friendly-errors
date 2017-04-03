from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework_friendly_errors.utils import update_field_settings


USER_SETTINGS = getattr(settings, 'FRIENDLY_ERRORS', {})

USER_FRIENDLY_FIELD_ERRORS = USER_SETTINGS.get('FIELD_ERRORS', {})
USER_NON_FIELD_ERRORS = USER_SETTINGS.get('NON_FIELD_ERRORS', {})
USER_VALIDATOR_ERRORS = USER_SETTINGS.get('VALIDATOR_ERRORS', {})
USER_EXCEPTION_DICT = USER_SETTINGS.get('EXCEPTION_DICT', {})

VALIDATION_FAILED_CODE = USER_SETTINGS.get('VALIDATION_FAILED_CODE', 1000)
VALIDATION_FAILED_MESSAGE = USER_SETTINGS.get('VALIDATION_FAILED_MESSAGE',
                                              _('Validation Failed'))

CATCH_ALL_EXCEPTIONS = USER_SETTINGS.get(
    'CATCH_ALL_EXCEPTIONS', False)

FRIENDLY_FIELD_ERRORS = {
    'BooleanField': {'required': 2001, 'invalid': 2011, 'null': 2021},
    'NullBooleanField': {'required': 2001, 'invalid': 2011, 'null': 2021},

    'CharField': {'required': 2002, 'null': 2022, 'blank': 2031,
                  'max_length': 2041, 'min_length': 2051},
    'EmailField': {'required': 2002, 'invalid': 2012, 'null': 2022,
                   'blank': 2031, 'max_length': 2041, 'min_length': 2051},
    'RegexField': {'required': 2002, 'invalid': 2012, 'null': 2022,
                   'blank': 2031, 'max_length': 2041, 'min_length': 2051},
    'SlugField': {'required': 2002, 'invalid': 2012, 'null': 2022,
                  'blank': 2031, 'max_length': 2041, 'min_length': 2051},
    'URLField': {'required': 2002, 'invalid': 2012, 'null': 2022,
                 'blank': 2031, 'max_length': 2041, 'min_length': 2051},
    'UUIDField': {'required': 2002, 'invalid': 2012, 'null': 2022,
                  'blank': 2031, 'max_length': 2041, 'min_length': 2051},
    'FilePathField': {'required': 2002, 'null': 2022, 'invalid_choice': 2082},
    'IPAddressField': {'required': 2002, 'invalid': 2012, 'null': 2022,
                       'blank': 2031, 'max_length': 2041, 'min_length': 2051},

    'IntegerField': {'required': 2003, 'invalid': 2013, 'null': 2023,
                     'max_string_length': 2042, 'min_value': 2071,
                     'max_value': 2061},
    'FloatField': {'required': 2003, 'invalid': 2013, 'null': 2003,
                   'max_string_length': 2042, 'min_value': 2071,
                   'max_value': 2061},
    'DecimalField': {'required': 2003, 'invalid': 2013, 'null': 2003,
                     'max_string_length': 2042, 'min_value': 2071,
                     'max_value': 2061, 'max_whole_digits': 2011,
                     'max_digits': 2012, 'max_decimal_places': 2013},

    'ChoiceField': {'required': 2004, 'null': 2024, 'invalid_choice': 2081},
    'MultipleChoiceField': {'required': 2004, 'null': 2024,
                            'invalid_choice': 2081, 'not_a_list': 2121,
                            'empty': 2092},

    'FileField': {'required': 2005, 'invalid': 2014, 'null': 2025,
                  'max_length': 2043, 'empty': 2091, 'no_name': 2101},
    'ImageField': {'required': 2005, 'invalid': 2014, 'null': 2025,
                   'max_length': 2043, 'empty': 2091, 'no_name': 2101,
                   'invalid_image': 2111},

    'ListField': {'required': 2006, 'null': 2026, 'not_a_list': 2122,
                  'empty': 2015, "max_length": 2041, "min_length": 2051},
    'DictField': {'required': 2006, 'null': 2026, 'not_a_dict': 2131,
                  'empty': 2015},
    'JSONField': {'required': 2006, 'invalid': 2141, 'null': 2026},

    'StringRequiredField': {'required': 2007, 'null': 2027},
    'PrimaryKeyRelatedField': {'required': 2007, 'null': 2027,
                               'does_not_exist': 2151, 'incorrect_type': 2161},
    'HyperlinkedRelatedField': {'required': 2007, 'null': 2027,
                                'does_not_exist': 2151, 'incorrect_type': 2161,
                                'incorrect_match': 2171, 'no_match': 2171},
    'SlugRelatedField': {'required': 2007, 'invalid': 2002, 'null': 2027,
                         'does_not_exist': 2151, 'incorrect_type': 2161},
    'HyperlinkedIdentityField': {'required': 2001, 'null': 2027,
                                 'does_not_exist': 2151, 'incorrect_type': 2161,
                                 'incorrect_match': 2171, 'no_match': 2171},
    'ManyRelatedField': {'required': 2007, 'null': 2027,
                         'invalid_choice': 2083, 'not_a_list': 2123,
                         'empty': 2093},

    'ReadOnlyField': {'required': 2008, 'null': 2028},
    'HiddenField': {'required': 2008, 'null': 2028},
    'ModelField': {'required': 2008, 'null': 2028, 'max_length': 2041},
    'SerializerMethodField': {'required': 2008, 'null': 2028},

    'DateTimeField': {'invalid': 2015, 'date': 2181},
    'DateField': {'invalid': 2015, 'datetime': 2191},
    'TimeField': {'invalid': 2015},
    'DurationField': {'invalid': 2015},
}

FRIENDLY_FIELD_ERRORS = update_field_settings(FRIENDLY_FIELD_ERRORS,
                                              USER_FRIENDLY_FIELD_ERRORS)

INVALID_DATA_MESSAGE = 'Invalid data. Expected a dictionary, but got {data_type}.'

FRIENDLY_NON_FIELD_ERRORS = {
    'invalid': 1001
}

FRIENDLY_NON_FIELD_ERRORS.update(USER_NON_FIELD_ERRORS)

FRIENDLY_VALIDATOR_ERRORS = {
    'UniqueValidator': 3001,
    'UniqueTogetherValidator': 3003,
    'UniqueForDateValidator': 3004,
    'UniqueForMonthValidator': 3004,
    'UniqueForYearValidator': 3005,
    'RegexValidator': 3006,
    'EmailValidator': 3007,
    'URLValidator': 3008,
    'MaxValueValidator': 3009,
    'MinValueValidator': 3010,
    'MaxLengthValidator': 3011,
    'MinLengthValidator': 3012,
    'DecimalValidator': 3013,
    'validate_email': 3014,
    'validate_slug': 3015,
    'validate_unicode_slug': 3016,
    'validate_ipv4_address': 3017,
    'validate_ipv46_address': 3018,
    'validate_comma_separated_integer_list': 3019,
    'int_list_validator': 3020,
}

FRIENDLY_VALIDATOR_ERRORS.update(USER_VALIDATOR_ERRORS)

FRIENDLY_EXCEPTION_DICT = {
    'APIException': 4000,
    'ParseError': 4001,
    'AuthenticationFailed': 4002,
    'NotAuthenticated': 4003,
    'PermissionDenied': 4004,
    'NotFound': 4005,
    'MethodNotAllowed': 4006,
    'NotAcceptable': 4007,
    'UnsupportedMediaType': 4008,
    'Throttled': 4009
}
FRIENDLY_EXCEPTION_DICT.update(USER_EXCEPTION_DICT)
