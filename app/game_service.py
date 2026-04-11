from dataclasses import dataclass, field

from app.game_logic import (
    check_bingo,
    draw_card,
    generate_board,
    generate_card_deck,
    generate_scavenger_list,
    get_scavenger_progress,
    get_winning_square_ids,
    toggle_scavenger_item,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData, CardDeckItem, GameState, ScavengerItem


@dataclass
class GameSession:
    """Holds the state for a single game session."""

    game_state: GameState = GameState.START
    board: list[BingoSquareData] = field(default_factory=list)
    winning_line: BingoLine | None = None
    show_bingo_modal: bool = False
    scavenger_items: list[ScavengerItem] = field(default_factory=list)
    card_deck: list[CardDeckItem] = field(default_factory=list)
    current_card: CardDeckItem | None = None

    @property
    def winning_square_ids(self) -> set[int]:
        """Return the set of square IDs that form the winning bingo line, or empty set."""
        return get_winning_square_ids(self.winning_line)

    @property
    def has_bingo(self) -> bool:
        """Return True when the game is in the BINGO state."""
        return self.game_state == GameState.BINGO

    def start_game(self) -> None:
        """Generate a fresh bingo board and transition to the PLAYING state."""
        self.board = generate_board()
        self.winning_line = None
        self.game_state = GameState.PLAYING
        self.show_bingo_modal = False

    def handle_square_click(self, square_id: int) -> None:
        """Toggle the marked state of a square and check for bingo."""
        if self.game_state != GameState.PLAYING:
            return
        self.board = toggle_square(self.board, square_id)

        if self.winning_line is None:
            bingo = check_bingo(self.board)
            if bingo is not None:
                self.winning_line = bingo
                self.game_state = GameState.BINGO
                self.show_bingo_modal = True

    def reset_game(self) -> None:
        """Clear all game state and return to the START state."""
        self.game_state = GameState.START
        self.board = []
        self.winning_line = None
        self.show_bingo_modal = False
        self.scavenger_items = []
        self.card_deck = []
        self.current_card = None

    def dismiss_modal(self) -> None:
        """Dismiss the bingo modal and resume the PLAYING state."""
        self.show_bingo_modal = False
        self.game_state = GameState.PLAYING

    def start_scavenger_hunt(self) -> None:
        """Initialise the scavenger hunt and transition to SCAVENGER_HUNT state."""
        self.scavenger_items = generate_scavenger_list()
        self.game_state = GameState.SCAVENGER_HUNT

    def handle_scavenger_item_click(self, item_id: int) -> None:
        """Toggle the checked state of the scavenger item with the given ID."""
        self.scavenger_items = toggle_scavenger_item(self.scavenger_items, item_id)

    @property
    def scavenger_progress(self) -> tuple[int, int]:
        """Return (checked_count, total_count) for the scavenger hunt."""
        return get_scavenger_progress(self.scavenger_items)

    def start_card_deck(self) -> None:
        """Shuffle a new 24-card deck and transition to the CARD_DECK state."""
        self.card_deck = generate_card_deck()
        self.current_card = None
        self.game_state = GameState.CARD_DECK

    def draw_next_card(self) -> None:
        """Draw the top card from the deck into current_card, or set it to None when empty."""
        if self.card_deck:
            self.current_card, self.card_deck = draw_card(self.card_deck)
        else:
            self.current_card = None

    @property
    def cards_remaining(self) -> int:
        """Return the number of cards still in the deck (not yet drawn)."""
        return len(self.card_deck)

    @property
    def cards_drawn(self) -> int:
        """Return the number of cards that have been drawn so far.

        The drawn card is removed from self.card_deck when draw_next_card() is
        called, so ``24 - len(self.card_deck)`` correctly counts cards already
        drawn (including the one currently displayed as current_card).
        """
        return 24 - len(self.card_deck)


# In-memory session store keyed by session ID
_sessions: dict[str, GameSession] = {}


def get_session(session_id: str) -> GameSession:
    """Get or create a game session for the given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = GameSession()
    return _sessions[session_id]
