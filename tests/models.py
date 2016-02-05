from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import title


LANGUAGE_CHOICES = (
    ('python', 'Python'),
    ('c++', 'C++'),
    ('java', 'Java'),
    ('ruby', 'Ruby'),
    ('cobol', 'Cobol'),
    ('erlang', 'Erlang')
)


def is_proper_title(value):
    if value and value != title(value):
        raise ValidationError('Incorrect title')


class Snippet(models.Model):
    title = models.CharField(max_length=10, validators=[is_proper_title])
    comment = models.CharField(max_length=255)
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    posted_date = models.DateTimeField()
    watermark = models.CharField(max_length=100, unique=True)
