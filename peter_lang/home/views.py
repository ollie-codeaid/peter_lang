from django.views.generic.list import ListView

from peter_lang.artworks.models import Artwork
from peter_lang.articles.models import Article


class HomeView(ListView):
    model = Artwork
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]

        return context
