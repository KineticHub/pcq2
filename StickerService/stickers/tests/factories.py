import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import file
from rest_framework.authtoken.models import Token

from stickers.models import Sticker, StickerQuery

fake = Faker()
fake.add_provider(file.Provider)
Faker.seed(524)


class StickerFactory(DjangoModelFactory):
    filename = factory.LazyAttribute(lambda _: fake.file_name(extension='jpg'))

    class Meta:
        model = Sticker


class StickerQueryFactory(DjangoModelFactory):
    query = factory.Sequence(lambda n: "query_%d" % n)

    class Meta:
        model = StickerQuery


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = Token
