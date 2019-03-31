from django.forms import ModelForm

from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = [
                'name',
                'slug',
                'text',
                'preview_picture',
                'preview_text',
                'is_published',
        ]
