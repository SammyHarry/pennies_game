import time

import numpy as np
import struct

class Deck:
    def __init__(self, num_decks: int = 1):
        self.cards = self._generate_deck(num_decks)

    def _generate_deck(self, num_decks: int):
        shape = (52, num_decks)
        grid = np.zeros(shape, dtype=int)
        grid[::2,] = 1
        self.decks = grid
        return self.decks

    def shuffle(self):
        rng = np.random.default_rng()

        self.decks = rng.permuted(self.decks, axis=0)
        return self.decks

    def save_decks(self, filename: str):
        np.savez_compressed(filename, decks=self.decks)




def main(num_decks: int = 100):
    deck = Deck(num_decks=num_decks)
    deck.shuffle()
    deck.save_decks(f"data/decks_{num_decks}_{time.ctime()}.npz")


if __name__ == '__main__':
    main()