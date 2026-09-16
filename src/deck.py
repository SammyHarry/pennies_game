import json
import time
from pathlib import Path
import numpy as np

class Deck:
    def __init__(self, num_decks: int = 1):
        self.cards = self._generate_deck(num_decks)
        self.PATH_SEED_LOG = Path('data/seed_log.json')
        self.PATH_DECK_LOG = Path('data/deck_log.json')

    def _generate_deck(self, num_decks: int):
        shape = (52, num_decks)
        grid = np.zeros(shape, dtype=int)
        grid[::2,] = 1
        self.decks = grid
        return self.decks

    def shuffle(self):
        rng = np.random.default_rng(seed=self.get_next_seed())

        self.decks = rng.permuted(self.decks, axis=0)
        return self.decks

    def save_decks(self, filename: str):
        np.savez_compressed(filename, decks=self.decks)

    def get_next_seed(self) -> int:
        #make sure parent dir exists
        self.PATH_SEED_LOG.parent.mkdir(parents=True, exist_ok=True)

        #determine next seed
        if not self.PATH_SEED_LOG.exists():
            print(f'NO seed found stat w {0}')
            self.seed = 0
        else:
            with self.PATH_SEED_LOG.open('r') as f:
                seed_log = json.load(f)
            self.seed = seed_log['seed'] +1

        seed_log = {
            'seed' : self.seed,
            'seed_time': str(time.ctime())
        }
        with self.PATH_SEED_LOG.open('w') as f:
                json.dump(seed_log, f)
        return self.seed




def main(num_decks: int = 100):
    deck = Deck(num_decks=num_decks)
    deck.shuffle()
    deck.save_decks(f"data/decks_{num_decks}_{time.ctime()}_seed_{deck.seed}.npz")


if __name__ == '__main__':
    main()
