import gc
from io import BytesIO
from pathlib import Path
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand
from vectors.models import ImageVector


class Command(BaseCommand):
    help = "Process image vectors and store in database"

    def handle(self, *args, **options):

        import os
        import pickle

        import torch
        import clip
        from glob import glob
        from PIL import Image

        ml_path = "/SearchService/core/ml_models"
        model_file = f"{ml_path}/cmodel.pth"
        preprocess_file = f"{ml_path}/preprocess.pkl"

        device = "cuda" if torch.cuda.is_available() else "cpu"

        if os.path.isfile(model_file) and os.path.isfile(preprocess_file):
            cmodel = torch.load(model_file)
            with open(preprocess_file, 'rb') as f:
                preprocess = pickle.load(f)
        else:
            cmodel, preprocess = clip.load("ViT-B/32", device=device)
            torch.save(cmodel, model_file)
            with open(preprocess_file, 'wb') as f:
                pickle.dump(preprocess, f)

        def get_vector_for_image(filepath):
            # print(filepath)
            try:
                image = Image.open(filepath)
                return cmodel.encode_image(preprocess(image).unsqueeze(0))
            except Exception:
                print(f"failed on {filepath}")

        def save_vectors(filename):

            image_vectors = torch.cat([get_vector_for_image(fp) for fp in [filename]])
            image_vectors /= image_vectors.norm(dim=-1, keepdim=True)
            size = str(image_vectors[0].size())

            for filename_inside, vector in zip([filename], image_vectors):
                buffer = BytesIO()
                torch.save(vector, buffer)
                ImageVector(filename=Path(filename_inside).name, tensor_blob=buffer.getvalue(), tensor_shape=size).save()
                buffer.close()

            del image_vectors

        filepaths = glob(f"{settings.BASE_DIR}/core/ml_models/images/val2014/*.jpg")

        for file in filepaths:
            if not ImageVector.objects.filter(filename=Path(file).name).exists():
                save_vectors(file)
                sleep(1)

        print("Finished processing images.")
