"""
Tests for the Base Repository.
"""

from assertpy import assert_that
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from models import Player, TeamStaff, TeamLeague, Team, TypeCode, Position, \
    StatisticCode, \
    Statistic, \
    StatisticCategory, Schedule, League
from repositories import BaseRepository


def create_maker() -> sessionmaker:
    """
    Sets up the SQLite Database.
    :return: Session Maker.
    """
    engine = create_engine('sqlite://')
    Player.metadata.create_all(bind=engine)
    TeamStaff.metadata.create_all(bind=engine)
    TeamLeague.metadata.create_all(bind=engine)
    Team.metadata.create_all(bind=engine)
    TypeCode.metadata.create_all(bind=engine)
    Position.metadata.create_all(bind=engine)
    StatisticCode.metadata.create_all(bind=engine)
    Statistic.metadata.create_all(bind=engine)
    StatisticCategory.metadata.create_all(bind=engine)
    Schedule.metadata.create_all(bind=engine)
    League.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_save():
    """
    Tests Saving a Record
    """
    maker = create_maker()
    repo = BaseRepository(maker)

    player = Player(id=1, url='www.google.com', name='Jim Smith')
    repo.save(player)

    session = maker()
    stmt = select(Player).where(Player.id == 1)
    result = session.execute(stmt).first()
    assert_that(result).is_not_empty()
    assert_that(result).contains(player)


def test_save_all():
    """
    Tests Saving a collection of items.
    :return:
    """

    maker = create_maker()
    repo = BaseRepository(maker)

    player = Player(id=1, url='www.google.com', name='Jim Smith')
    code = TypeCode(id=1, code='tst', description='Test')
    repo.save_all([player, code])

    session = maker()

    player_result = session.execute(select(Player).where(Player.name == 'Jim Smith')).first()
    assert_that(player_result).is_not_empty().contains(player)

    type_result = session.execute(select(TypeCode).where(TypeCode.code == 'tst')).first()
    assert_that(type_result).is_not_empty().contains(code)


def test_save_exceptions():
    """
    Tests an exception is thrown.
    """

    engine = create_engine('sqlite://')
    maker = sessionmaker(bind=engine, expire_on_commit=False)
    repo = BaseRepository(maker)
    player = Player(id=1, url='www.google.com', name='Jim Smith')

    assert_that(repo.save).raises(SQLAlchemyError).when_called_with(player)


def test_save_all_exceptions():
    """
    Tests exception is thrown on Save All.
    """
    engine = create_engine('sqlite://')
    maker = sessionmaker(bind=engine, expire_on_commit=False)
    repo = BaseRepository(maker)
    player = Player(id=1, url='www.google.com', name='Jim Smith')

    assert_that(repo.save_all).raises(SQLAlchemyError).when_called_with([player])
