"""
League Repository Tests.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import League
from repositories import LeagueRepository


def create_maker() -> sessionmaker:
    """
    Creates the Session Maker.
    :return: sessionmaker
    """
    engine = create_engine('sqlite://')
    League.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_league_exists():
    """
    Tests if a League exists.
    """
    maker = create_maker()
    league = League(id=1, code='NFC', description='National Football Conference')
    repo = LeagueRepository(maker)
    repo.save(league)

    result = repo.league_exits(league)
    assert_that(result).is_true()


def test_league_does_not_exist():
    """
    Tests if a league does not exist.
    """
    maker = create_maker()
    league = League(id=1, code='NFC', description='National Football Conference')
    league2 = League(id=2, code='AFC', description='American Football Conference')
    repo = LeagueRepository(maker)
    repo.save(league)

    result = repo.league_exits(league2)

    assert_that(result).is_false()


def test_get_league():
    """
    Tests retrieving a League by id
    """
    maker = create_maker()
    league = League(id=1, code='NFC', description='National Football Conference')
    league2 = League(id=2, code='AFC', description='American Football Conference')
    repo = LeagueRepository(maker)
    repo.save(league)
    repo.save(league2)

    result = repo.get_league(id=1)

    assert_that(result).is_equal_to(league)


def test_get_league_by_code():
    """
    Tests retrieving a League by Code
    """

    maker = create_maker()
    league = League(id=1, code='NFC', description='National Football Conference')
    league2 = League(id=2, code='AFC', description='American Football Conference')
    repo = LeagueRepository(maker)
    repo.save(league)
    repo.save(league2)

    result = repo.get_league(code='AFC')
    assert_that(result).is_equal_to(league2)


def test_get_league_not_exists():
    """
    Tests retrieving a League that does not exist.
    """
    maker = create_maker()
    league = League(id=1, code='NFC', description='National Football Conference')
    league2 = League(id=2, code='AFC', description='American Football Conference')
    repo = LeagueRepository(maker)
    repo.save(league)
    repo.save(league2)

    result = repo.get_league(code='JJJ')
    assert_that(result).is_none()


def test_get_league_no_args():
    """
    Tests retrieving a league without Args.
    """
    maker = create_maker()
    league = League(id=1, code='NFC', description='National Football Conference')
    league2 = League(id=2, code='AFC', description='American Football Conference')
    repo = LeagueRepository(maker)
    repo.save(league)
    repo.save(league2)

    result = repo.get_league()
    assert_that(result).is_none()


def test_get_leagues():
    """
    Tests retrieving all Leagues
    """
    maker = create_maker()
    league = League(id=1, code='NFC', description='National Football Conference')
    league2 = League(id=2, code='AFC', description='American Football Conference')
    repo = LeagueRepository(maker)
    repo.save(league)
    repo.save(league2)

    result = repo.get_leagues()
    assert_that(result).contains_only(league, league2)
