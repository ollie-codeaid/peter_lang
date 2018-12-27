from django.urls import path

from .views import ArtworkCreate, ArtworkList

app_name = 'artworks'
urlpatterns = [
    path('', ArtworkList.as_view(), name='artwork-list'),
    path('create', ArtworkCreate.as_view(), name='create'),
]
