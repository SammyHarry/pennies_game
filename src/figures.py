from pathlib import Path

import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def make_heatmaps(trick_matrix, card_matrix, difference_matrix,
                  trick_labels, card_labels, num_simulations):
    fig, axes = plt.subplots(1, 2, figsize=(16,8))

    for ax, matrix, labels, mode in (
        (axes[0], trick_matrix, trick_labels, 'Tricks'),
        (axes[1], card_matrix, card_labels, 'Cards'),
    ):
        sb.heatmap(
            matrix, annot=labels, fmt='', cmap='Blues',
            vmin=0, vmax=1, cbar=False, square=True,
            linewidths=0.5, linecolor='white', ax=ax,
        )
        best_responses = matrix.eq(matrix.max(axis=1), axis=0)
        for row, column in zip(*best_responses.to_numpy().nonzero()):
            ax.add_patch(Rectangle(
                (column, row), 1, 1, fill=False,
                edgecolor='black', linewidth=2.5, clip_on=False,
            ))
        ax.set_title(f'My Probability of Win(Tie)\nScoring By {mode}\nN={num_simulations:,}')

    for ax in axes:
        ax.set_facecolor('lightgray')
        ax.set_xlabel('My Choice')
        ax.set_ylabel('Opponent Choice')
        ax.tick_params(axis='both', labelrotation=0)

    Path('figures').mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig('figures/simulation_results.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
