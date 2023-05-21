from rest_framework import serializers

from stickers.models import StickerQuery, StickerQueryScore


class StickerQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = StickerQuery
        fields = ["query", "usage"]


class StickerQueryScoreSerializer(serializers.ModelSerializer):
    sticker = serializers.CharField(source='sticker.filename')

    class Meta:
        model = StickerQueryScore
        fields = ["sticker", "positives", "negatives"]
