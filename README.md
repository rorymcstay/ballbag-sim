# ball-bag sim

<!--toc:start-->
- [ball-bag sim](#ball-bag-sim)
  - [Player Interface](#player-interface)
  - [Player types](#player-types)
<!--toc:end-->

A simulator for the card game ball-bag, aka [Yaniv](https://github.com/rorymcstay/ballbag-sim).

##  Player Interface
To implement player behaviour. Implement the following interface.

```python
class Player:

  def call(self, players) -> bool: ...
  def draw_card(self, deck: CardDeck, pile: list[Card]) -> Card: ...
  def play_cards(self) -> list[Card]: ...
```

## Player types

1. `RandomPlayer`

* Plays single card from hand at random.
* Draws from the deck or pile at random.
* Calls ballbag once less than 7 is achieved.

2. `MaxCardDown`

* Plays its single maximum card on turn.
* Draws from the deck or pile at random.
* Calls ballbag once less than 7 is achieved.

## Up next

* Data collection
* Common strategy implementations

