from django.urls import path

from .views import ArtworkCreate

app_name = 'artworks'
urlpatterns = [
    path('create', ArtworkCreate.as_view(), name='create'),
]
