from src.deck import Deck
import numpy as np


class scoring:
    def __init__(self):
        # Wins, ties, tricks per deck, and cards per trick.
        self.score = np.zeros((8, 8, 4))
        self.strategies = [
            ['R', 'R', 'R'], ['B', 'B', 'B'],
            ['R', 'B', 'B'], ['B', 'B', 'R'],
            ['R', 'R', 'B'], ['B', 'R', 'R'],
            ['R', 'B', 'R'], ['B', 'R', 'B'],
        ]

    def play(self, decks: Deck | np.ndarray, scoring: str = 'trick'):
        if scoring not in ('trick', 'cards'):
            raise ValueError("Scoring must be 'trick' or 'cards'.")

        cards = self._prepare_decks(decks)
        codes = self._strategy_codes()
        patterns = self._find_patterns(cards)

        self.score.fill(0)
        for i, p1_code in enumerate(codes):
            for j in range(i + 1, len(codes)):
                tricks, captured = self._play_pair(patterns, (p1_code, codes[j]))
                self._record_results(i, j, tricks, captured, scoring)

        return self.score

    def _prepare_decks(self, decks):  #essentially converts the decks to a 2D numpy array of 0s and 1s
        if isinstance(decks, Deck):
            decks = decks.decks
        cards = np.asarray(decks)
        if cards.ndim == 1:
            cards = cards[:, None]
        if cards.ndim != 2 or 0 in cards.shape:
            raise ValueError('Decks must be a nonempty (cards, decks) array.')
        if not np.all((cards == 0) | (cards == 1)):
            raise ValueError('Cards must be 0 (B) or 1 (R).')
        return cards

    def _strategy_codes(self):
        codes = []
        for first, second, third in self.strategies:
            code = 4 * (first == 'R') + 2 * (second == 'R') + (third == 'R')
            codes.append(code)
        return codes

    def _find_patterns(self, cards):
        patterns = np.zeros(cards.shape, dtype=np.int8)
        if cards.shape[0] >= 3:
            patterns[2:] = 4 * cards[:-2] + 2 * cards[1:-1] + cards[2:]
        return patterns

    def _play_pair(self, patterns, codes):
        num_decks = patterns.shape[1]
        tricks = np.zeros((2, num_decks), dtype=np.int64)
        captured = np.zeros((2, num_decks), dtype=np.int64)
        pile_length = np.zeros(num_decks, dtype=np.int64)

        for position in range(patterns.shape[0]):
            pile_length += 1
            if position < 2:
                continue
            for player, code in enumerate(codes):
                won = (pile_length >= 3) & (patterns[position] == code)
                tricks[player, won] += 1
                captured[player, won] += pile_length[won]
                pile_length[won] = 0

        return tricks, captured

    def _record_results(self, i, j, tricks, captured, scoring):
        num_decks = tricks.shape[1]
        points = tricks if scoring == 'trick' else captured
        ties = np.count_nonzero(points[0] == points[1])
        for player, row, column in ((0, i, j), (1, j, i)):
            total_tricks = tricks[player].sum()
            cards_per_trick = 0
            if total_tricks:
                cards_per_trick = captured[player].sum() / total_tricks
            self.score[row, column] = [
                np.count_nonzero(points[player] > points[1 - player]),
                ties,
                total_tricks / num_decks,
                cards_per_trick,
            ]
