"""
Team Staff Repository Tests.
"""
from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import TeamStaff
from repositories import TeamStaffRepository


def create_maker() -> sessionmaker:
    """
    Creates the Session Maker.
    :return: Session Maker
    """

    engine = create_engine('sqlite://')
    TeamStaff.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_team_staff_exists():
    """
    Tests if a Team Staff Exists.
    """
    maker = create_maker()
    staff = TeamStaff(id=1, player_id=1, team_id=2, year_value=2020)
    repo = TeamStaffRepository(maker)
    repo.save(staff)

    result = repo.team_staff_exists(staff)
    assert_that(result).is_true()


def test_team_staff_does_not_exist():
    """
    Tests that a Team Staff does not exist.
    """
    maker = create_maker()
    staff = TeamStaff(id=1, player_id=1, team_id=2, year_value=2020)
    staff2 = TeamStaff(id=2, player_id=2, team_id=2, year_value=2020)
    repo = TeamStaffRepository(maker)
    repo.save(staff)

    result = repo.team_staff_exists(staff2)
    assert_that(result).is_false()


def test_get_team_staff_entry():
    """
    Tests retrieving a Team Staff from by ID
    """
    maker = create_maker()
    staff = TeamStaff(id=1, player_id=1, team_id=2, year_value=2020)
    staff2 = TeamStaff(id=2, player_id=2, team_id=2, year_value=2020)
    repo = TeamStaffRepository(maker)
    repo.save(staff)
    repo.save(staff2)

    result = repo.get_team_staff_entry(1)
    assert_that(result).is_equal_to(staff)


def test_get_team_staff_entries():
    """
    Tests retrieving all Team Staff Entries
    """
    maker = create_maker()
    staff = TeamStaff(id=1, player_id=1, team_id=2, year_value=2020)
    staff2 = TeamStaff(id=2, player_id=2, team_id=2, year_value=2020)
    repo = TeamStaffRepository(maker)
    repo.save(staff)
    repo.save(staff2)

    result = repo.get_team_staff_entries()
    assert_that(result).contains_only(staff, staff2)


def test_get_team_staff_team_id():
    """
    Tests retrieving the Team Staff entries by Team Id
    """
    maker = create_maker()
    staff = TeamStaff(id=1, player_id=1, team_id=2, year_value=2020)
    staff2 = TeamStaff(id=2, player_id=2, team_id=3, year_value=2020)
    repo = TeamStaffRepository(maker)
    repo.save(staff)
    repo.save(staff2)

    result = repo.get_team_staff_entries(team_id=3)
    assert_that(result).contains_only(staff2)


def test_get_team_staff_by_player_team():
    """
    Tests retrieving the Team Staff by Player and Team ID
    """
    maker = create_maker()
    staff = TeamStaff(id=1, player_id=1, team_id=2, year_value=2020)
    staff2 = TeamStaff(id=2, player_id=2, team_id=2, year_value=2020)
    repo = TeamStaffRepository(maker)
    repo.save(staff)
    repo.save(staff2)

    result = repo.get_team_staff_entries(player_id=1, team_id=2)
    assert_that(result).contains_only(staff)


def test_get_team_staff_by_player():
    """
    Tests retrieving the Team Staff by Player Id
    """
    maker = create_maker()
    staff = TeamStaff(id=1, player_id=1, team_id=2, year_value=2020)
    staff2 = TeamStaff(id=2, player_id=2, team_id=2, year_value=2020)
    repo = TeamStaffRepository(maker)
    repo.save(staff)
    repo.save(staff2)

    result = repo.get_team_staff_entries(player_id=1)
    assert_that(result).contains_only(staff)
