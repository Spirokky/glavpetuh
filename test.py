import unittest

from core.quotes import Quote


class TestQuotes(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestQuotes, self).__init__(*args, **kwargs)
        self.q = Quote()

    def test_quote_get(self):
        data = self.q.quote_get()
        self.assertEqual(type(data), tuple)

    def test_quote_get_with_id(self):
        data = self.q.quote_get(1)
        expecting = (1, 'Нам деньги-то не очень нужны (C) Натаха')
        self.assertEqual(data, expecting)


if __name__ == "__main__":
    unittest.main()