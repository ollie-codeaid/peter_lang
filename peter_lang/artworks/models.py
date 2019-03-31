from django.db import models


class Artwork(models.Model):
    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField()
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name
