from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
        CreateView,
)
from django.urls import reverse_lazy

from .forms import ArtworkForm
from .models import Artwork


class ArtworkCreate(
        LoginRequiredMixin,
        CreateView):
    model = Artwork
    form_class = ArtworkForm
    login_url = '/accounts/login/'
    success_url = reverse_lazy('home')

