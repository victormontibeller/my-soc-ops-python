import pytest

from app.data import FREE_SPACE, QUESTIONS
from app.game_logic import (
    generate_scavenger_list,
    get_scavenger_progress,
    toggle_scavenger_item,
)
from app.game_service import GameSession
from app.models import GameState, ScavengerItem


class TestScavengerModel:
    def test_scavenger_item_has_id_text_is_checked_fields(self):
        item = ScavengerItem(id=0, text="bikes to work")
        assert item.id == 0
        assert item.text == "bikes to work"
        assert item.is_checked is False

    def test_scavenger_item_can_be_checked(self):
        item = ScavengerItem(id=0, text="test", is_checked=True)
        assert item.is_checked is True

    def test_scavenger_item_is_frozen(self):
        item = ScavengerItem(id=0, text="test")
        with pytest.raises(Exception):
            item.is_checked = True  # type: ignore[misc]


class TestGenerateScavengerList:
    def test_list_has_24_items(self):
        items = generate_scavenger_list()
        assert len(items) == 24

    def test_all_items_are_unchecked(self):
        items = generate_scavenger_list()
        assert all(item.is_checked is False for item in items)

    def test_items_have_sequential_ids(self):
        items = generate_scavenger_list()
        for idx, item in enumerate(items):
            assert item.id == idx

    def test_all_questions_from_pool(self):
        items = generate_scavenger_list()
        for item in items:
            assert item.text in QUESTIONS

    def test_no_free_space_in_list(self):
        items = generate_scavenger_list()
        assert all(item.text != FREE_SPACE for item in items)


class TestToggleScavengerItem:
    def test_toggle_checks_unchecked_item(self):
        items = generate_scavenger_list()
        assert items[0].is_checked is False
        new_items = toggle_scavenger_item(items, 0)
        assert new_items[0].is_checked is True

    def test_toggle_unchecks_checked_item(self):
        items = generate_scavenger_list()
        items = toggle_scavenger_item(items, 0)
        assert items[0].is_checked is True
        items = toggle_scavenger_item(items, 0)
        assert items[0].is_checked is False

    def test_toggle_returns_new_list(self):
        items = generate_scavenger_list()
        new_items = toggle_scavenger_item(items, 0)
        assert items is not new_items

    def test_toggle_only_affects_target_item(self):
        items = generate_scavenger_list()
        new_items = toggle_scavenger_item(items, 0)
        for item in new_items[1:]:
            assert item.is_checked is False


class TestGetScavengerProgress:
    def test_progress_is_zero_when_no_items_checked(self):
        items = generate_scavenger_list()
        checked, total = get_scavenger_progress(items)
        assert checked == 0
        assert total == 24

    def test_progress_counts_checked_items(self):
        items = generate_scavenger_list()
        items = toggle_scavenger_item(items, 0)
        items = toggle_scavenger_item(items, 1)
        items = toggle_scavenger_item(items, 2)
        checked, total = get_scavenger_progress(items)
        assert checked == 3
        assert total == 24

    def test_progress_when_all_checked(self):
        items = generate_scavenger_list()
        for i in range(24):
            items = toggle_scavenger_item(items, i)
        checked, total = get_scavenger_progress(items)
        assert checked == 24
        assert total == 24


class TestGameSessionScavenger:
    def test_scavenger_items_field_defaults_to_empty_list(self):
        session = GameSession()
        assert session.scavenger_items == []

    def test_start_scavenger_hunt_sets_state(self):
        session = GameSession()
        session.start_scavenger_hunt()
        assert session.game_state == GameState.SCAVENGER_HUNT

    def test_start_scavenger_hunt_populates_items(self):
        session = GameSession()
        session.start_scavenger_hunt()
        assert len(session.scavenger_items) == 24

    def test_handle_scavenger_item_click_toggles_item(self):
        session = GameSession()
        session.start_scavenger_hunt()
        assert session.scavenger_items[0].is_checked is False
        session.handle_scavenger_item_click(0)
        assert session.scavenger_items[0].is_checked is True

    def test_scavenger_progress_property(self):
        session = GameSession()
        session.start_scavenger_hunt()
        progress = session.scavenger_progress
        assert isinstance(progress, tuple)
        assert len(progress) == 2
        checked, total = progress
        assert checked == 0
        assert total == 24

    def test_scavenger_progress_updates_after_click(self):
        session = GameSession()
        session.start_scavenger_hunt()
        checked_before, _ = session.scavenger_progress
        session.handle_scavenger_item_click(0)
        checked_after, _ = session.scavenger_progress
        assert checked_after == checked_before + 1


class TestGameStateEnum:
    def test_scavenger_hunt_state_exists(self):
        assert GameState.SCAVENGER_HUNT == "scavenger_hunt"
