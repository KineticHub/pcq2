import json
import struct
from io import BytesIO

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock, call


class VectorsApiTests(APITestCase):

    @patch('vectors.api.ImageSearch')
    @patch('vectors.api.ImageVector.objects.values_list')
    @patch('vectors.api.torch')
    def test_SearchImageVectors(self, torch_mock, image_vector_values_list_mock, image_search_mock):
        """
        Test to make sure we are making the expected calls to various functions, and are returning the
        data as expected.
        """

        query = 'cat'
        fake_files = ["a", "b", "c", "d", 'e']
        fake_vectors = [struct.pack('f', 0.1 * i) for i in range(512)]
        fake_scores = ['0', '1', '2', '3', '4']

        def values_list_returns(*args, **kwargs):
            if args == ('filename',):
                return fake_files
            elif args == ('tensor_blob',):
                return fake_vectors

        url = reverse('search_image_vectors') + '?query=' + query

        image_vector_values_list_mock.side_effect = values_list_returns
        search_instance = MagicMock()
        search_instance.get_scores.return_value = fake_scores
        image_search_mock.return_value = search_instance

        response = self.client.get(url, format='json')

        self.assertEqual(json.loads(response.content)['filenames'], fake_files)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(torch_mock.cat.called)
        self.assertTrue(torch_mock.load.called)
        self.assertTrue(torch_mock.Size.called)

        self.assertTrue(image_search_mock.called)

        self.assertEqual(image_vector_values_list_mock.call_count, 2)
        image_vector_values_list_mock.assert_has_calls([
            call('tensor_blob', flat=True),
            call('filename', flat=True)
        ])

        search_instance.get_scores.assert_called_once_with(query)

