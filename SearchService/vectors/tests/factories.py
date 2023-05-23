from factory.django import DjangoModelFactory
from faker import Faker

from vectors.models import ImageVector


class ImageVectorFactory(DjangoModelFactory):
    filename = Faker().file_name(category='image')
    tensor_blob = Faker().binary(length=64)

    class Meta:
        model = ImageVector