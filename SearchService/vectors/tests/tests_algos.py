import json
import struct
from io import BytesIO
from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock, call


class ImageSearchTests(TestCase):

    @patch('vectors.api.ImageSearch')
    @patch('vectors.api.clip')
    def test_encode_text(self, torch_mock, ImageSearch_mock):
        """
        Ensure we can create a new account object.
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

        ImageVector_values_list_mock.side_effect = values_list_returns
        search_instance = MagicMock()
        search_instance.get_scores.return_value = fake_scores
        ImageSearch_mock.return_value = search_instance

        response = self.client.get(url, format='json')

        self.assertEqual(json.loads(response.content)['filenames'], fake_files)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(torch_mock.cat.called)
        self.assertTrue(torch_mock.load.called)
        self.assertTrue(torch_mock.Size.called)

        self.assertTrue(ImageSearch_mock.called)

        self.assertEqual(ImageVector_values_list_mock.call_count, 2)
        ImageVector_values_list_mock.assert_has_calls([
            call('tensor_blob', flat=True),
            call('filename', flat=True)
        ])

        search_instance.get_scores.assert_called_once_with(query)

