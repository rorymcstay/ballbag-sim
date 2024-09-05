from __future__ import annotations
import enum
import abc
import random
from typing import Optional


# TODO: 'pile' api, for draw from pile, num cards reasonably visible
# TODO: cards to be added to pile in batches, so that player can choose which
#   one accordingly. For example, top/bottom of a run.


class Card(enum.Enum):

    ACE_DIAMONDS = enum.auto()
    TWO_DIAMONDS = enum.auto()
    THREE_DIAMONDS = enum.auto()
    FOUR_DIAMONDS = enum.auto()
    FIVE_DIAMONDS = enum.auto()
    SIX_DIAMONDS = enum.auto()
    SEVEN_DIAMONDS = enum.auto()
    EIGHT_DIAMONDS = enum.auto()
    NINE_DIAMONDS = enum.auto()
    TEN_DIAMONDS = enum.auto()
    JACK_DIAMONDS = enum.auto()
    QUEEN_DIAMONDS = enum.auto()
    KING_DIAMONDS = enum.auto()

    ACE_HEARTS = enum.auto()
    TWO_HEARTS = enum.auto()
    THREE_HEARTS = enum.auto()
    FOUR_HEARTS = enum.auto()
    FIVE_HEARTS = enum.auto()
    SIX_HEARTS = enum.auto()
    SEVEN_HEARTS = enum.auto()
    EIGHT_HEARTS = enum.auto()
    NINE_HEARTS = enum.auto()
    TEN_HEARTS = enum.auto()
    JACK_HEARTS = enum.auto()
    QUEEN_HEARTS = enum.auto()
    KING_HEARTS = enum.auto()

    ACE_SPADES = enum.auto()
    TWO_SPADES = enum.auto()
    THREE_SPADES = enum.auto()
    FOUR_SPADES = enum.auto()
    FIVE_SPADES = enum.auto()
    SIX_SPADES = enum.auto()
    SEVEN_SPADES = enum.auto()
    EIGHT_SPADES = enum.auto()
    NINE_SPADES = enum.auto()
    TEN_SPADES = enum.auto()
    JACK_SPADES = enum.auto()
    QUEEN_SPADES = enum.auto()
    KING_SPADES = enum.auto()

    ACE_CLUBS = enum.auto()
    TWO_CLUBS = enum.auto()
    THREE_CLUBS = enum.auto()
    FOUR_CLUBS = enum.auto()
    FIVE_CLUBS = enum.auto()
    SIX_CLUBS = enum.auto()
    SEVEN_CLUBS = enum.auto()
    EIGHT_CLUBS = enum.auto()
    NINE_CLUBS = enum.auto()
    TEN_CLUBS = enum.auto()
    JACK_CLUBS = enum.auto()
    QUEEN_CLUBS = enum.auto()
    KING_CLUBS = enum.auto()

    JOKER_1 = enum.auto()
    JOKER_2 = enum.auto()

    @property
    def score(self) -> int:
        if self == self.JOKER_1 or self == self.JOKER_2:
            return 0
        return min(self.value % 13, 10) or 10

    def __repr__(self):
        return self.name


class EmptyDeckError(Exception):
    """Raised when the deck is empty and a draw is attempted"""


class CardDeck:
    """Initialise a deck of cards"""

    def __init__(
        self,
        cards: Optional[list[Card]] = None,
    ):
        self._storage = (
            [i.value for i in cards]
            if cards is not None
            else [i for i in reversed(range(1, 55))]
        )

    def __len__(self):
        """The number of cards remaining in the deck"""
        return len(self._storage)

    @property
    def empty(self):
        return len(self._storage) == 0

    def __eq__(self, other):
        return self._storage == other._storage

    def shuffle(self):
        """Shuffle the deck of cards into random order"""
        random.shuffle(self._storage)

    def draw(self) -> Card:
        """Draw a card from the deck"""
        try:
            draw = self._storage.pop(-1)
        except IndexError as ex:
            raise EmptyDeckError from ex
        return Card(draw)


