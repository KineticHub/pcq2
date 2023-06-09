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
            if not Sticker.objects.filter(filename=Path(filepath).name).exists():
                Sticker(filename=Path(filepath).name).save()
        print("Finished saving stickers to database.")
