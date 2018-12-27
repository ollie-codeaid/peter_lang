from django.forms import ModelForm

from .models import Artwork


class ArtworkForm(ModelForm):
    class Meta:
        model = Artwork
        fields = [
                'name',
                'slug',
                'image',
                'height',
                'width',
                'unit',
                'price',
        ]
