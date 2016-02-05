from __future__ import unicode_literals


class FieldMap(object):
    TIME_FORMAT = 'hh:mm[:ss[.uuuuuu]]'
    DATE_FORMAT = 'YYYY[-MM[-DD]]'
    DATETIME_FORMAT = 'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]'
    DURATION_FORMAT = '[DD] [HH:[MM:]]ss[.uuuuuu]'

    @property
    def field_map(self):
        return {
            'boolean': ['BooleanField', 'NullBooleanField'],
            'string': ['CharField', 'EmailField', 'RegexField', 'SlugField',
                       'URLField', 'UUIDField', 'FilePathField',
                       'IPAddressField'],
            'numeric': ['IntegerField', 'FloatField', 'DecimalField'],
            'date': {'DateTimeField': self.DATETIME_FORMAT,
                     'DateField': self.DATE_FORMAT,
                     'TimeField': self.TIME_FORMAT,
                     'DurationField': self.DURATION_FORMAT},
            'choice': ['ChoiceField', 'MultipleChoiceField'],
            'file': ['FileField', 'ImageField'],
            'composite': ['ListField', 'DictField', 'JSONField'],
            'relation': ['StringRelatedField', 'PrimaryKeyRelatedField',
                         'HyperlinkedRelatedField', 'SlugRelatedField',
                         'HyperlinkedIdentityField', 'ManyRelatedField'],
            'miscellaneous': ['ReadOnlyField', 'HiddenField', 'ModelField',
                              'SerializerMethodField']
        }
