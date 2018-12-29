import pytest

from ..models import Article

pytestmark = pytest.mark.django_db


def test_article___str___matches_name():
    article = Article(
            name = 'Article',
            text = '',
    )
    article.save()

    assert article.name == str(article)
