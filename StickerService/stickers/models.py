from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, SET_NULL, PROTECT

from core.models.base import AbstractBaseModel


class Sticker(AbstractBaseModel):
    filename = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.filename}"


class StickerQuery(AbstractBaseModel):
    query = models.CharField(max_length=255, unique=True)
    usage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.query}"


class StickerQueryScore(AbstractBaseModel):
    query = models.ForeignKey(StickerQuery, on_delete=PROTECT, related_name='query_scores')
    sticker = models.ForeignKey(Sticker, on_delete=CASCADE, related_name='sticker_scores')
    positives = models.PositiveIntegerField(default=0)
    negatives = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('query', 'sticker',)

    def __str__(self):
        return f"{self.sticker}, {self.query}"
