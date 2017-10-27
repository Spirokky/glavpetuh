import pytest

from random import randrange, random
from core import Exp


BIGNUM = 1000


@pytest.fixture(scope='module')
def setup(request):
    global exp, level, levels, max_lvl, table
    exp = Exp()
    level = exp.next_level
    levels = exp.levels
    max_lvl = max(levels.keys())
    table = exp.exp_table


def test_next_level(setup):
    assert level(1) == 'Опыта до lvl-up: 68'
    assert level(24) == 'Опыта до lvl-up: 751,775'
    assert level(80) == 'Опыта до lvl-up: 111,669,655,790'


def test_next_level_negative(setup):
    assert level(-50) == 'Минимальный уровень: 1'
    assert level(-50, 23) == 'Минимальный уровень: 1'


def test_next_level_zero(setup):
    assert level(0) == 'Минимальный уровень: 1'
    assert level(0, 92.24) == 'Минимальный уровень: 1'
    assert level(0, 200) == 'Минимальный уровень: 1'


def test_next_level_big_lvl(setup):
    for n in range(100):
        rand_num = randrange(101, BIGNUM)
        assert level(rand_num) == 'Максимальный уровень: %s' % max_lvl

    assert level(256) == 'Максимальный уровень: %s' % max_lvl


def test_next_level_string(setup):
    for n in range(100):
        rand_num = randrange(0, 100)
        assert level(str(rand_num)) == level(rand_num)


def test_next_level_percent(setup):
    for n in range(100):
        rand_num = randrange(0, 100)
        rand_percent = random() * 100
        assert level(str(rand_num), str(rand_percent)) == level(rand_num, rand_percent)

    assert level(24, 0) == 'Опыта до lvl-up: 751,775'
    assert level(1, 24.76) == 'Опыта до lvl-up: 51'
    assert level(56, 6.857463535465757) == 'Опыта до lvl-up: 71,090,320'


def test_next_level_big_percent(setup):
    for n in range(100):
        rand_num = randrange(101, BIGNUM)
        assert level(1, float(rand_num)) == 'Больной ублюдок'

    assert level(24, 101) == 'Больной ублюдок'
    assert level(56, 178) == 'Больной ублюдок'


@pytest.mark.xfail
def test_next_level_no_args(setup):
    assert level() == 'Какой левел, ущербный?'


def test_exp_table_negative_start(setup):
    for n in range(100):
        start = randrange(1, max_lvl+1) * -1
        end = randrange(1, max_lvl+1)
        assert table(start, end) == table(1, end)


def test_exp_table_negative_end(setup):
    for n in range(100):
        start = randrange(1, max_lvl+1)
        end = randrange(1, max_lvl+1) * -1
        assert table(start, end) == table(start, abs(end))


def test_exp_table_start_bigger_than_end(setup):
    assert table(80, 56) == 'НАЧАЛО должно быть меньше КОНЦА'
