"""
Tests for the Team League Repository.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import TeamLeague
from repositories import TeamLeagueRepository


def create_maker() -> sessionmaker:
    """
    Creates the Session Maker.
    :return: Session Maker
    """

    engine = create_engine('sqlite://')
    TeamLeague.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_team_league_exists():
    """
    Tests the Team League exists.
    """
    maker = create_maker()
    team_league = TeamLeague(id=1, team_id=1, league_id=2, year_value=2021)
    repo = TeamLeagueRepository(maker)
    repo.save(team_league)

    result = repo.team_league_exists(team_league)
    assert_that(result).is_true()


def test_team_league_not_exist():
    """
    Tests the Team League does not exist.
    """

    maker = create_maker()
    team_league = TeamLeague(id=1, team_id=1, league_id=2, year_value=2021)
    team_league2 = TeamLeague(id=2, team_id=1, league_id=2, year_value=2022)
    repo = TeamLeagueRepository(maker)
    repo.save(team_league)

    result = repo.team_league_exists(team_league2)
    assert_that(result).is_false()


def test_get_team_leagues_team():
    """
    Test returning the Team Leagues by Team.
    """
    maker = create_maker()
    team_league = TeamLeague(id=1, team_id=1, league_id=2, year_value=2021)
    team_league2 = TeamLeague(id=2, team_id=2, league_id=2, year_value=2022)
    repo = TeamLeagueRepository(maker)
    repo.save(team_league)
    repo.save(team_league2)

    result = repo.get_team_leagues(team_id=1)
    assert_that(result).contains_only(team_league)


def test_get_team_league_league():
    """
    Tests returning the Team Leagues by Leage.
    """
    maker = create_maker()
    team_league = TeamLeague(id=1, team_id=1, league_id=2, year_value=2021)
    team_league2 = TeamLeague(id=2, team_id=1, league_id=2, year_value=2022)
    repo = TeamLeagueRepository(maker)
    repo.save(team_league)
    repo.save(team_league2)

    result = repo.get_team_leagues(league_id=2)
    assert_that(result).contains_only(team_league, team_league2)


def test_get_team_leagues():
    """
    Tests returning all Team Leagues.
    """
    maker = create_maker()
    team_league = TeamLeague(id=1, team_id=1, league_id=2, year_value=2021)
    team_league2 = TeamLeague(id=2, team_id=1, league_id=2, year_value=2022)
    repo = TeamLeagueRepository(maker)
    repo.save(team_league)
    repo.save(team_league2)

    result = repo.get_team_leagues()
    assert_that(result).contains_only(team_league, team_league2)


def test_get_team_league():
    """
    Tests returning the Team League by ID.
    """
    maker = create_maker()
    team_league = TeamLeague(id=1, team_id=1, league_id=2, year_value=2021)
    team_league2 = TeamLeague(id=2, team_id=1, league_id=2, year_value=2022)
    repo = TeamLeagueRepository(maker)
    repo.save(team_league)
    repo.save(team_league2)

    result = repo.get_team_league(1)
    assert_that(result).is_equal_to(team_league)


def test_get_team_league_not_exist():
    """
    Tests returning the Team League that does not exist.
    """
    maker = create_maker()
    team_league = TeamLeague(id=1, team_id=1, league_id=2, year_value=2021)
    team_league2 = TeamLeague(id=2, team_id=1, league_id=2, year_value=2022)
    repo = TeamLeagueRepository(maker)
    repo.save(team_league)
    repo.save(team_league2)

    result = repo.get_team_league(3)
    assert_that(result).is_none()
