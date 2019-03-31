import pytest
from unittest import mock

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from ..models import Article
from ..views import (
        ArticleCreate,
        ArticleList,
        ArticleDetail,
        ArticleDelete,
        ArticleUpdate,
        ArticlePublicList,
)
from .factories import ArticleFactory
from peter_lang.artworks.tests.factories import ArtworkFactory

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
        request = request_factory.get('/articles/create/')
        self._test_view_redirects_anonymous_user(request)

    def test_POST_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        request = request_factory.post('/articles/create/')
        self._test_view_redirects_anonymous_user(request)

    def test_GET_logged_in_user_is_not_redirected(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        request = request_factory.get('/articles/create/')
        request.user = user

        response = ArticleCreate.as_view()(request)

        assert response.status_code == 200

    def test_POST_creates_new_article(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory
    ):
        artwork = ArtworkFactory()
        data = {
                'name': 'Test Article',
                'slug': 'test-article',
                'text': 'Some test text',
                'preview_text': 'Some preview text',
                'preview_picture': artwork.pk,
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
                '/articles/create/',
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
                '/articles/create/',
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
                '/articles/create/',
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

    def test_GET_returns_expected_article(
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


class TestArticlePublicList:
    def test_GET_anonymous_returns_expected_article(self, request_factory: RequestFactory):
        article = ArticleFactory()
        request = request_factory.get('/articles/')
        request.user = AnonymousUser()

        response = ArticlePublicList.as_view()(request)

        assert response.status_code == 200
        article_list = response.context_data['object_list']
        assert article_list.count() == 1
        assert article == article_list.first()

    def test_GET_returns_expected_article(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        article = ArticleFactory()
        request = request_factory.get('/articles/')
        request.user = user

        response = ArticlePublicList.as_view()(request)

        assert response.status_code == 200
        article_list = response.context_data['object_list']
        assert article_list.count() == 1
        assert article == article_list.first()

    def test_private_article_not_shown(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        article = ArticleFactory()
        ArticleFactory(is_published=False)
        request = request_factory.get('/articles/')
        request.user = user

        response = ArticlePublicList.as_view()(request)

        assert response.status_code == 200
        article_list = response.context_data['object_list']
        assert article_list.count() == 1
        assert article == article_list.first()

    def test_articles_returned_in_descending_date_order(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        oldest_article = ArticleFactory()
        latest_article = ArticleFactory()
        request = request_factory.get('/articles/')
        request.user = user

        response = ArticlePublicList.as_view()(request)

        assert response.status_code == 200
        article_list = response.context_data['object_list']
        assert article_list.count() == 2
        assert oldest_article == article_list.last()
        assert latest_article == article_list.first()


class TestArticleDetail:

    def test_GET_returns_expected_article(
            self,
            request_factory: RequestFactory,
    ):
        article = ArticleFactory()
        request = request_factory.get('/articles/')
        request.user = AnonymousUser()

        response = ArticleDetail.as_view()(request, slug=article.slug)

        assert response.status_code == 200
        assert article == response.context_data['object']


class TestArticleDelete(AnonymousUserRedirectMixin):
    view_class = ArticleDelete

    def test_GET_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        article = ArticleFactory()
        request = request_factory.get(f'/articles/{article.slug}/delete')
        self._test_view_redirects_anonymous_user(request)

    def test_POST_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        article = ArticleFactory()
        request = request_factory.post(f'/articles/{article.slug}/delete')
        self._test_view_redirects_anonymous_user(request)

    def test_authenticated_user_can_delete(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        article = ArticleFactory()
        request = request_factory.post(f'/articles/{article.slug}/delete')
        request.user = user

        response = ArticleDelete.as_view()(request, slug=article.slug)

        assert Article.objects.count() == 0


class TestArticleUpdate(AnonymousUserRedirectMixin):
    view_class = ArticleUpdate

    def test_GET_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        article = ArticleFactory()
        request = request_factory.get(f'/articles/{article.slug}/update')
        self._test_view_redirects_anonymous_user(request)

    def test_POST_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        article = ArticleFactory()
        request = request_factory.post(f'/articles/{article.slug}/update')
        self._test_view_redirects_anonymous_user(request)

    def test_authenticated_user_can_update(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        article = ArticleFactory()
        artwork = ArtworkFactory()
        data = {
                'name': 'Test Article',
                'slug': 'test-article',
                'text': 'Some test text',
                'preview_text': 'Some preview text',
                'preview_picture': artwork.pk,
        }
        request = request_factory.post(f'/articles/{article.slug}/update', data)
        request.user = user

        ArticleUpdate.as_view()(request, slug=article.slug)

        article.refresh_from_db()
        assert article.name == 'Test Article'
        assert article.slug == 'test-article'
        assert article.text == 'Some test text'
        assert article.preview_text == 'Some preview text'
        assert article.preview_picture == artwork
