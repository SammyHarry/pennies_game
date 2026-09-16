import numpy as np
import pandas as pd

from src.deck import Deck
from src.scoring import scoring as Scoring
import src.figures as figure

def _run_simulations(num_simulations: int, scoring: str) -> Scoring:
    """Shuffle one batch and score every strategy pair against it."""
    if isinstance(num_simulations, (bool, np.bool_)) or not isinstance(
        num_simulations, (int, np.integer)
    ) or num_simulations <= 0:
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
    focus: str = 'p2',
):
    p1_wins = scores[i, j, 0]
    p2_wins = scores[j, i, 0]
    ties = scores[i, j, 1]
    if focus == 'p2':
        decisive_games = num_simulations - ties
        return p2_wins / decisive_games if decisive_games else np.nan
    return np.array([p1_wins, p2_wins, ties]) / num_simulations


def carlo_simulation(
    num_simulations: int = 1000,
    scoring: str = 'trick',
    p1_strategy=('R', 'R', 'R'),
    p2_strategy=('B', 'B', 'B'),
    focus: str = 'p2',
):

    strategies = Scoring().strategies
    p1, p2 = list(p1_strategy), list(p2_strategy)
    if p1 not in strategies or p2 not in strategies:
        raise ValueError('Strategies must contain exactly three R/B cards.')
    if p1 == p2:
        raise ValueError('Player strategies must be different.')

    scorer = _run_simulations(num_simulations, scoring)
    i, j = strategies.index(p1), strategies.index(p2)
    return _pair_probabilities(scorer.score, i, j, num_simulations, focus)


def all_carlo_simulations(
    num_simulations: int = 10000, scoring: str = 'trick',
) -> dict:
    scorer = _run_simulations(num_simulations, scoring)
    results = {}
    for i, p1 in enumerate(scorer.strategies):
        for j, p2 in enumerate(scorer.strategies):
            if i != j:
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
