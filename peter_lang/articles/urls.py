from django.urls import path

from .views import (
        ArticleCreate,
        ArticleList,
        ArticleDetail,
        ArticleUpdate,
        ArticleDelete,
        ArticlePublicList,
)

app_name = 'articles'
urlpatterns = [
    path('', ArticlePublicList.as_view(), name='list'),
    path('create', ArticleCreate.as_view(), name='create'),
    path('manage', ArticleList.as_view(), name='manage'),
    path('<str:slug>/', ArticleDetail.as_view(), name='detail'),
    path('<str:slug>/update', ArticleUpdate.as_view(), name='update'),
    path('<str:slug>/delete', ArticleDelete.as_view(), name='delete'),
]
