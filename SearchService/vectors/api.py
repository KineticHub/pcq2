from io import BytesIO

import torch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from vectors.algos.ImageVectorTextSearch import ImageSearch
from vectors.models import ImageVector


class SearchImageVectors(APIView):
    """
    """
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        """
        """
        vectors = torch.cat([torch.load(BytesIO(vector)).view(torch.Size([512])).unsqueeze(0)
                             for vector in ImageVector.objects.values_list('tensor_blob', flat=True)])
        filenames = ImageVector.objects.values_list('filename', flat=True)
        images = [filenames[int(x)] for x in ImageSearch(vectors).get_scores(request.query_params.get('query'))]
        return Response({"filenames": images})
