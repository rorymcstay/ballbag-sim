from typing import Optional
from ballbag_sim import (
    BallbagRound,
    ManualPlayer,
    BallbagGame,
)


def prompt_for_caller(players) -> ManualPlayer:
    caller = input("Who called ballbag?: ")
    try:

        return players[caller]

    except KeyError as _:
        print(f"Don't recognise that player. {caller}")
        return prompt_for_caller(players)


def print_players(game: BallbagGame):

    for number, player in enumerate(game.leaders):
        print(f"\t{number+1}. {player.number} - {player.total_score}")


def main():
    players: dict[str, ManualPlayer] = {}
    while name := input("\rEnter player name: ").strip():

        players[name] = ManualPlayer(name)

        print(players[name])

    game = BallbagGame(list(players.values()))

    while not game.is_finished:

        print("May the best player win...")
        round = BallbagRound(game.players)
        caller = prompt_for_caller(players)

        for player in players.values():

            player.input_hand()

        round.tally_scores(caller)

        print("Leaders are:")
        print_players(game)

    print("And the winner is:")
    print_players(game)


if __name__ == "__main__":
    main()
