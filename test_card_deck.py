from ballbag_sim import (
    BallbagGame,
    BallbagRound,
    Card,
    CardDeck,
    EmptyDeckError,
    Player,
    RandomPlayer,
    MaxCardDown,
)


def test_deck_initialisation():

    deck = CardDeck()

    assert len(deck) == 54

    for _ in range(54):
        assert deck.draw()

    with pytest.raises(EmptyDeckError):
        deck.draw()


def test_deck_shuffle():

    deck1 = CardDeck()
    deck2 = CardDeck()

    assert deck1 == deck2

    deck1.shuffle()

    assert deck1 != deck2


def test_card_value():

    assert Card.ACE_DIAMONDS.score == 1
    assert Card.ACE_CLUBS.score == 1
    assert Card.ACE_HEARTS.score == 1
    assert Card.ACE_SPADES.score == 1

    assert Card.TWO_DIAMONDS.score == 2
    assert Card.TWO_CLUBS.score == 2
    assert Card.TWO_HEARTS.score == 2
    assert Card.TWO_SPADES.score == 2

    assert Card.THREE_DIAMONDS.score == 3
    assert Card.THREE_CLUBS.score == 3
    assert Card.THREE_HEARTS.score == 3
    assert Card.THREE_SPADES.score == 3

    assert Card.FOUR_DIAMONDS.score == 4
    assert Card.FOUR_CLUBS.score == 4
    assert Card.FOUR_HEARTS.score == 4
    assert Card.FOUR_SPADES.score == 4

    assert Card.FIVE_DIAMONDS.score == 5
    assert Card.FIVE_CLUBS.score == 5
    assert Card.FIVE_HEARTS.score == 5
    assert Card.FIVE_SPADES.score == 5

    assert Card.SIX_DIAMONDS.score == 6
    assert Card.SIX_CLUBS.score == 6
    assert Card.SIX_HEARTS.score == 6
    assert Card.SIX_SPADES.score == 6

    assert Card.SEVEN_DIAMONDS.score == 7
    assert Card.SEVEN_CLUBS.score == 7
    assert Card.SEVEN_HEARTS.score == 7
    assert Card.SEVEN_SPADES.score == 7

    assert Card.EIGHT_DIAMONDS.score == 8
    assert Card.EIGHT_CLUBS.score == 8
    assert Card.EIGHT_HEARTS.score == 8
    assert Card.EIGHT_SPADES.score == 8

    assert Card.EIGHT_DIAMONDS.score == 8
    assert Card.EIGHT_CLUBS.score == 8
    assert Card.EIGHT_HEARTS.score == 8
    assert Card.EIGHT_SPADES.score == 8

    assert Card.NINE_DIAMONDS.score == 9
    assert Card.NINE_CLUBS.score == 9
    assert Card.NINE_HEARTS.score == 9
    assert Card.NINE_SPADES.score == 9

    assert Card.TEN_DIAMONDS.score == 10
    assert Card.TEN_CLUBS.score == 10
    assert Card.TEN_HEARTS.score == 10
    assert Card.TEN_SPADES.score == 10

    assert Card.JACK_DIAMONDS.score == 10
    assert Card.JACK_CLUBS.score == 10
    assert Card.JACK_HEARTS.score == 10
    assert Card.JACK_SPADES.score == 10

    assert Card.QUEEN_DIAMONDS.score == 10
    assert Card.QUEEN_CLUBS.score == 10
    assert Card.QUEEN_HEARTS.score == 10
    assert Card.QUEEN_SPADES.score == 10

    assert Card.KING_DIAMONDS.score == 10
    assert Card.KING_CLUBS.score == 10
    assert Card.KING_HEARTS.score == 10
    assert Card.KING_SPADES.score == 10

    assert Card.JOKER_1.score == 0
    assert Card.JOKER_2.score == 0


def test_tally_scores():

    game = BallbagGame(
        [
            RandomPlayer(1, hand=[Card.QUEEN_DIAMONDS]),
            RandomPlayer(2, hand=[Card.QUEEN_SPADES]),
        ]
    )

    round = BallbagRound(game.players)

    round.tally_scores(game.players[1])

    game.players[0].total_score = 0
    game.players[1].total_score = 30

    game = BallbagGame(
        [
            RandomPlayer(1, hand=[Card.SEVEN_SPADES]),
            RandomPlayer(2, hand=[Card.QUEEN_SPADES]),
        ]
    )

    round = BallbagRound(game.players)

    round.tally_scores(game.players[0])

    game.players[0].total_score = 0
    game.players[1].total_score = 10


def test_random_players_vs_max_card_down():

    game = BallbagGame(
        [
            RandomPlayer(1),
            RandomPlayer(2),
            MaxCardDown(3),
        ]
    )

    i = 1

    try:

        while not isinstance(game.run(), RandomPlayer):

            i += 1

        print(i)

    except KeyboardInterrupt:
        print(f"\n{i} games played")


test_random_players_vs_max_card_down()
