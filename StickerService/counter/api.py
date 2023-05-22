from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from counter.algos.digit_counter import count_numbers_with_digit


class DigitCounterView(APIView):
    """
    """
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        """
        Count the number of numbers that have the specified digit between 1 and n.
        """
        digit = request.query_params.get('digit', 7)
        n = request.query_params.get('n')
        return Response({"answer": count_numbers_with_digit(int(digit), int(n))})
