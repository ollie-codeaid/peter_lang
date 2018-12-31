from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
        CreateView,
)
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .forms import ArticleForm
from .models import Article


class ArticleCreate(
        LoginRequiredMixin,
        CreateView
):
    model = Article
    form_class = ArticleForm
    login_url = '/accounts/login/'
    success_url = reverse_lazy('home')


class ArticleList(
        LoginRequiredMixin,
        ListView,
):
    model = Article
    template_name = 'articles/article_management_list.html'

