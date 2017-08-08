import unittest

from core import quotes


class TestQuotes(unittest.TestCase):

    def test_quote_get(self):
        data = quotes.quote_get()
        self.assertTrue(type(data), tuple)

    def test_quote_get_with_id(self):
        data = quotes.quote_get(1)
        expecting = (1, 'Нам деньги-то не очень нужны (C) Натаха')
        self.assertEqual(data, expecting)

    def test_quote_get_is_not_none(self):
        data = quotes.quote_get()
        self.assertIsNotNone(data)


if __name__ == "__main__":
    unittest.main()
