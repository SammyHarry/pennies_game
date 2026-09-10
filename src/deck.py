import numpy as np

class Deck:
    def __init__(self):
        self.cards = self._generate_deck()

    def _generate_deck(self):
        suits = ['R', 'B'] * 26  # 26 red and 26 black cards 
        return [(suit) for suit in suits]

    def shuffle(self):
        np.random.shuffle(self.cards)

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in the deck to deal.")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards



def main():
    deck = Deck()
    print("Initial deck:", deck.cards)
    deck.shuffle()
    print("Shuffled deck:", deck.cards)
    dealt_cards = deck.deal(1)
    print("Dealt cards:", dealt_cards)
    print("Remaining deck:", deck.cards)

if __name__ == '__main__':
    main()