from django.db import models

from core.db_models.base import AbstractBaseModel


class ImageVector(AbstractBaseModel):
    filename = models.CharField(max_length=255)
    tensor_blob = models.BinaryField()
    tensor_shape = models.CharField(max_length=255)
