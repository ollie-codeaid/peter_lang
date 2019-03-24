from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
        CreateView,
        DeleteView,
        UpdateView
)
from django.views.generic.detail import DetailView
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
    success_url = reverse_lazy('articles:manage')


class ArticleList(
        LoginRequiredMixin,
        ListView,
):
    model = Article
    template_name = 'articles/article_management_list.html'


class ArticlePublicList(ListView):
    model = Article
    template_name = 'articles/article_list.html'


class ArticleDetail(DetailView):
    model = Article


class ArticleDelete(
        LoginRequiredMixin,
        DeleteView,
):
    model = Article
    success_url = reverse_lazy('articles:manage')


class ArticleUpdate(
        LoginRequiredMixin,
        UpdateView,
):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('articles:manage')
