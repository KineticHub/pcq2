from django.db.models import F

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from core.services.search import SearchService

from stickers.models import StickerQuery, Sticker, StickerQueryScore
from stickers.serializers import StickerQuerySerializer, StickerQueryScoreSerializer


class StickersSearchView(APIView):
    """
    Takes a customer query and returns the top ten images based on the searched  text.
    This is a proxy method for the SearchService, to decouple the ml-model from the primary
    customer-facing service. We track query usage for later analysis.
    """
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        query = request.query_params.get('query')
        if not query:
            return Response({"message": "Please provide a query."})
        if len(query) > 255:
            return Response({"message": "Query is too long."})
        query_mod, _ = StickerQuery.objects.get_or_create(query=request.query_params.get('query'))
        query_mod.usage = F('usage') + 1
        query_mod.save()
        images = SearchService().get_images_for_query(query)
        return Response({"stickers": images})


class StickersFeedbackView(APIView):
    """
    We want to receive feedback from the customer on whether they felt that the
    images provided matched the search that they gave. We allow for multiple feedbacks
    at one time for a more flexible interface.
    """
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        feedbacks = request.data['feedback']
        failed = []
        for fb in feedbacks:
            if not StickerQuery.objects.filter(query=fb['query']).exists():
                return Response({"message": "Query not found."})
            query_mod = StickerQuery.objects.get(query=fb['query'])
            for item in fb['positive']:
                if not Sticker.objects.filter(filename=item).exists():
                    failed.append(item)
                    continue
                sticker_mod = Sticker.objects.get(filename=item)
                feedback_mod, _ = StickerQueryScore.objects\
                    .get_or_create(sticker=sticker_mod, query=query_mod)
                feedback_mod.positives = F('positives') + 1
                feedback_mod.save()
            for item in fb['negative']:
                if not Sticker.objects.filter(filename=item).exists():
                    failed.append(item)
                    continue
                sticker_mod = Sticker.objects.get(filename=item)
                feedback_mod, _ = StickerQueryScore.objects \
                    .get_or_create(sticker=sticker_mod, query=query_mod)
                feedback_mod.negatives = F('negatives') + 1
                feedback_mod.save()
        return Response({"failed": failed})


class StickersStatisticsView(APIView):
    """
    For internal use only. Provide a mechanism for getting data about the customer feedback
    received in searches.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        query = request.query_params.get('query')

        if not StickerQuery.objects.filter(query=query).exists():
            return Response({"message": "Query not found."})

        query_mod = StickerQuery.objects.get(query=query)
        query_ser = StickerQuerySerializer(query_mod)

        score_qs = StickerQueryScore.objects.filter(query=query_mod)
        score_ser = StickerQueryScoreSerializer(score_qs, many=True)

        return Response({"query": query_ser.data, "feedback scores": score_ser.data})
