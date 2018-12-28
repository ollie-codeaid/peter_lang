from django.urls import path

from .views import (
        ArtworkCreate,
        ArtworkDetail,
        ArtworkList,
)

app_name = 'artworks'
urlpatterns = [
    path('', ArtworkList.as_view(), name='list'),
    path('create', ArtworkCreate.as_view(), name='create'),
    path('<str:slug>/', ArtworkDetail.as_view(), name='detail'),
]
