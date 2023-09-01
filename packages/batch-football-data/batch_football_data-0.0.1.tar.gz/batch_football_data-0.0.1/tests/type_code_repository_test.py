"""
Tests for the Type Code Repository.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import TypeCode
from repositories import TypeCodeRepository


def create_maker() -> sessionmaker:
    """
    Creates a Session Maker.
    """
    engine = create_engine('sqlite://')
    TypeCode.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_type_code_exists():
    """
    Tests the Type Code Exists.
    """
    maker = create_maker()
    code = TypeCode(id=1, code='TST', description='Test Code')
    repo = TypeCodeRepository(maker)
    repo.save(code)

    result = repo.type_code_exists(code)
    assert_that(result).is_true()


def test_type_code_not_exists():
    """
    Tests the Type Code not exists.
    """
    maker = create_maker()
    code = TypeCode(id=1, code='TST', description='Test Code')
    code2 = TypeCode(id=2, code='TST2', description='Test Code 2')
    repo = TypeCodeRepository(maker)
    repo.save(code)

    result = repo.type_code_exists(code2)
    assert_that(result).is_false()


def test_get_type_code():
    """
    Tests retrieving Type Code by ID
    """
    maker = create_maker()
    code = TypeCode(id=1, code='TST', description='Test Code')
    code2 = TypeCode(id=2, code='TST2', description='Test Code 2')
    repo = TypeCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_type_code(id=1)
    assert_that(result).is_equal_to(code)


def test_get_type_code_by_code():
    """
    Tests retrieving Type code by Code.
    """
    maker = create_maker()
    code = TypeCode(id=1, code='TST', description='Test Code')
    code2 = TypeCode(id=2, code='TST2', description='Test Code 2')
    repo = TypeCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_type_code(code='TST')
    assert_that(result).is_equal_to(code)


def test_get_type_code_not_exist():
    """
    Tests retrieving a Type Code that does not exist.
    """
    maker = create_maker()
    code = TypeCode(id=1, code='TST', description='Test Code')
    code2 = TypeCode(id=2, code='TST2', description='Test Code 2')
    repo = TypeCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_type_code(id=3)
    assert_that(result).is_none()


def test_get_type_code_no_args():
    """
    Tests retrieving a Type Code without Args.
    """

    maker = create_maker()
    code = TypeCode(id=1, code='TST', description='Test Code')
    code2 = TypeCode(id=2, code='TST2', description='Test Code 2')
    repo = TypeCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_type_code()
    assert_that(result).is_none()


def test_get_type_codes():
    """
    Tests retrieving all type codes.
    """
    maker = create_maker()
    code = TypeCode(id=1, code='TST', description='Test Code')
    code2 = TypeCode(id=2, code='TST2', description='Test Code 2')
    repo = TypeCodeRepository(maker)
    repo.save(code)
    repo.save(code2)

    result = repo.get_type_codes()
    assert_that(result).is_not_empty().contains_only(code, code2)
