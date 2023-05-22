import os

import clip
import torch


def __get_torch_model__():

    ml_path = "/SearchService/core/ml_models"
    model_file = f"{ml_path}/cmodel.pth"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    if os.path.isfile(model_file):
        cmodel = torch.load(model_file)
    else:
        cmodel, _ = clip.load("ViT-B/32", device=device)
        torch.save(cmodel, model_file)

    return cmodel


class ImageSearch:
    def __init__(self, image_vectors):
        self.image_vectors = image_vectors
        self.cmodel = __get_torch_model__()

    def _encode_text(self, text):
        return self.cmodel.encode_text(clip.tokenize(text))

    def get_scores(self, text):
        scores = self.image_vectors @ self._encode_text(text).t()
        return scores.squeeze().argsort(descending=True)[:10]