class Player(abc.ABC):

    def __init__(self, number, total_score: int = 0, hand: Optional[list[Card]] = None):
        self._hand: list[Card] = hand or []
        self.number = number
        self.total_score = 0

    def __len__(self):
        return len(self._hand)

    def deal(self, card: Card):
        self._hand.append(card)

    def reset_hand(self):
        self._hand.clear()

    def __repr__(self):
        return f"Player(number={self.number}, current_score={self.score}, total_score={self.total_score})"

    @abc.abstractmethod
    def play_cards(self) -> list[Card]:
        """Select cards from hand to play"""

    @abc.abstractmethod
    def draw_card(self, deck: CardDeck, pile: list[Card]) -> Card:
        """Draw a card from either the deck or the pile"""

    @abc.abstractmethod
    def call(self, players: list[Player]) -> bool:
        """Call ballbag or not at the start of turn"""

    @property
    def score(self):
        return sum((c.score for c in self._hand))


class RandomPlayer(Player):

    def play_cards(self) -> list[Card]:
        card_to_play = random.choice(self._hand)
        return [card_to_play]

    def draw_card(self, deck, pile) -> Card:
        if pile and random.uniform(0, 1) < 0.5:
            # if nothing to select from card
            # select from draw
            replacement = pile[-1]
        else:
            # else randomly select from draw or pile
            replacement = deck.draw()

        return replacement

    def call(self, players: list[Player]) -> bool:
        if self.score <= 7:
            return True
        return False


class MaxCardDown(RandomPlayer):

    def play_cards(self) -> list[Card]:
        card_to_play = max(self._hand, key=lambda i: i.score)
        return [card_to_play]


class BallbagGame:

    def __init__(self, players: list[Player]):
        self.players = players

    @property
    def is_finished(self):
        """Property representing if the game is finished or not"""
        return any(p.total_score > 100 for p in self.players)

    @property
    def leaders(self):
        """Return the players in order"""
        return sorted(self.players, key=lambda i: i.total_score)

    def run(self) -> Player:
        """Play the game and return the winner"""
        try:
            num_rounds = 0
            while not self.is_finished:
                num_rounds += 1
                round = BallbagRound(self.players)
                player = round.run()
                # print(f"Winner of round {num_rounds}: {player}, hand: {player._hand}")

            # print(self.leaders)
            return self.leaders[0]
        finally:
            for p in self.players:
                p.reset_hand()
                p.total_score = 0


class BallbagRound:

    def __init__(
        self,
        players: list[Player],
        card_deck: Optional[CardDeck] = None,
    ):
        """Initialise a round of ballbag"""

        self.card_deck = card_deck or CardDeck()
        self.card_pile = []
        self.players = players

        self.card_deck.shuffle()

        for p in self.players:
            p.reset_hand()

        while all(len(p) < 5 for p in self.players):
            for p in self.players:
                if len(p) == 5:
                    continue

                p.deal(self.card_deck.draw())

        self.card_pile.append(self.card_deck.draw())

    def tally_scores(self, caller: Player):
        """Tally up the points after the round"""

        if any(p.score <= caller.score for p in self.players if p is not caller):
            caller.total_score += 30
        else:
            caller.total_score += 0

        for p in self.players:
            if p is caller:
                continue
            p.total_score += p.score

            if p.total_score and (p.total_score % 25 == 0):
                p.total_score -= 25

    def reset_deck(self):
        """Resets the deck from the card pile"""
        assert self.card_pile and self.card_deck.empty
        self.card_deck = CardDeck(self.card_pile)
        self.card_deck.shuffle()
        self.card_pile = [self.card_deck.draw()]

    @staticmethod
    def validate_played(replacements):
        # TODO: Raise on the following conditions
        # 1. cards are pairs
        # 2. if not pairs, cards are in order of the same suit.
        assert True

    def game_round(self):
        """
        Represents one round of turns in the game. Each player plays
        in sequential order. If in that round, a player calls ballbag,
        the round ends early.
        """

        player = self.players[0]
        for player in self.players:
            # player has chance to call
            if player.call(self.players):
                self.tally_scores(player)
                return False

            # reset the deck if empty
            if self.card_deck.empty:
                self.reset_deck()

            # if not called, player plays their cards
            replacements = player.play_cards()
            self.validate_played(replacements)
            for c in replacements:
                player._hand.remove(c)

            # player then draws from deck or pile
            drawn_card = player.draw_card(self.card_deck, self.card_pile)
            # validate selection here
            if drawn_card == self.card_pile[-1]:
                self.card_pile.remove(drawn_card)
            # player is dealt their selected card
            player.deal(drawn_card)
            # played cards added to the pile
            self.card_pile.extend(replacements)

        return True

    def run(self):
        """Play rounds until"""
        while self.game_round():
            # print(self.players)
            pass

        return min(self.players, key=lambda p: p.score)
