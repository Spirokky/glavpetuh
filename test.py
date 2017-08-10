import unittest

from core.quotes import Quote


class TestQuotes(unittest.TestCase):

    def setUp(self):
        self.q = Quote('core/testing_database.db')

        with self.q.connect:
            self.q.cursor.execute("SELECT id FROM quotes WHERE id = (SELECT MAX(id)  FROM quotes);")
            self.last_row = self.q.cursor.fetchone()

    def tearDown(self):
        with self.q.connect:
            self.q.cursor.execute("DELETE FROM quotes WHERE id > (?);", self.last_row)

    def test_get(self):
        self.assertTupleEqual(self.q.get(3), (3, 'Все дороги ведут к людям.'))
        self.assertIsNotNone(self.q.get(1))

    def test_get_with_no_id(self):
        self.assertTrue(type(self.q.get()), tuple)

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

    def test_add(self):
        self.assertTrue(type(self.q.add('Жить дальше – безнравственно')), tuple)
        self.assertEqual(self.q.add('Бармен все равно что психотерапевт.')[1], ('Бармен все равно что психотерапевт.'))

    def test_add_no_args(self):
        with self.assertRaises(TypeError):
            self.q.add()
            self.q.add(False)

    def test_remove(self):
        pass


if __name__ == "__main__":
    unittest.main()
