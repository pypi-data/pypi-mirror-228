"""
Tests for the Statistic Category Code Repository.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import StatisticCategory
from repositories import StatisticCategoryRepository


def create_maker():
    """
    Creates the In Memory Database.
    """
    engine = create_engine('sqlite://')
    StatisticCategory.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_get_statistic_category_code():
    """
    Tests retrieving a Statistic Category Code.
    """
    maker = create_maker()
    code = StatisticCategory(id=1, code='O', description='Offense')
    repo = StatisticCategoryRepository(maker)
    repo.save(code)

    result = repo.get_statistic_category(code='O')
    assert_that(result).is_not_none().is_equal_to(code)


def test_get_statistic_category_code_by_id():
    """
    Tests retrieving the statistic category by primary key ID.
    """
    maker = create_maker()
    code = StatisticCategory(id=1, code='O', description='Offense')
    repo = StatisticCategoryRepository(maker)
    repo.save(code)

    result = repo.get_statistic_category(id=1)
    assert_that(result).is_not_none().is_equal_to(code)


def test_get_statistic_category_not_exist():
    """
    Tests retrieving a Statistic Category that does not exist.
    """
    maker = create_maker()
    code = StatisticCategory(id=1, code='O', description='Offense')
    repo = StatisticCategoryRepository(maker)
    repo.save(code)

    result = repo.get_statistic_category(code='D')
    assert_that(result).is_none()


def test_get_statistic_category_no_args():
    """
    Tests retrieving a statistic category without args.
    """
    maker = create_maker()
    code = StatisticCategory(id=1, code='O', description='Offense')
    repo = StatisticCategoryRepository(maker)
    repo.save(code)

    result = repo.get_statistic_category()
    assert_that(result).is_none()


def test_statistic_category_exists():
    """
    Tests a statistic category exists.
    """

    maker = create_maker()
    code = StatisticCategory(id=1, code='O', description='Offense')
    repo = StatisticCategoryRepository(maker)
    repo.save(code)

    result = repo.statistic_category_exists(code)
    assert_that(result).is_true()


def test_statistic_category_does_not_exist():
    """
    Tests that a statistic category does not exist.
    """
    maker = create_maker()
    code = StatisticCategory(id=1, code='O', description='Offense')
    code2 = StatisticCategory(id=2, code='D', description='Defense')
    repo = StatisticCategoryRepository(maker)
    repo.save(code)

    result = repo.statistic_category_exists(code2)
    assert_that(result).is_false()


def test_get_statistic_categories():
    """
    Tests retrieving all Statistic Category Codes.
    """
    maker = create_maker()
    code = StatisticCategory(id=1, code='O', description='Offense')
    code2 = StatisticCategory(id=2, code='D', description='Defense')
    repo = StatisticCategoryRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_statistic_categories()
    assert_that(result).is_not_empty().contains_only(code, code2)
