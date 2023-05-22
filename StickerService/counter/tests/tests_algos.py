from unittest import TestCase

from counter.algos.digit_counter import count_numbers_with_digit


class DigitCounterTests(TestCase):

    def test_count_numbers_with_digit_only(self):
        self.assertEqual(1, count_numbers_with_digit(7, 7))

    def test_count_numbers_with_digit_no_digit_in_number(self):
        self.assertEqual(0, count_numbers_with_digit(7, 5))
        self.assertEqual(1, count_numbers_with_digit(7, 8))
        self.assertEqual(2, count_numbers_with_digit(7, 20))
        self.assertEqual(6, count_numbers_with_digit(7, 58))
        self.assertEqual(19, count_numbers_with_digit(7, 100))
        self.assertEqual(271, count_numbers_with_digit(7, 1000))
        self.assertEqual(504, count_numbers_with_digit(7, 1800))

    def test_count_numbers_with_digit_ones_column(self):
        self.assertEqual(3, count_numbers_with_digit(7, 27))
        self.assertEqual(18, count_numbers_with_digit(7, 87))
        self.assertEqual(63, count_numbers_with_digit(7, 357))
        self.assertEqual(76, count_numbers_with_digit(7, 397))

    def test_count_numbers_with_digit_tens_column(self):
        self.assertEqual(8, count_numbers_with_digit(7, 70))
        self.assertEqual(16, count_numbers_with_digit(7, 78))
        self.assertEqual(88, count_numbers_with_digit(7, 474))
        self.assertEqual(245, count_numbers_with_digit(7, 874))

    def test_count_numbers_with_digit_tens_and_ones_columns(self):
        self.assertEqual(15, count_numbers_with_digit(7, 77))
        self.assertEqual(34, count_numbers_with_digit(7, 177))
        self.assertEqual(267, count_numbers_with_digit(7, 977))

    def test_count_numbers_with_digit_triple_columns(self):
        self.assertEqual(211, count_numbers_with_digit(7, 777))
        self.assertEqual(3108, count_numbers_with_digit(7, 8777))
