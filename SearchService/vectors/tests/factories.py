import factory
from factory.django import DjangoModelFactory
from faker import Faker

from vectors.models import ImageVector


class ImageVectorFactory(DjangoModelFactory):
    filename = Faker().file_name(category='audio')
    tensor_blob = Faker().binary(length=64)
    # tensor_shape = Faker().in

    class Meta:
        model = ImageVector