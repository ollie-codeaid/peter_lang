from django.db import models

from peter_lang.artworks.models import Artwork


class Article(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    preview_picture = models.ForeignKey(Artwork, on_delete=models.SET_NULL, null=True)
    preview_text = models.TextField()
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

