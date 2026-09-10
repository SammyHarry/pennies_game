import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

def make_heatmaps(trick_matrix, card_matrix, difference_matrix):

    fig, axes = plt.subplots(1, 3, figsize=(24, 7))

    sb.heatmap(
        trick_matrix,
        annot=True,
        fmt=".3f",
        vmin=0,
        vmax=1,
        ax=axes[0],
    )
    axes[0].set_title("Trick Scoring")

    sb.heatmap(
        card_matrix,
        annot=True,
        fmt=".3f",
        vmin=0,
        vmax=1,
        ax=axes[1],
    )
    axes[1].set_title("Card Scoring")

    sb.heatmap(
        difference_matrix,
        annot=True,
        fmt=".3f",
        center=0,
        vmin=-.2,
        vmax=.2,
        cmap="coolwarm",
        ax=axes[2],
    )
    axes[2].set_title("Trick − Card")

    fig.savefig('figures/simulation_results.png', dpi=300)

    # Close the figure after saving.
    plt.close(fig)

    return None

