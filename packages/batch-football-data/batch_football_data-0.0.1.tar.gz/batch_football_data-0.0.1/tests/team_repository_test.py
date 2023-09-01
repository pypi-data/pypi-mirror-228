"""
Tests for the Team Repository.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Team
from repositories import TeamRepository


def create_maker() -> sessionmaker:
    """
    Creates a Session Maker.
    :return: Session Maker
    """
    engine = create_engine('sqlite://')
    Team.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_get_team():
    """
    Tests retrieving the Team by ID Value
    :return: Team or None
    """
    maker = create_maker()
    team = Team(id=1, url='www.google.com', code='KC', name='Kansas City')
    repo = TeamRepository(maker)
    repo.save(team)

    result = repo.get_team(id=1)

    assert_that(result).is_equal_to(team)


def test_get_team_by_code():
    """
    Tests retrieving the Team by Code.
    :return: Team or None
    """

    maker = create_maker()
    team = Team(id=1, url='www.google.com', code='KC', name='Kansas City')
    repo = TeamRepository(maker)
    repo.save(team)

    result = repo.get_team(code='KC')

    assert_that(result).is_equal_to(team)


def test_get_team_by_url():
    """
    Tests retrieving a Team by URL
    :return: Team or None
    """

    maker = create_maker()
    team = Team(id=1, url='www.google.com', code='KC', name='Kansas City')
    repo = TeamRepository(maker)
    repo.save(team)

    result = repo.get_team(url='www.google.com')

    assert_that(result).is_equal_to(team)


def test_get_team_not_exists():
    """
    Tests retrieving a team that does not exist.
    """

    maker = create_maker()
    team = Team(id=1, url='www.google.com', code='KC', name='Kansas City Chiefs')
    team2 = Team(id=2, url='www.team.com', code='LAR', name='Los Angeles Rams')
    repo = TeamRepository(maker)
    repo.save(team)
    repo.save(team2)

    result = repo.get_team(id=3)
    assert_that(result).is_none()


def test_get_team_no_args():
    """
    Tests retrieving a Team without Args.
    """
    maker = create_maker()
    team = Team(id=1, url='www.google.com', code='KC', name='Kansas City Chiefs')
    team2 = Team(id=2, url='www.team.com', code='LAR', name='Los Angeles Rams')
    repo = TeamRepository(maker)
    repo.save(team)
    repo.save(team2)

    result = repo.get_team()
    assert_that(result).is_none()


def test_team_exists():
    """
    Tests a Team exists.
    :return: Bool
    """

    maker = create_maker()
    team = Team(id=1, url='www.google.com', code='KC', name='Kansas City')
    repo = TeamRepository(maker)
    repo.save(team)

    result = repo.team_exists(team)

    assert_that(result).is_true()


def test_team_not_exist():
    """
    Tests a Team does not exist.
    :return: Bool
    """
    maker = create_maker()
    team = Team(id=1, url='www.google.com', code='KC', name='Kansas City Chiefs')
    team2 = Team(id=2, url='www.team.com', code='LAR', name='Los Angeles Rams')
    repo = TeamRepository(maker)
    repo.save(team)

    result = repo.team_exists(team2)

    assert_that(result).is_false()


def test_get_teams():
    """
    Tests retrieving all Teams.
    :return: list of Teams
    """

    maker = create_maker()
    team = Team(id=1, url='www.google.com', code='KC', name='Kansas City Chiefs')
    team2 = Team(id=2, url='www.team.com', code='LAR', name='Los Angeles Rams')
    repo = TeamRepository(maker)
    repo.save(team)
    repo.save(team2)

    result = repo.get_teams()
    assert_that(result).is_not_empty().contains_only(team, team2)
