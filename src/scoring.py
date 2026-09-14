from deck import Deck
import numpy as np

class scoring:
    def init(self):
       self.score = np.zeros(shape = (8, 8, 4)) #stragegies x strategies x [p1 wins, ties, avg tricks of p1, avg length of trick of p1]
       self.strategies = [
        ['R', 'R', 'R'], ['B', 'B', 'B'],
        ['R', 'B', 'B'], ['B', 'B', 'R'],
        ['R', 'R', 'B'], ['B', 'R', 'R'],
        ['R', 'B', 'R'], ['B', 'R', 'B'],
        ]
       
       
       
       



