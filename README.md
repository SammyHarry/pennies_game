# Penney's Game and the Humble–Nishiyama Game

## Penney's Game

Two players each choose a sequence of three coin flips, using heads (`H`) or tails (`T`), such as `HHT` or `THT`. Player 1 chooses first, and Player 2 chooses after seeing Player 1's sequence.

A coin is flipped repeatedly until one of the chosen sequences appears in three consecutive flips. The player whose sequence appears first wins that round.

## The H-N Game

The Humble–Nishiyama (H-N) Game is a variation of Penney's Game that uses a deck of cards instead of a coin. The deck contains 26 red cards and 26 black cards. Each player chooses a sequence of three colors, such as `RBB` or `BRR`.

Cards are dealt one at a time into a pile. When the most recent three cards match one player's sequence, that player wins the pile, or **trick**. The pile is cleared, and dealing continues until the entire deck has been used. Any cards left in the pile at the end do not count toward either player's score.

This project compares two scoring rules:

- **H-N scoring:** Each player receives one point for every trick they win.
- **Ron's variation:** A player receives the total number of cards in each pile they win instead of one point.

## Purpose of the investigation

There are three main purposes to this investigation.

First, we are developing a well-rounded workflow and improving our skills with repositories and reproducible data analysis.

Second, we are checking the probabilities reported in the [Penney's Game Wikipedia article](https://en.wikipedia.org/wiki/Penney%27s_game).

Third, we are investigating and forming hypotheses about why Ron's variation produces slight differences in the optimal strategies.

The simulation evaluates all 56 ordered matchups between the eight possible three-color sequences. It records each player's win probability and the probability of a tie.

## How to use the code

You will need Python 3.12 or newer. From the project directory, install the dependencies and run the simulation:

```sh
uv sync
uv run python main.py
```

Once ran, the CLI will ask you how many decks you would like to simulate. We recommend that for your first run, you  simulate 1,000,000 decks, so the law of large numbers will apply. This should take around 2 minutes or so. After this you will be prompted to  take a look at the HeatMap created (can also be found in`figures/simulation_results.png`). Running the program additional times adds to number of overall simulations and updates  the previous heatmap with the new data .

In the  two heatmaps, rows are the opponent's choice and columns are my choice. A label such as `80(8)` means that Player 2 won approximately 80% of the games and tied approximately 8% of them. Darker blue represents a higher win probability. A black border marks the best response for that opponent's choice. Gray diagonal cells are invalid because both players cannot choose the same sequence.

## Findings

For the standard H-N game, the strategy generally follows this rule: take the opponent's first two colors, move them to the end, and place the opposite color at the beginning. For example, the recommended response to `BBB` is `RBB`, and the recommended response to `RBR` is `RRB`.

Ron's variation produces a small change in the optimal response. For `RBR` and its color-swapped equivalent, `BRB`, the best response changes from `RRB` or `BBR` under trick scoring to `BBR` or `RRB` under card scoring, respectively.

Across both scoring rules, Player 1's strongest opening choices are `BRB` and `RBR`. Player 2 still has an advantage after seeing Player 1's choice, but the best response depends on the opening sequence and on whether the game is scored by tricks or by cards. These results come from simulation, so the percentages are estimates rather than exact probabilities.
