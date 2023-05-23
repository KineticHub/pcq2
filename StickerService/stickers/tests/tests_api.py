import json
import struct
from io import BytesIO

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock, call, PropertyMock

from stickers.models import StickerQuery, StickerQueryScore
from stickers.tests.factories import StickerFactory, StickerQueryFactory, UserFactory, TokenFactory


class StickersApiTests(APITestCase):

    @patch('stickers.api.SearchService')
    def test_StickersSearch_search(self, search_service_mock):
        """
        Ensure that we use the query passed in from the user, increase the query usage counter,
        and return the filenames provided by the ml-based search service.
        """

        sticker_query_obj = StickerQueryFactory()

        filenames = ['a', 'b', 'c']
        url = reverse('stickers_search') + '?query=' + sticker_query_obj.query

        search_service_mock.get_images_for_query.return_value = filenames
        search_service_mock.return_value = search_service_mock

        response = self.client.get(url, format='json')
        self.assertEqual(json.loads(response.content)['stickers'], filenames)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sticker_query_obj.refresh_from_db()
        self.assertEqual(sticker_query_obj.usage, 1)

        search_service_mock.get_images_for_query.assert_called_once_with(sticker_query_obj.query)

    def test_StickersFeedback_single_query_and_stickers(self):
        """
        Check that the feedback is saved for the query with positive and negative sticker feedbacks.
        """

        sticker_objs = StickerFactory.create_batch(2)
        sticker_query_obj = StickerQueryFactory()

        feedback = {
            "feedback": [
                {
                    "query": sticker_query_obj.query,
                    "positive": [sticker_objs[0].filename],
                    "negative": [sticker_objs[1].filename]
                }
            ]
        }
        url = reverse('stickers_feedback')

        response = self.client.post(url, data=feedback, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(StickerQueryScore.objects.count() == 2)

        positive_obj = StickerQueryScore.objects.get(query=sticker_query_obj, sticker=sticker_objs[0])
        self.assertEqual(positive_obj.positives, 1)
        negative_obj = StickerQueryScore.objects.get(query=sticker_query_obj, sticker=sticker_objs[1])
        self.assertEqual(negative_obj.negatives, 1)

    def test_StickersFeedback_multiple_query_and_stickers(self):
        """
        Check that the feedback is saved for multiple queries, and each query feedback is correctly saved with
        multiple positive and/or negative sticker feedbacks.
        """

        sticker_objs = StickerFactory.create_batch(4)
        sticker_query_objs = StickerQueryFactory.create_batch(2)

        feedback = {
            "feedback": [
                {
                    "query": sticker_query_objs[0].query,
                    "positive": [sticker_objs[0].filename, sticker_objs[1].filename],
                    "negative": []
                },
                {
                    "query": sticker_query_objs[1].query,
                    "positive": [],
                    "negative": [sticker_objs[2].filename, sticker_objs[3].filename]
                }
            ]
        }

        url = reverse('stickers_feedback')
        response = self.client.post(url, data=feedback, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(StickerQueryScore.objects.count() == 4)
        self.assertEqual(StickerQueryScore.objects.filter(query=sticker_query_objs[0], positives=1).count(), 2)
        self.assertEqual(StickerQueryScore.objects.filter(query=sticker_query_objs[1], negatives=1).count(), 2)

    def test_StickersFeedback_bad_query(self):
        """
        Return a query not found message when attempting to provide feedback for a query that was never used.
        """

        sticker_objs = StickerFactory.create_batch(2)

        feedback = {
            "feedback": [
                {
                    "query": "bad_query",
                    "positive": [sticker_objs[0].filename],
                    "negative": [sticker_objs[1].filename]
                }
            ]
        }
        url = reverse('stickers_feedback')

        response = self.client.post(url, data=feedback, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("not found" in json.loads(response.content)['message'].lower())

        self.assertTrue(StickerQueryScore.objects.count() == 0)

    def test_StickersFeedback_bad_image(self):
        """
        Check that we return a list of failed images, but save the correct ones.
        """

        sticker_objs = StickerFactory.create_batch(2)
        sticker_query_obj = StickerQueryFactory()
        bad_image = "bad_image_filename"

        feedback = {
            "feedback": [
                {
                    "query": sticker_query_obj.query,
                    "positive": [sticker_objs[0].filename, bad_image],
                    "negative": [sticker_objs[1].filename]
                }
            ]
        }
        url = reverse('stickers_feedback')

        response = self.client.post(url, data=feedback, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['failed'], [bad_image])

        self.assertTrue(StickerQueryScore.objects.count() == 2)

    def test_StickersStatistics_unauthenticated(self):
        """
        Anonymous users should not be able to access statistics.
        """

        sticker_query_obj = StickerQueryFactory()

        url = reverse('stickers_query_stats') + '?query=' + sticker_query_obj.query

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_StickersStatistics_unauthorized(self):
        """
        Users who are logged in but are not admins should not have access.
        """

        sticker_query_obj = StickerQueryFactory()

        url = reverse('stickers_query_stats') + '?query=' + sticker_query_obj.query

        self.client.force_login(UserFactory(is_staff=False))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_StickersStatistics_authorized_missing_token(self):
        """
        Users who are logged in and are admins but have not included the header token are denied.
        """

        sticker_query_obj = StickerQueryFactory()

        url = reverse('stickers_query_stats') + '?query=' + sticker_query_obj.query

        self.client.force_login(UserFactory(is_staff=True))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_StickersStatistics_authorized(self):
        """
        Users who are admins with a token should be authorized.
        """

        sticker_query_obj = StickerQueryFactory()

        url = reverse('stickers_query_stats') + '?query=' + sticker_query_obj.query

        user = UserFactory(is_staff=True)
        token = TokenFactory(user=user)

        headers = {"Authorization": f"Token {token.key}"}
        response = self.client.get(url, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_StickersStatistics_bad_query(self):
        """
        If trying to get statistics for a query that was not used, return not found.
        """

        bad_query = "bad_query"

        url = reverse('stickers_query_stats') + '?query=' + bad_query

        user = UserFactory(is_staff=True)
        token = TokenFactory(user=user)

        headers = {"Authorization": f"Token {token.key}"}
        response = self.client.get(url, format='json', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("not found" in json.loads(response.content)['message'].lower())
