from factory import DjangoModelFactory, Faker
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Artwork

test_image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open('peter_lang/artworks/tests/test_image.jpeg', 'rb').read(),
        content_type='image/jpeg')


class ArtworkFactory(DjangoModelFactory):
    name = Faker('name')
    slug = Faker('slug')
    image = test_image

    class Meta:
        model = Artwork

