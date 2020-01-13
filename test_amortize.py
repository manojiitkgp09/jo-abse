import unittest
from datetime import datetime

from amortize import amortize


class TestAmortize(unittest.TestCase):

    def _run_test(self, start_date, end_date, num_months, expected_result):
        actual_result = amortize(self.amount, start_date, end_date)
        self.assertEqual(len(actual_result), num_months)
        self.assertEqual(sum(actual_result), self.amount)
        self.assertTrue(all(isinstance(val, int) for val in actual_result))
        self.assertEqual(actual_result, expected_result)

    def setUp(self):
        self.amount = 100

    def test_start_date_less_than_end_date_return_empty_list(self):
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2014, 1, 1)
        result = amortize(self.amount, start_date, end_date)
        self.assertEqual(result, list())

    def test_end_date_in_same_month_and_year_as_start_date(self):
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2015, 1, 1)
        expected_result = [100]
        self._run_test(start_date, end_date, 1, expected_result)

    def test_end_date_in_consecutive_month_and_same_year_as_start_date(self):
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2015, 2, 1)
        expected_result = [97, 3]
        self._run_test(start_date, end_date, 2, expected_result)

    def test_end_date_month_is_partial_month_and_start_date_month_is_full_month(self):
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2015, 2, 10)
        expected_result = [74, 26]
        self._run_test(start_date, end_date, 2, expected_result)

    def test_end_date_month_is_partial_month_and_start_date_month_is_partial_month(self):
        start_date = datetime(2015, 1, 10)
        end_date = datetime(2015, 2, 10)
        expected_result = [66, 34]
        self._run_test(start_date, end_date, 2, expected_result)

    def test_start_date_month_is_partial_month_and_end_date_month_is_full_month(self):
        start_date = datetime(2015, 1, 10)
        end_date = datetime(2015, 3, 31)
        expected_result = [25, 38, 37]
        self._run_test(start_date, end_date, 3, expected_result)

    def test_both_date_year_same_and_start_date_month_is_full_month_and_end_date_month_is_full_month(self):
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2015, 3, 31)
        expected_result = [34, 33, 33]
        self._run_test(start_date, end_date, 3, expected_result)

    def test_both_date_year_not_same_and_start_date_month_is_full_month_and_end_date_month_is_full_month(self):
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2016, 3, 31)
        expected_result = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6]
        self._run_test(start_date, end_date, 15, expected_result)


if __name__ == '__main__':
    unittest.main()
