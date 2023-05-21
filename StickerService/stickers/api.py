from django.db.models import F
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from core.services.search import SearchService

from stickers.models import StickerQuery, Sticker, StickerQueryScore
from stickers.serializers import StickerQuerySerializer, StickerQueryScoreSerializer


class StickersSearchView(APIView):
    """
    """
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        """
        """
        query = request.query_params.get('query')
        query_mod, _ = StickerQuery.objects.get_or_create(query=request.query_params.get('query'))
        query_mod.usage = F('usage') + 1
        query_mod.save()
        images = SearchService().get_images_for_query(query)
        return Response({"stickers": images})


class StickersFeedbackView(APIView):
    """
    """
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        """
        """
        feedbacks = request.data['feedback']
        for fb in feedbacks:
            query_mod = StickerQuery.objects.get(query=fb['query'])
            for item in fb['positive']:
                sticker_mod = Sticker.objects.get(filename=item)
                feedback_mod, _ = StickerQueryScore.objects\
                    .get_or_create(sticker=sticker_mod, query=query_mod)
                feedback_mod.positives = F('positives') + 1
                feedback_mod.save()
            for item in fb['negative']:
                sticker_mod = Sticker.objects.get(filename=item)
                feedback_mod, _ = StickerQueryScore.objects \
                    .get_or_create(sticker=sticker_mod, query=query_mod)
                feedback_mod.negatives = F('negatives') + 1
                feedback_mod.save()
        return Response()


class StickersStatisticsView(APIView):
    """
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        """
        """
        query = request.query_params.get('query')

        query_mod = StickerQuery.objects.get(query=query)
        query_ser = StickerQuerySerializer(query_mod)

        score_qs = StickerQueryScore.objects.filter(query=query_mod)
        score_ser = StickerQueryScoreSerializer(score_qs, many=True)

        return Response({"query": query_ser.data, "feedback scores": score_ser.data})
