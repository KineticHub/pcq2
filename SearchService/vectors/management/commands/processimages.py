import gc
from io import BytesIO
from pathlib import Path

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
            print(filepath)
            try:
                image = Image.open(filepath)
                return cmodel.encode_image(preprocess(image).unsqueeze(0))
            except Exception:
                print(f"failed on {filepath}")

        def get_vector_for_text(text):
            return cmodel.encode_text(clip.tokenize(text))

        def save_vectors(a, z):

            process_files = []
            for file in filepaths[a:z]:
                if not ImageVector.objects.filter(filename=Path(file).name).exists():
                    process_files.append(file)

            if process_files:

                image_vectors = torch.cat([get_vector_for_image(fp) for fp in process_files])

                image_vectors /= image_vectors.norm(dim=-1, keepdim=True)

                size = str(image_vectors[0].size())
                for file, vector in zip(process_files, image_vectors):
                    buffer = BytesIO()
                    torch.save(vector, buffer)
                    ImageVector(filename=Path(file).name, tensor_blob=buffer.getvalue(), tensor_shape=size).save()
                    buffer.close()

                del image_vectors
            gc.collect()

        filepaths = glob('/code/app/core/ml_models/images/val2014/*.jpg')

        save_vectors(300, 350)