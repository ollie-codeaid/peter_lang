from django.urls import path

from .views import (
        ArticleCreate,
        ArticleList,
)

app_name = 'articles'
urlpatterns = [
    path('create', ArticleCreate.as_view(), name='create'),
    path('manage', ArticleList.as_view(), name='manage'),
]
