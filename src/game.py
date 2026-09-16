import src.deck as deck

class Game:
    def __init__(self, scoring = 'trick', p1_strategy = ['R', 'R', 'R'], p2_strategy = ['B', 'B', 'B']):
        self.scoring = scoring
        self.deck = deck.Deck()
        self.deck.shuffle()

        self.p1 = p1_strategy #p1 strategy
        self.p2 = p2_strategy #p2 strategy
        if self.p1 == self.p2:
            raise ValueError("Player strategies must be different.")

        self.score = [0,0] #p1 score, p2 score

        self.winner = [0,0,0] #p1 wins, p2 wins, ties

    def score_game(self):
        if self.scoring == 'trick':
            return 1
        elif self.scoring == 'cards':
            return len(self.current)

    def play(self):
        
        self.reset()

        for card in self.deck.decks[:, 0]:
            self.current.append('R' if card == 1 else 'B')
            window = self.current[-3:]
            if window == self.p1:
                self.score[0] += self.score_game()
                self.current = [] 
            elif window == self.p2:
                self.score[1] += self.score_game()
                self.current = []
        self.deck.decks = self.deck.decks[:0]
        if self.score[0] > self.score[1]:
            self.winner[0] += 1
        elif self.score[1] > self.score[0]:
            self.winner[1] += 1
        else:
            self.winner[2] += 1

    def reset (self):
        self.deck = deck.Deck()
        self.deck.shuffle()
        self.current =  []
        self.score = [0,0]

    def results(self):
        return [self.winner[0], self.winner[1],self.winner[2]]


def main():
    game = Game(scoring = 'cards')
    game.play()
    print("Final Score:", game.score)
    print("Winner:", "Player 1" if game.winner[0] > game.winner[1] else "Player 2" if game.winner[1] > game.winner[0] else "Tie")   



if __name__ == '__main__':
    main()
    


        
