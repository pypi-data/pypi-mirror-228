"""
Tests for the Schedule Repository.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Schedule
from repositories import ScheduleRepository


def create_maker() -> sessionmaker:
    engine = create_engine('sqlite://')
    Schedule.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_schedule_exists():
    """
    Tests if a schedule exits.
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)

    result = repo.schedule_exists(schedule)
    assert_that(result).is_true()


def test_schedule_does_not_exist():
    """
    Tests if a schedule does not exit.
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    schedule2 = Schedule(id=2, team_id=2, opponent_id=1, year_value=2020, week_number=3,
                         game_id=665567,
                         url='www.google.com', type_id=1, is_home=False)

    repo = ScheduleRepository(maker)
    repo.save(schedule)

    result = repo.schedule_exists(schedule2)
    assert_that(result).is_false()


def test_get_schedule():
    """
    Tests retrieving a Schedule.
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)

    repo = ScheduleRepository(maker)
    repo.save(schedule)

    result = repo.get_schedule(1)
    assert_that(result).is_equal_to(schedule)


def test_get_schedule_not_exists():
    """
    Tests retrieving a schedule that does not exist.
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)

    result = repo.get_schedule(2)
    assert_that(result).is_none()


def test_get_schedules():
    """
    Tests retrieving all schedules.
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)

    result = repo.get_schedules()
    assert_that(result).is_not_empty().contains(schedule)


def test_get_schedules_by_team():
    """
    Tests retrieving a Teams schedules.
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)
    result = repo.get_schedules(team_id=1)
    assert_that(result).is_not_empty().contains(schedule)


def test_get_schedules_by_year_and_week():
    """
    Tests retrieving Schedules by Week and Year
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    schedule2 = Schedule(id=2, team_id=2, opponent_id=1, year_value=2020, week_number=4,
                         game_id=665567,
                         url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)
    repo.save(schedule2)

    result = repo.get_schedules(year=2020, week=3)
    assert_that(result).is_not_empty().contains_only(schedule)


def test_get_schedules_by_team_year_week():
    """
    Tests retrieving a Teams Schedule by week and year.
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    schedule2 = Schedule(id=2, team_id=2, opponent_id=1, year_value=2020, week_number=4,
                         game_id=665567,
                         url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)
    repo.save(schedule2)

    result = repo.get_schedules(team_id=1, year=2020, week=3)
    assert_that(result).is_not_empty().contains_only(schedule)


def test_get_schedules_by_team_year():
    """
    Tests retrieving Schedule by Team and Year
    """

    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    schedule2 = Schedule(id=2, team_id=2, opponent_id=1, year_value=2020, week_number=4,
                         game_id=665567,
                         url='www.google.com', type_id=1, is_home=True)
    schedule3 = Schedule(id=3, team_id=2, opponent_id=1, year_value=2021, week_number=4,
                         game_id=665568,
                         url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)
    repo.save(schedule2)
    repo.save(schedule3)

    result = repo.get_schedules(team_id=2, year=2020)
    assert_that(result).contains_only(schedule2)


def test_get_schedules_by_year():
    """
    Tests retrieving the Schedules by only the year.
    :return:
    """
    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    schedule2 = Schedule(id=2, team_id=2, opponent_id=1, year_value=2020, week_number=4,
                         game_id=665567,
                         url='www.google.com', type_id=1, is_home=True)
    schedule3 = Schedule(id=3, team_id=2, opponent_id=1, year_value=2021, week_number=4,
                         game_id=665568,
                         url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)
    repo.save(schedule2)
    repo.save(schedule3)

    result = repo.get_schedules(year=2020)

    assert_that(result).contains_only(schedule, schedule2)


def test_get_schedule_by_week():
    """
    Tests retrieving schedule by only week.
    """

    maker = create_maker()
    schedule = Schedule(id=1, team_id=1, opponent_id=2, year_value=2020, week_number=3,
                        game_id=665566,
                        url='www.google.com', type_id=1, is_home=True)
    schedule2 = Schedule(id=2, team_id=2, opponent_id=1, year_value=2020, week_number=4,
                         game_id=665567,
                         url='www.google.com', type_id=1, is_home=True)
    schedule3 = Schedule(id=3, team_id=2, opponent_id=1, year_value=2021, week_number=4,
                         game_id=665568,
                         url='www.google.com', type_id=1, is_home=True)
    repo = ScheduleRepository(maker)
    repo.save(schedule)
    repo.save(schedule2)
    repo.save(schedule3)

    result = repo.get_schedules(week=4)
    assert_that(result).contains_only(schedule2, schedule3)
