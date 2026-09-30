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

Once run, the CLI will ask you how many decks you would like to simulate. We recommend that for your first run, you simulate 1,000,000 decks, so the law of large numbers will apply. This should take around 2 minutes or so. After this, you will be prompted to take a look at the heatmap created, which can also be found in `figures/simulation_results.png`. Running the program additional times adds to the number of overall simulations and updates the previous heatmap with the new data.

In the two heatmaps, rows are the opponent's choice and columns are my choice. A label such as `80(8)` means that Player 2 won approximately 80% of the games and tied approximately 8% of them. Darker blue represents a higher win probability. A black border marks the best response for that opponent's choice. Gray diagonal cells are invalid because both players cannot choose the same sequence.

## Findings

For the standard H-N game, the strategy generally follows this rule: take the opponent's first two colors, move them to the end, and place the opposite color at the beginning. For example, the recommended response to `BBB` is `RBB`, and the recommended response to `RBR` is `RRB`.

Ron's variation produces a small change in the optimal response. For `RBR` and its color-swapped equivalent, `BRB`, the best response changes from `RRB` or `BBR` under trick scoring to `BBR` or `RRB` under card scoring, respectively.

Across both scoring rules, Player 1's strongest opening choices are `BRB` and `RBR`. Player 2 still has an advantage after seeing Player 1's choice, but the best response depends on the opening sequence and on whether the game is scored by tricks or by cards. These results come from simulation, so the percentages are estimates rather than exact probabilities.

## Stretch Goal: Why the Strategies Differ

We also tried a numerical-analysis-style approach to this question, but the clearest explanation came from looking at the behavior of the specific strategy matchups. The difference in optimal strategies is concentrated around the `RBR` case and its color-swapped equivalent, `BRB`. These are the cases where the best response and the second-best response are close enough that changing the scoring rule can change which strategy is optimal.

Under trick scoring, the optimal responses mirror the usual Penney's Game strategy because only the number of tricks won matters. Under Ron's variation, however, the number of cards won in each trick also matters. This changes the comparison between `BBR` and `RRB` as responses to `RBR`.

For most opponent choices, there is one clear best response, so switching from trick scoring to card scoring does not change the optimal strategy. The `RBR` case is different because `BBR` and `RRB` are close competitors.

The main question is why `BBR` becomes better than `RRB` against `RBR` under Ron's variation. The answer appears to involve score variance. `RRB` can have a larger average margin when it wins tricks, but the goal is not to maximize the average score difference. The goal is to maximize the number of games won. In Ron's variation, the `BBR` matchup appears to have smaller score variance, which means fewer games move into extreme win/loss outcomes. This leads to fewer losing games overall.

One way to formalize this would be to compute variance using `E(X^2) - E(X)^2`, but we can also reason about the game structure. In the `BBR` versus `RBR` matchup, a `BBR` win tends to leave more red cards in the remaining deck. That increases the chance that `RBR` wins next. When `RBR` wins, it tends to leave more black cards, increasing the chance that `BBR` wins afterward. This creates a negative feedback loop that pulls the deck back toward a more balanced red/black state. Since a balanced deck has relatively shorter expected trick lengths, this reduces the size of extreme outcomes. Even so, `BBR` still benefits under Ron's variation because its average winning trick length remains slightly longer than `RBR`'s.

The `RRB` versus `RBR` matchup behaves differently. It creates more of a positive feedback loop, where wins can increase the number of black cards left in the deck unless a large `BBB` sequence occurs. This does not necessarily increase either strategy's chance of winning the next trick, but it can increase the size of later wins and losses. As a result, the score difference becomes more variable. Even though `RRB` has advantages under trick scoring, the larger variance in Ron's variation pushes more games into the tails and leads to a slightly lower overall game win probability.
