from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
        CreateView,
        DeleteView,
        UpdateView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .forms import ArtworkForm
from .models import Artwork


class ArtworkCreate(
        LoginRequiredMixin,
        CreateView
):
    model = Artwork
    form_class = ArtworkForm
    login_url = '/accounts/login/'
    success_url = reverse_lazy('artworks:list')


class ArtworkList(
        LoginRequiredMixin,
        ListView,
):
    model = Artwork


class PublicArtworkList(
        ListView,
):
    model = Artwork
    template_name = 'artworks/artwork_carousel.html'


class ArtworkDetail(DetailView):
    model = Artwork


class ArtworkDelete(
        LoginRequiredMixin,
        DeleteView,
):
    model = Artwork
    success_url = reverse_lazy('artworks:list')


class ArtworkUpdate(
        LoginRequiredMixin,
        UpdateView,
):
    model = Artwork
    form_class = ArtworkForm
    success_url = reverse_lazy('artworks:list')
