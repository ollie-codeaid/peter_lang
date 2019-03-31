import pytest

from django.test import RequestFactory

from ..views import HomeView
from peter_lang.articles.tests.factories import ArticleFactory

pytestmark = pytest.mark.django_db


class TestHomeView:

    def test_latest_public_article_displayed(
            self,
            request_factory: RequestFactory,
    ):
        oldest_article = ArticleFactory()
        latest_article = ArticleFactory()
        private_article = ArticleFactory(is_published=False)

        request = request_factory.get('/')

        response = HomeView.as_view()(request)

        assert response.status_code == 200
        article = response.context_data['latest_article']
        assert latest_article == article
