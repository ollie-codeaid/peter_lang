from factory import DjangoModelFactory, Faker

from ..models import Article


class ArticleFactory(DjangoModelFactory):
    name = Faker('name')
    slug = Faker('slug')
    text = Faker('text')

    class Meta:
        model = Article

