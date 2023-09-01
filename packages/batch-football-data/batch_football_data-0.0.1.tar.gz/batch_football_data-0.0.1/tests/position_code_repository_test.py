"""
Repository Tests for Position Codes.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Position
from repositories import PositionCodeRepository


def create_maker() -> sessionmaker:
    """
    Creates the Session Maker.
    """
    engine = create_engine('sqlite://')
    Position.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_position_code_exists():
    """
    Tests if the Position Code Exits.
    """

    maker = create_maker()
    repo = PositionCodeRepository(maker)

    position = Position(id=1, code='QB', description='Quarterback')
    repo.save(position)

    result = repo.position_code_exists(position)

    assert_that(result).is_true()


def test_position_code_does_not_exist():
    """
    Tests if a position code does not exist.
    """
    maker = create_maker()
    repo = PositionCodeRepository(maker)

    position = Position(id=1, code='QB', description='Quarterback')
    position2 = Position(id=2, code='WR', description='Wide Receiver')
    repo.save(position)

    result = repo.position_code_exists(position2)
    assert_that(result).is_false()


def test_get_position_code_by_id():
    """
    Tests retrieving a Position Code by ID Value
    """
    maker = create_maker()
    repo = PositionCodeRepository(maker)

    position = Position(id=1, code='QB', description='Quarterback')
    repo.save(position)

    result = repo.get_position_code(id=1)
    assert_that(result).is_equal_to(position)


def test_get_position_code_by_code():
    """
    Tests retrieving a position code by the code.
    """
    maker = create_maker()
    repo = PositionCodeRepository(maker)

    position = Position(id=1, code='QB', description='Quarterback')
    repo.save(position)

    result = repo.get_position_code(code='QB')
    assert_that(result).is_equal_to(position)


def test_get_position_code_not_exist():
    """
    Tests retrieving a code that does not exist.
    """
    maker = create_maker()
    repo = PositionCodeRepository(maker)

    position = Position(id=1, code='QB', description='Quarterback')
    repo.save(position)

    result = repo.get_position_code(code='WR')
    assert_that(result).is_none()


def test_get_position_code_no_args():
    """
    Tests retrieving the Position code without args
    """
    maker = create_maker()
    repo = PositionCodeRepository(maker)

    position = Position(id=1, code='QB', description='Quarterback')
    repo.save(position)

    result = repo.get_position_code()
    assert_that(result).is_none()


def test_get_position_codes():
    """
    Tests retrieving all Position Codes.
    """
    maker = create_maker()
    repo = PositionCodeRepository(maker)

    position = Position(id=1, code='QB', description='Quarterback')
    repo.save(position)

    result = repo.get_position_codes()
    assert_that(result).contains(position)
