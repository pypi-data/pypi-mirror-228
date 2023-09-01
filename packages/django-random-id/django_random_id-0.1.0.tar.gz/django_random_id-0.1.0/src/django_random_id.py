import uuid
import string
from random import randint,choices
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.conf import settings


__author__ = "Serdar Ilarslan"
__version__ = "0.0.1"

try:
    digits = settings.RANDOM_ID_MODEL_LENGTH
except ImproperlyConfigured:
    digits = 16


def generate_random_id(is_alphanumeric=False):
    if is_alphanumeric:
        return ''.join(choices(string.ascii_letters + string.digits, k=digits))
    return randint(10 ** (digits - 1), 10 ** digits)


class RandomIDModel(models.Model):
    """Provides a custom ID primary key field."""

    class Meta:
        abstract = True

    id = models.BigIntegerField(primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        """If the user hasn't provided an ID, generate a random Int."""

        if not self.id:
            is_unique = False
            while not is_unique:
                random_id = generate_random_id()
                is_unique = not self.__class__.objects.filter(id=random_id).exists()
            self.id = random_id
        super(RandomIDModel, self).save(*args, **kwargs)


class RandomAlphaNumIDModel(models.Model):
    """Provides a ALPHANUMERIC ID primary key field."""

    class Meta:
        abstract = True

    id = models.CharField(primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        """If the user hasn't provided an ID, generate a random Int."""

        if not self.id:
            is_unique = False
            while not is_unique:
                random_id = generate_random_id(is_alphanumeric=True)
                is_unique = not self.__class__.objects.filter(id=random_id).exists()
            self.id = random_id
        super(RandomAlphaNumIDModel, self).save(*args, **kwargs)
