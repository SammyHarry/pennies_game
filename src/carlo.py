from pathlib import Path

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
    decks.save_decks(f"data/decks_{num_simulations}_seed_{decks.seed}.npz")
    scorer = Scoring()
    scorer.play(decks, scoring=scoring)
    return scorer


def _pair_probabilities(
    scores: np.ndarray, i: int, j: int, num_simulations: int,
):
    p2_wins = scores[j, i, 0]
    ties = scores[i, j, 1]
    decisive_games = num_simulations
    return p2_wins / decisive_games, ties / decisive_games


def all_carlo_simulations(
    num_simulations: int = 10000, scoring: str = 'trick',
) -> dict:
    scorer = _run_simulations(num_simulations, scoring)
    return _scores_to_results(scorer.score, num_simulations)


def _scores_to_results(scores: np.ndarray, num_simulations: int) -> dict:
    strategies = Scoring().strategies
    results = {}
    for i, p1 in enumerate(strategies):
        for j, p2 in enumerate(strategies):
            if i == j:
                continue
            key = (tuple(p1), tuple(p2))
            results[key] = _pair_probabilities(
                scores, i, j, num_simulations
            )
    return results


def results_to_matrix(results: dict, outcome: int = 0) -> pd.DataFrame:
    probabilities = pd.Series({
        (''.join(p1), ''.join(p2)): values[outcome]
        for (p1, p2), values in results.items()
    })
    probabilities.index = probabilities.index.set_names(
        ['P1 Strategy', 'P2 Strategy']
    )
    # P2 is "My Choice"; the values are P2's win probabilities.
    return probabilities.unstack('P2 Strategy')


def results_to_labels(results: dict) -> pd.DataFrame:
    wins = results_to_matrix(results)
    ties = results_to_matrix(results, outcome=1)
    labels = wins.copy().astype(object)
    for row in wins.index:
        for column in wins.columns:
            labels.loc[row, column] = (
                '' if pd.isna(wins.loc[row, column]) else
                f'{wins.loc[row, column]:.0%}({ties.loc[row, column]:.0%})'.replace('%', '')
            )
    return labels


def main(num_simulations: int = 1_000_000) -> None:
    totals_path = Path('data/totals.npz')
    total_decks = 0
    trick_counts = np.zeros((8, 8, 2), dtype=np.int64)
    card_counts = np.zeros((8, 8, 2), dtype=np.int64)
    if totals_path.exists():
        with np.load(totals_path, allow_pickle=False) as totals:
            total_decks = int(totals['total_decks'])
            trick_counts = totals['trick_counts']
            card_counts = totals['card_counts']

    # Only wins and ties are additive; the other score fields are averages.
    trick_counts = trick_counts + _run_simulations(
        num_simulations, scoring='trick',
    ).score[:, :, :2].astype(np.int64)
    card_counts = card_counts + _run_simulations(
        num_simulations, scoring='cards',
    ).score[:, :, :2].astype(np.int64)
    total_decks += num_simulations

    # Replace saved totals only after both modes finish and writing succeeds.
    pending_path = totals_path.with_name('totals.pending.npz')
    np.savez_compressed(
        pending_path, total_decks=total_decks,
        trick_counts=trick_counts, card_counts=card_counts,
    )
    pending_path.replace(totals_path)

    trick_results = _scores_to_results(trick_counts, total_decks)
    card_results = _scores_to_results(card_counts, total_decks)

    trick_matrix = results_to_matrix(trick_results)
    card_matrix = results_to_matrix(card_results)
    difference_matrix = trick_matrix - card_matrix

    figure.make_heatmaps(
        trick_matrix, card_matrix, difference_matrix,
        results_to_labels(trick_results), results_to_labels(card_results),
        total_decks,
    )


if __name__ == '__main__':
    main()
