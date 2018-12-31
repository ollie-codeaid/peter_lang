import pytest
from unittest import mock

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from ..models import Article
from ..views import (
        ArticleCreate,
        ArticleList,
)
from .factories import ArticleFactory

pytestmark = pytest.mark.django_db


class AnonymousUserRedirectMixin:

    @property
    def view_class(self):
        raise NotImplementedError

    def _test_view_redirects_anonymous_user(self, request):
        request.user = AnonymousUser()

        response = self.view_class.as_view()(request)

        assert response.status_code == 302
        assert response.url.startswith('/accounts/login/?next=')


class TestArticleCreate(AnonymousUserRedirectMixin):
    view_class = ArticleCreate

    def test_GET_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        request = request_factory.get('/article/create/')
        self._test_view_redirects_anonymous_user(request)

    def test_POST_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        request = request_factory.post('/article/create/')
        self._test_view_redirects_anonymous_user(request)

    def test_GET_logged_in_user_is_not_redirected(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        request = request_factory.get('/article/create/')
        request.user = user

        response = ArticleCreate.as_view()(request)

        assert response.status_code == 200

    def test_POST_creates_new_article(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory
    ):
        data = {
                'name': 'Test Article',
                'slug': 'test-article',
                'text': 'Some test text',
        }
        request = request_factory.post(
                '/article/create/',
                data,
        )
        request.user = user

        response = ArticleCreate.as_view()(request)

        assert response.status_code == 302
        assert Article.objects.count() == 1

    def test_POST_requires_name(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        data = {
                'slug': 'test-article',
                'text': 'Some test text',
        }
        request = request_factory.post(
                '/article/create/',
                data,
        )
        request.user = user

        response = ArticleCreate.as_view()(request)

        assert response.status_code == 200
        assert Article.objects.count() == 0
        assert 'This field is required.' in response.context_data['form'].errors['name']

    def test_POST_requires_slug(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        data = {
                'name': 'Test article',
                'text': 'Some test text',
        }
        request = request_factory.post(
                '/article/create/',
                data,
        )
        request.user = user

        response = ArticleCreate.as_view()(request)

        assert response.status_code == 200
        assert Article.objects.count() == 0
        assert 'This field is required.' in response.context_data['form'].errors['slug']

    def test_POST_requires_text(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        data = {
                'name': 'Test Article',
                'slug': 'test-article',
        }
        request = request_factory.post(
                '/article/create/',
                data,
        )
        request.user = user

        response = ArticleCreate.as_view()(request)

        assert response.status_code == 200
        assert Article.objects.count() == 0
        assert 'This field is required.' in response.context_data['form'].errors['text']


class TestArticleList(AnonymousUserRedirectMixin):
    view_class = ArticleList

    def test_GET_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        request = request_factory.get('/articles/manage/')
        self._test_view_redirects_anonymous_user(request)

    def test_GET_returns_expected_artwork(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        article = ArticleFactory()
        request = request_factory.get('/articles/manage/')
        request.user = user

        response = ArticleList.as_view()(request)

        assert response.status_code == 200
        article_list = response.context_data['object_list']
        assert article_list.count() == 1
        assert article == article_list.first()


