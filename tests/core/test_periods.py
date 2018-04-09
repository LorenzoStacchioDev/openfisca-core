# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from nose.tools import assert_equal, raises

from openfisca_core.periods import Period, Instant, YEAR, MONTH, period

first_jan = Instant((2014, 1, 1))
first_march = Instant((2014, 3, 1))


# Test Period -> String

def test_year():
    assert_equal(str(Period((YEAR, first_jan, 1))), '2014')


def test_12_months_is_a_year():
    assert_equal(str(Period((MONTH, first_jan, 12))), '2014')


def test_rolling_year():
    assert_equal(str(Period((MONTH, first_march, 12))), 'year:2014-03')
    assert_equal(str(Period((YEAR, first_march, 1))), 'year:2014-03')


def test_month():
    assert_equal(str(Period((MONTH, first_jan, 1))), '2014-01')


def test_several_months():
    assert_equal(str(Period((MONTH, first_jan, 3))), 'month:2014-01:3')
    assert_equal(str(Period((MONTH, first_march, 3))), 'month:2014-03:3')


def test_several_years():
    assert_equal(str(Period((YEAR, first_jan, 3))), 'year:2014:3')
    assert_equal(str(Period((YEAR, first_march, 3))), 'year:2014-03:3')

# Test String -> Period


def test_parsing_year():
    assert_equal(period('2014'), Period((YEAR, first_jan, 1)))


def test_parsing_month():
    assert_equal(period('2014-01'), Period((MONTH, first_jan, 1)))


def test_parsing_rolling_year():
    assert_equal(period('year:2014-03'), Period((YEAR, first_march, 1)))


def test_parsing_several_months():
    assert_equal(period('month:2014-03:3'), Period((MONTH, first_march, 3)))


def test_parsing_several_years():
    assert_equal(period('year:2014:2'), Period((YEAR, first_jan, 2)))


@raises(ValueError)
def test_wrong_syntax_several_years():
    period('2014:2')


@raises(ValueError)
def test_wrong_syntax_several_months():
    period('2014-2:2')


@raises(ValueError)
def test_daily_period():
    period('2014-2-3')


@raises(ValueError)
def test_daily_period_2():
    period('2014-2-3:2')


@raises(ValueError)
def test_ambiguous_period():
    period('month:2014')


@raises(TypeError)
def test_deprecated_signature():
    period(MONTH, 2014)


@raises(ValueError)
def test_wrong_argument():
    period({})


@raises(ValueError)
def test_wrong_argument_1():
    period([])


@raises(ValueError)
def test_none():
    period(None)


@raises(ValueError)
def test_empty_string():
    period('')
