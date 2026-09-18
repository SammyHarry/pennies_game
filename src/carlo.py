import numpy as np
import pandas as pd

from src.deck import Deck
from src.scoring import scoring as Scoring
import src.figures as figure


def _run_simulations(num_simulations: int, scoring: str) -> Scoring:
    is_integer = isinstance(num_simulations, (int, np.integer))
    is_boolean = isinstance(num_simulations, (bool, np.bool_))
    if not is_integer or is_boolean or num_simulations <= 0:
        raise ValueError('num_simulations must be a positive integer.')
    if scoring not in ('trick', 'cards'):
        raise ValueError("Scoring must be 'trick' or 'cards'.")

    decks = Deck(num_decks=num_simulations)
    decks.shuffle()
    scorer = Scoring()
    scorer.play(decks, scoring=scoring)
    return scorer


def _pair_probabilities(
    scores: np.ndarray, i: int, j: int, num_simulations: int,
):
    p2_wins = scores[j, i, 0]
    ties = scores[i, j, 1]
    decisive_games = num_simulations - ties
    return p2_wins / decisive_games


def all_carlo_simulations(
    num_simulations: int = 10000, scoring: str = 'trick',
) -> dict:
    scorer = _run_simulations(num_simulations, scoring)
    results = {}
    for i, p1 in enumerate(scorer.strategies):
        for j, p2 in enumerate(scorer.strategies):
            if i == j:
                continue
            key = (tuple(p1), tuple(p2))
            results[key] = _pair_probabilities(
                scorer.score, i, j, num_simulations
            )
    return results


def results_to_matrix(results: dict) -> pd.DataFrame:
    probabilities = pd.Series(results)
    probabilities.index = probabilities.index.set_names(
        ['P1 Strategy', 'P2 Strategy']
    )
    return probabilities.unstack('P1 Strategy')


def main(num_simulations: int = 1_000_000) -> None:
    trick_results = all_carlo_simulations(num_simulations, scoring='trick')
    card_results = all_carlo_simulations(num_simulations, scoring='cards')

    trick_matrix = results_to_matrix(trick_results)
    card_matrix = results_to_matrix(card_results)
    difference_matrix = trick_matrix - card_matrix

    figure.make_heatmaps(trick_matrix, card_matrix, difference_matrix)


if __name__ == '__main__':
    main()
