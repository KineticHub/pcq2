from django.contrib import admin

from stickers.models import Sticker, StickerQuery, StickerQueryScore


@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ["filename"]
    search_fields = ["filename"]


@admin.register(StickerQuery)
class StickerQueryAdmin(admin.ModelAdmin):
    list_display = ["query", "usage"]
    search_fields = ["query"]


@admin.register(StickerQueryScore)
class StickerQueryScoreAdmin(admin.ModelAdmin):
    list_display = ["sticker", "query", "positives", "negatives"]
    search_fields = ["sticker", "query"]
    list_filter = ["query"]
