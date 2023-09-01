"""
Statistic Code Repository Tests.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (StatisticCode)
from repositories import StatisticCodeRepository


def create_maker() -> sessionmaker:
    """
    Creates the session maker.
    :return: sessionmaker
    """

    engine = create_engine('sqlite://')
    StatisticCode.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_statistic_code_exists():
    """
    Tests Statistic Code Exists.
    """

    maker = create_maker()
    code = StatisticCode(id=1, code='TST', description='Test Code')
    code2 = StatisticCode(id=2, code='TST2', description='Test Code2')
    repo = StatisticCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.statistic_code_exists(code)
    assert_that(result).is_true()


def test_statistic_code_not_exists():
    """
    Tests Statistics Code Not Exists.
    """
    maker = create_maker()
    code = StatisticCode(id=1, code='TST', description='Test Code')
    code2 = StatisticCode(id=2, code='TST2', description='Test Code2')
    repo = StatisticCodeRepository(maker)
    repo.save(code)

    result = repo.statistic_code_exists(code2)
    assert_that(result).is_false()


def test_get_statistic_code():
    """
    Test retrieving the statistic code by the id.
    """
    maker = create_maker()
    code = StatisticCode(id=1, code='TST', description='Test Code')
    code2 = StatisticCode(id=2, code='TST2', description='Test Code2')
    repo = StatisticCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_statistic_code(id=1)
    assert_that(result).is_equal_to(code)


def test_get_statistic_code_not_exists():
    """
    Test retrieving statistic code that doesn't exist
    """

    maker = create_maker()
    code = StatisticCode(id=1, code='TST', description='Test Code')
    code2 = StatisticCode(id=2, code='TST2', description='Test Code2')
    repo = StatisticCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_statistic_code(id=3)
    assert_that(result).is_none()


def test_get_statistic_code_no_args():
    """
    Tests retrieving a statistic code without args.
    """

    maker = create_maker()
    code = StatisticCode(id=1, code='TST', description='Test Code')
    code2 = StatisticCode(id=2, code='TST2', description='Test Code2')
    repo = StatisticCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_statistic_code()
    assert_that(result).is_none()


def test_get_statistic_code_by_code():
    """
    Tests retrieving a statistic code by code.
    """
    maker = create_maker()
    code = StatisticCode(id=1, code='TST', description='Test Code')
    code2 = StatisticCode(id=2, code='TST2', description='Test Code2')
    repo = StatisticCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_statistic_code(code='TST2')
    assert_that(result).is_equal_to(code2)


def test_get_statistic_codes():
    """
    Tests retrieving the statistic codes.
    """
    maker = create_maker()
    code = StatisticCode(id=1, code='TST', description='Test Code')
    code2 = StatisticCode(id=2, code='TST2', description='Test Code2')
    repo = StatisticCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_statistic_codes()
    assert_that(result).contains_only(code, code2)
