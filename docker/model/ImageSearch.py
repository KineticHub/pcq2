# #!/usr/bin/env python
# # coding: utf-8
#
# # In[1]:
#
#
# get_ipython().system('pip install openai-clip')
# get_ipython().system('pip install torch torchvision')
# get_ipython().system('pip install ftfy regex tqdm')
#
#
# # ### Load the CLIP model weights
#
# # In[2]:
#
#
# import torch
# import clip
# from PIL import Image
#
# device = "cuda" if torch.cuda.is_available() else "cpu"
# cmodel, preprocess = clip.load("ViT-B/32", device=device)
#
#
# # ### Define functions to map image/text to vector
#
# # In[3]:
#
#
# def get_vector_for_image(image):
#     return cmodel.encode_image(preprocess(image).unsqueeze(0))
#
# def get_vector_for_text(text):
#     return cmodel.encode_text(clip.tokenize(text))
#
#
# # ### Test those functions
# #
#
# # In[4]:
#
#
# from PIL import Image
# image = Image.open('/Users/sisovina/Downloads/vinay_canny.jpg')
# get_vector_for_image(image).shape
#
#
# # In[5]:
#
#
# get_vector_for_text('a cat').shape
#
#
# # ### Load the images and calculate the image vectors
#
# # In[6]:
#
#
# from glob import glob
#
# filepaths = glob('./val2014/*.jpg')
# len(filepaths)
#
#
# # In[7]:
#
#
# image_vectors = torch.cat([get_vector_for_image(
#     Image.open(fp)
# ) for fp in filepaths])
#
# image_vectors.shape
#
#
# # ### Change the L2 norm of vectors to 1
#
# # In[8]:
#
#
# image_vectors /= image_vectors.norm(dim=-1, keepdim=True)
#
#
# # ### Create the "search engine"
#
# # In[9]:
#
#
# class ImageSearch():
#     def __init__(self, image_vectors):
#         self.image_vectors = image_vectors
#
#     def _encode_text(self, text):
#         return cmodel.encode_text(clip.tokenize(text))
#
#     def __call__(self, text):
#         scores = self.image_vectors @ self._encode_text(text).t()
#         return scores.squeeze().argsort(descending=True)[:10]
#
#
# # In[10]:
#
#
# search = ImageSearch(image_vectors)
#
#
# # ### Let's test it now
#
# # In[11]:
#
#
# search('cat in a park')
#
#
# # In[12]:
#
#
# Image.open(filepaths[178])
#
#
# # In[13]:
#
#
# indices = search('a cute baby')
# Image.open(filepaths[indices[0]])
#
#
# # In[ ]:
#
#
#
#
