import pytest
from unittest import mock

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory

from ..models import Artwork
from ..views import ArtworkCreate, ArtworkList, ArtworkDetail
from .factories import ArtworkFactory

pytestmark = pytest.mark.django_db

test_image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open('peter_lang/artworks/tests/test_image.jpeg', 'rb').read(),
        content_type='image/jpeg')


class AnonymousUserRedirectMixin:

    @property
    def view_class(self):
        raise NotImplementedError

    @property
    def expected_redirect_url(self):
        raise NotImplementedError

    def _test_view_redirects_anonymous_user(self, request):
        request.user = AnonymousUser()

        response = self.view_class.as_view()(request)

        assert response.status_code == 302
        assert response.url == self.expected_redirect_url


class TestArtworkCreate(AnonymousUserRedirectMixin):
    view_class = ArtworkCreate
    expected_redirect_url = '/accounts/login/?next=/artwork/create/'

    def test_GET_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        request = request_factory.get('/artwork/create/')
        self._test_view_redirects_anonymous_user(request)

    def test_POST_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        request = request_factory.post('/artwork/create/')
        self._test_view_redirects_anonymous_user(request)

    def test_GET_logged_in_user_is_not_redirected(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        request = request_factory.get('/artwork/create/')
        request.user = user

        response = ArtworkCreate.as_view()(request)

        assert response.status_code == 200

    def test_POST_creates_new_artwork(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory
    ):
        data = {
                'name': 'Test Art',
                'slug': 'test-art',
                'image': test_image,
        }
        request = request_factory.post(
                '/artwork/create/',
                data,
        )
        request.user = user

        response = ArtworkCreate.as_view()(request)

        assert response.status_code == 302
        assert Artwork.objects.count() == 1

    def test_POST_requires_name(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        data = {
                'slug': 'test-art',
                'image': test_image,
        }
        request = request_factory.post(
                '/artwork/create/',
                data,
        )
        request.user = user

        response = ArtworkCreate.as_view()(request)

        assert response.status_code == 200
        assert Artwork.objects.count() == 0
        assert 'This field is required.' in response.context_data['form'].errors['name']

    def test_POST_requires_image(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        data = {
                'name': 'Test Art',
                'slug': 'test-art',
        }
        request = request_factory.post(
                '/artwork/create/',
                data,
        )
        request.user = user

        response = ArtworkCreate.as_view()(request)

        assert response.status_code == 200
        assert Artwork.objects.count() == 0
        assert 'This field is required.' in response.context_data['form'].errors['image']


class TestArtworkList(AnonymousUserRedirectMixin):
    view_class = ArtworkList
    expected_redirect_url = '/accounts/login/?next=/artwork/'

    def test_GET_anonymous_user_is_redirected(self, request_factory: RequestFactory):
        request = request_factory.get('/artwork/')
        self._test_view_redirects_anonymous_user(request)

    def test_GET_returns_expected_artwork(
            self,
            user: settings.AUTH_USER_MODEL,
            request_factory: RequestFactory,
    ):
        artwork = ArtworkFactory()
        request = request_factory.get('/artwork')
        request.user = user

        response = ArtworkList.as_view()(request)

        assert response.status_code == 200
        artwork_list = response.context_data['object_list']
        assert artwork_list.count() == 1
        assert artwork == artwork_list.first()


class TestArtworkDetail:

    def test_GET_returns_expected_artwork(
            self,
            request_factory: RequestFactory,
    ):
        artwork = ArtworkFactory()
        request = request_factory.get('/artwork/')
        request.user = AnonymousUser()

        response = ArtworkDetail.as_view()(request, slug=artwork.slug)

        assert response.status_code == 200
        assert artwork == response.context_data['object']
