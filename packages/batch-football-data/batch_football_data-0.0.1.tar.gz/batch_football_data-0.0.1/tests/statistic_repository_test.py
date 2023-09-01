"""
Tests for the Statistics Repository.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Statistic
from repositories import StatisticRepository


def create_maker() -> sessionmaker:
    """
    Creates the Sqlite Database Engine
    :return: sessionmaker
    """
    engine = create_engine('sqlite://')
    Statistic.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_player_statistic_exists():
    """
    Tests if a Statistic exists.
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, player_id=1, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)

    result = repo.statistic_exists(stat)
    assert_that(result).is_true()


def test_team_statistic_exists():
    """
    Tests if a Team Statistic Exists.
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, team_id=1, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)

    result = repo.statistic_exists(stat)
    assert_that(result).is_true()


def test_statistic_does_not_exist():
    """
    Tests that a statistic does not exist
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, team_id=1, schedule_id=1, value=20, category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)

    result = repo.statistic_exists(stat2)
    assert_that(result).is_false()


def test_get_statistic():
    """
    Tests retrieving a Statistic by the ID Value.
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, team_id=1, schedule_id=1, value=20, category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistic(1)
    assert_that(result).is_not_none().is_equal_to(stat)


def test_get_statistic_does_not_exist():
    """
    Tests retrieving Statistic that does not exist.
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, team_id=1, schedule_id=1, value=20, category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistic(3)
    assert_that(result).is_none()


def test_get_statistics_by_team_id():
    """
    Tests retrieving the statistics by Team ID
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, player_id=1, schedule_id=1, value=20, category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistics(team_id=2)
    assert_that(result).contains_only(stat2)


def test_get_statistics_by_player_id():
    """
    Tests retrieving the statistics by Player ID
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, player_id=1, schedule_id=1, value=20, category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistics(player_id=1)
    assert_that(result).contains_only(stat)


def test_get_statistics_by_schedule_id():
    """
    Tests retrieving the statistics by Schedule ID
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, player_id=1, schedule_id=1, value=20, category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistics(schedule_id=1)
    assert_that(result).contains_only(stat, stat2)


def test_get_statistics_by_player_team_and_schedule():
    """
    Tests retrieving the statistics by Player, Team, and Schedule.
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, team_id=1, player_id=1, schedule_id=1, value=20,
                     category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistics(player_id=1, team_id=1, schedule_id=1)
    assert_that(result).contains_only(stat)


def test_get_statistics_by_player_team():
    """
    Tests retrieving statistics by player and team
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, player_id=1, team_id=1, schedule_id=1, value=20,
                     category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistics(player_id=1, team_id=1)
    assert_that(result).contains_only(stat)


def test_get_statistics_by_player_schedule():
    """
    Tests retrieving statistics by player and schedule.
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, player_id=1, schedule_id=1, value=20, category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistics(player_id=1, schedule_id=1)
    assert_that(result).contains_only(stat)


def test_get_statistics_by_team_schedule():
    """
    Tests retrieving statistics by team and schedule.
    """
    maker = create_maker()
    stat = Statistic(id=1, statistic_code_id=1, team_id=1, schedule_id=1, value=20, category_id=1)
    stat2 = Statistic(id=2, statistic_code_id=1, team_id=2, schedule_id=1, value=20, category_id=1)
    repo = StatisticRepository(maker)
    repo.save(stat)
    repo.save(stat2)

    result = repo.get_statistics(team_id=2, schdule_id=1)
    assert_that(result).contains_only(stat2)
