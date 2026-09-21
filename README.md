# Penney's Game and the Humble–Nishiyama Game

This project uses Monte Carlo simulation to investigate two card-based versions of Penney's Game. We compare every pair of distinct three-color strategies to estimate each player's chance of winning and the chance of a tie.

## How the games work

### Penney's Game

Two players choose different sequences of three coin flips, such as `HHT` (heads, heads, tails). Player 1 chooses first, and Player 2 sees that choice before selecting a sequence. A fair coin is flipped repeatedly until one player's sequence appears in three consecutive flips. That player wins.

Although the coin is fair, the matchups are not equally likely: Player 2 can choose a response with a better than 50% chance of winning. There is no single sequence that beats every other sequence.

### The two H-N variations

The Humble–Nishiyama (H-N) Game replaces coin flips with a shuffled deck of 52 cards: 26 red (`R`) and 26 black (`B`). Each player chooses a different three-color sequence and keeps it for the whole deck.

Deal cards into a pile. When the last three cards match a player's sequence, that player collects the entire pile, winning one **trick**. Start a new pile and continue through the deck. In this implementation, any unmatched cards left at the end score nothing.

We compare two scoring rules:

- **Tricks:** The player who collects more piles wins, regardless of pile size.
- **Cards:** The player who collects more individual cards wins. A large pile is worth more than a small one.

Equal scores produce a tie. Unlike independent coin flips, cards are drawn without replacement, so the remaining color counts change during play.

For background on the original games, see [Winning odds by Yutaka Nishiyama and Steve Humble](https://plus.maths.org/os/issue55/features/nishiyama/index).

## Purpose of the investigation

We want to determine how much advantage Player 2 gains by seeing Player 1's choice, which opening choices give Player 1 the best chance against a strong response, and whether the best strategies change when scoring by cards instead of tricks.

There are eight three-color sequences and 56 ordered matchups between different sequences. The simulation evaluates all of them under both scoring rules. Win and tie probabilities use **all simulated games** as the denominator:

```text
win probability = wins / num_simulations
tie probability = ties / num_simulations
```

Ties are not removed from the denominator.

## How to run

Use Python 3.12 or newer. From the project directory, install the dependencies and run:

```sh
python -m pip install numpy pandas matplotlib seaborn
python main.py
```

Alternatively, with `uv` installed:

```sh
uv sync
uv run python main.py
```

The default is **1,000,000 decks per scoring mode**. For a quicker run:

```sh
python -c "from main import main; main(num_simulations=10000)"
```

The output is `figures/simulation_results.png`, containing trick-scoring, card-scoring, and difference heatmaps. Running the program again overwrites that image.

In the first two heatmaps, rows are Player 1's choice ("Opponent Choice") and columns are Player 2's choice ("My Choice"). A cell labeled `80(8)` means Player 2 won approximately 80% of games and tied approximately 8%. Blue shading represents win probability. A black border marks the best response in each row: the choice with the highest unrounded win probability, including all choices tied for best. Gray diagonal cells exclude identical choices. The third heatmap shows trick win probability minus card win probability; a negative value means the card-scoring win probability is higher.

## Findings

The table below comes from a separate verification run of **100,000 decks with NumPy seed 42**, using the same decks for both scoring modes. Percentages are rounded to one decimal place and are estimates, not exact probabilities. This verification run is separate from the saved heatmap labeled `N=1,000,000`.

Here, Player 2's best response means the sequence with the highest probability of winning outright, with ties reported separately.

| Player 1 | Best response: tricks | P2 win | Tie | Best response: cards | P2 win | Tie |
| --- | --- | --- | --- | --- | --- | --- |
| BBB | RBB | 99.5% | 0.4% | RBB | 100.0% | 0.0% |
| BBR | RBB | 93.6% | 3.8% | RBB | 99.8% | 0.0% |
| BRB | BBR | 80.0% | 8.3% | RRB | 91.9% | 1.3% |
| BRR | BBR | 88.2% | 6.6% | BBR | 95.5% | 0.9% |
| RBB | RRB | 88.4% | 6.5% | RRB | 95.7% | 0.8% |
| RBR | RRB | 80.2% | 8.2% | BBR | 91.8% | 1.4% |
| RRB | BRR | 93.7% | 3.7% | BRR | 99.7% | 0.0% |
| RRR | BRR | 99.5% | 0.4% | BRR | 100.0% | 0.0% |

**Player 1 should choose `BRB` or `RBR`.** These give the highest estimated chance of winning against a Player 2 who chooses a best response: about 12% under trick scoring and 7% under card scoring. They also give the highest worst-case win probabilities across all opposing choices. The two openings are equivalent under swapping red and black; small differences in the estimates come from sampling. Neither removes Player 2's advantage.

**Player 2 should respond to the opening rather than use one fixed sequence.** The best responses agree between scoring modes for six of the eight openings. The exceptions are `BRB` and `RBR`: trick scoring favors `BBR` and `RRB`, respectively, while card scoring reverses those responses. Winning more piles and collecting more cards are different objectives, so the same response need not maximize both.

Card scoring gives Player 2 a higher estimated win probability at each opening's best response and produces fewer ties in these matchups. A displayed `100.0%` is a rounded simulation result, not proof of a guaranteed win.

To reproduce the verification table's underlying scores without changing the seed log or saved figure:

```python
import numpy as np
from src.deck import Deck
from src.scoring import scoring

decks = np.random.default_rng(42).permuted(Deck(100_000).decks, axis=0)
for mode in ('trick', 'cards'):
    game = scoring()
    scores = game.play(decks, scoring=mode)
    names = [''.join(strategy) for strategy in game.strategies]
    print(mode)
    for i in sorted(range(8), key=lambda index: names[index]):
        j = max((j for j in range(8) if j != i),
                key=lambda j: scores[j, i, 0])
        print(names[i], names[j],
              'win:', scores[j, i, 0] / decks.shape[1],
              'tie:', scores[i, j, 1] / decks.shape[1])
```
