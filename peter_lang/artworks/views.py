from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
        CreateView,
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
    success_url = reverse_lazy('home')


class ArtworkList(
        LoginRequiredMixin,
        ListView,
):
    model = Artwork


class ArtworkDetail(
        DetailView,
):
    model = Artwork
