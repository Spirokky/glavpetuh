import unittest

from core.quotes import Quote


class TestQuotes(unittest.TestCase):

    def setUp(self):
        self.q = Quote('core/testing_database.db')

    def tearDown(self):
        self.q.connect.rollback()
        self.q.connect.close()

    def test_get(self):
        self.assertTupleEqual(self.q.get(3), (3, 'Все дороги ведут к людям.'))
        self.assertIsNotNone(self.q.get(1))

    def test_get_with_no_id(self):
        with self.assertRaises(ValueError):
            self.q.get(False)
            self.q.get()

    def test_get_with_str(self):
        self.assertTupleEqual(self.q.get("3"), (3, 'Все дороги ведут к людям.'))
        with self.assertRaises(ValueError):
            self.q.get("string")

    def test_getrandom(self):
        self.assertTrue(type(self.q.getrandom()), tuple)
        self.assertIsNotNone(self.q.getrandom())

    def test_getrandom_with_args(self):
        with self.assertRaises(TypeError):
            self.q.getrandom(123)


if __name__ == "__main__":
    unittest.main()
