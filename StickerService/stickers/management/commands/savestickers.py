from glob import glob
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from stickers.models import Sticker


class Command(BaseCommand):
    help = "Save sticker filenames to the database"

    def handle(self, *args, **options):
        stickers = glob(f"{settings.BASE_DIR}/media/images/val2014/*.jpg")
        for filepath in stickers:
            Sticker(filename=Path(filepath).name).save()
