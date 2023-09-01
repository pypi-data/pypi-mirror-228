"""
Tests for the Player Repository.
"""

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Player, Position
from repositories import PlayerRepository


def create_maker():
    """
    Creates the SQL Alchemy Session Maker.
    """

    engine = create_engine('sqlite://')
    Player.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_player_exists():
    """
    Tests if a player exists.
    """
    maker = create_maker()
    player = Player(id=1, url="www.google.com", name="Jim Smith")
    repo = PlayerRepository(maker)
    repo.save(player)

    result = repo.player_exits(player)
    assert_that(result).is_true()


def test_player_does_not_exist():
    """
    Tests if a player does not exist.
    """
    maker = create_maker()
    player = Player(id=1, url="www.google.com", name="Jim Smith")
    player2 = Player(id=2, url="www.player.com", name="Bill Smith")
    repo = PlayerRepository(maker)
    repo.save(player)

    result = repo.player_exits(player2)
    assert_that(result).is_false()


def test_get_player_by_id():
    """
    Tests retrieving the Player by Id
    """
    maker = create_maker()
    player = Player(id=1, url="www.google.com", name="Jim Smith")
    repo = PlayerRepository(maker)
    repo.save(player)

    result = repo.get_player(id=1)
    assert_that(result).is_not_none().is_equal_to(player)


def test_get_player_by_url():
    """
    Tests retrieving Player by Url.
    """
    maker = create_maker()
    player = Player(id=1, url="www.google.com", name="Jim Smith")
    repo = PlayerRepository(maker)
    repo.save(player)

    result = repo.get_player(url='www.google.com')
    assert_that(result).is_not_none().is_equal_to(player)


def test_get_player_not_exists():
    """
    Tests retrieving a Player that is not present.
    """
    maker = create_maker()
    player = Player(id=1, url="www.google.com", name="Jim Smith")
    repo = PlayerRepository(maker)
    repo.save(player)

    result = repo.get_player(url='www.player.com')
    assert_that(result).is_none()


def test_get_players():
    """
    Tests retrieving all players.
    """
    maker = create_maker()
    player = Player(id=1, url="www.google.com", name="Jim Smith")
    repo = PlayerRepository(maker)
    repo.save(player)

    result = repo.get_players()
    assert_that(result).is_not_empty().contains(player)


def test_get_players_by_position_id():
    """
    Tests retrieving a player by position id
    """
    maker = create_maker()

    position = Position(id=1, code='QB', description='Quarterback')
    player = Player(id=1, url="www.google.com", name="Jim Smith", position_id=1)
    repo = PlayerRepository(maker)
    repo.save_all([player, position])

    result = repo.get_players(position_id=1)
    assert_that(result).is_not_none().contains(player)


def test_get_players_by_position_code():
    """
    Tests retrieving Players by Position Code.
    """
    maker = create_maker()

    position = Position(id=1, code='QB', description='Quarterback')
    player = Player(id=1, url="www.google.com", name="Jim Smith", position_id=1)
    repo = PlayerRepository(maker)
    repo.save_all([player, position])

    result = repo.get_players(position_code='QB')
    assert_that(result).is_not_empty().contains(player)
