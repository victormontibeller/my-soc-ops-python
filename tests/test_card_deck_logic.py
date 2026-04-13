import pytest

from app.data import QUESTIONS
from app.game_logic import generate_card_deck, draw_card
from app.game_service import GameSession
from app.models import GameState, CardDeckItem


class TestCardDeckItem:
    def test_card_deck_item_has_id_and_text(self):
        item = CardDeckItem(id=0, text="hello")
        assert item.id == 0
        assert item.text == "hello"

    def test_card_deck_item_is_frozen(self):
        item = CardDeckItem(id=0, text="hello")
        with pytest.raises(Exception):
            item.text = "changed"  # type: ignore[misc]


class TestGenerateCardDeck:
    def test_deck_has_24_cards(self):
        deck = generate_card_deck()
        assert len(deck) == 24

    def test_all_items_are_card_deck_items(self):
        deck = generate_card_deck()
        assert all(isinstance(item, CardDeckItem) for item in deck)

    def test_all_questions_from_pool(self):
        deck = generate_card_deck()
        for item in deck:
            assert item.text in QUESTIONS

    def test_items_have_unique_ids(self):
        deck = generate_card_deck()
        ids = [item.id for item in deck]
        assert len(ids) == len(set(ids))

    def test_deck_is_shuffled(self):
        # Run 3 times; at least one pair should differ (probability of all matching is astronomically low)
        decks = [generate_card_deck() for _ in range(3)]
        texts = [[item.text for item in deck] for deck in decks]
        all_same = all(t == texts[0] for t in texts[1:])
        assert not all_same, "Expected at least one shuffled deck to differ from the others"

    def test_deck_has_no_duplicates(self):
        deck = generate_card_deck()
        texts = [item.text for item in deck]
        assert len(texts) == len(set(texts))


class TestDrawCard:
    def test_draw_card_returns_tuple(self):
        deck = generate_card_deck()
        result = draw_card(deck)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_draw_card_returns_first_card(self):
        deck = generate_card_deck()
        drawn, _ = draw_card(deck)
        assert drawn == deck[0]

    def test_draw_card_returns_remaining_deck(self):
        deck = generate_card_deck()
        _, remaining = draw_card(deck)
        assert len(remaining) == len(deck) - 1

    def test_draw_card_remaining_does_not_include_drawn(self):
        deck = generate_card_deck()
        drawn, remaining = draw_card(deck)
        remaining_ids = [item.id for item in remaining]
        assert drawn.id not in remaining_ids

    def test_draw_card_does_not_mutate_original(self):
        deck = generate_card_deck()
        original_length = len(deck)
        original_first_id = deck[0].id
        draw_card(deck)
        assert len(deck) == original_length
        assert deck[0].id == original_first_id


class TestGameSessionCardDeck:
    def test_card_deck_field_defaults_to_empty(self):
        session = GameSession()
        assert session.card_deck == []

    def test_current_card_defaults_to_none(self):
        session = GameSession()
        assert session.current_card is None

    def test_start_card_deck_sets_state(self):
        session = GameSession()
        session.start_card_deck()
        assert session.game_state == GameState.CARD_DECK

    def test_start_card_deck_populates_deck(self):
        session = GameSession()
        session.start_card_deck()
        assert len(session.card_deck) == 24

    def test_start_card_deck_current_card_is_none(self):
        session = GameSession()
        session.start_card_deck()
        assert session.current_card is None

    def test_draw_next_card_sets_current_card(self):
        session = GameSession()
        session.start_card_deck()
        session.draw_next_card()
        assert session.current_card is not None

    def test_draw_next_card_reduces_deck(self):
        session = GameSession()
        session.start_card_deck()
        session.draw_next_card()
        assert len(session.card_deck) == 23

    def test_cards_remaining_property(self):
        session = GameSession()
        session.start_card_deck()
        assert session.cards_remaining == 24
        session.draw_next_card()
        assert session.cards_remaining == 23

    def test_cards_drawn_property_initially_zero(self):
        session = GameSession()
        session.start_card_deck()
        assert session.cards_drawn == 0

    def test_cards_drawn_increments_after_draw(self):
        session = GameSession()
        session.start_card_deck()
        session.draw_next_card()
        assert session.cards_drawn == 1

    def test_draw_next_card_when_empty_sets_current_card_none(self):
        session = GameSession()
        session.start_card_deck()
        for _ in range(24):
            session.draw_next_card()
        # Deck is now exhausted; one more draw should result in None
        session.draw_next_card()
        assert session.current_card is None


class TestGameStateEnum:
    def test_card_deck_state_exists(self):
        assert GameState.CARD_DECK == "card_deck"
