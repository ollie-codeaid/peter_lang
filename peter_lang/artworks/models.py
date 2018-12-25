from django.db import models


class Artwork(models.Model):
    CM = 'CM'
    IN = 'IN'

    UNIT_CHOICES = (
            ('CM', 'cm'),
            ('IN', 'in'),
    )

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    unit = models.CharField(
            max_length=2,
            choices=UNIT_CHOICES,
            default=CM,
            blank=True,
            null=True,
    )
    price = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            blank=True,
            null=True,
    )

    def __str__(self):
        return self.name
