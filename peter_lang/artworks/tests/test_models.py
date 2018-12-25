import pytest

from ..models import Artwork

pytestmark = pytest.mark.django_db


def test_artwork___str___matches_name():
    artwork = Artwork(
            name='Art',
            slug='art',
    )

    artwork.save()

    assert artwork.name == str(artwork)
