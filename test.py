import unittest

from core.quotes import Quote
from core.exp import Exp


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


class TestExp(unittest.TestCase):

    def setUp(self):
        self.exp = Exp()

    def test_next_level(self):
        self.assertEqual(self.exp.next_level(24, 5), 'Опыта до lvl-up: 714,186')
        self.assertEqual(self.exp.next_level(24), 'Опыта до lvl-up: 751,775')
        self.assertEqual(self.exp.next_level(1), 'Опыта до lvl-up: 68')
        self.assertEqual(self.exp.next_level(1, 24.76), 'Опыта до lvl-up: 51')
        self.assertEqual(self.exp.next_level(80), 'Опыта до lvl-up: 111,669,655,790')

    def test_next_level_with_long_percent(self):
        self.assertEqual(self.exp.next_level(56, 6.857463535465757), 'Опыта до lvl-up: 71,090,320')
        self.assertEqual(self.exp.next_level(1, 0.1384591209475), 'Опыта до lvl-up: 68')

    def test_next_level_with_zero_lvl(self):
        self.assertEqual(self.exp.next_level(0), "Минимальный уровень: 1")
        self.assertEqual(self.exp.next_level(0, 50), "Минимальный уровень: 1")

    def test_next_level_with_zero_percent(self):
        self.assertEqual(self.exp.next_level(76, 0), 'Опыта до lvl-up: 1,175,470,061')

    def test_next_level_with_big_lvl(self):
        max_lvl = 85
        self.assertEqual(self.exp.next_level(156), 'Максимальный уровень: %s' % max_lvl)

    def test_next_level_with_max_lvl(self):
        self.assertEqual(self.exp.next_level(85), 'Опыта до lvl-up: 273,117,371,391')
        self.assertEqual(self.exp.next_level(85, 50),'Опыта до lvl-up: 136,558,685,696')

    def test_next_level_with_over_hundred_percent(self):
        self.assertEqual(self.exp.next_level(45, 234), 'Больной ублюдок')

    def test_exp_table(self):
        pass


if __name__ == "__main__":
    unittest.main()
