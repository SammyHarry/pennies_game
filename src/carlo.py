import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

import src.game as game
import src.figures as figure 


def carlo_simulation(num_simulations=1000, scoring='trick', p1_strategy=['R', 'R', 'R'], p2_strategy=['B', 'B', 'B'], focus = 'p2'):
    results = {'Player 1 Wins': 0, 'Player 2 Wins': 0, 'Ties': 0}
    g = game.Game(scoring=scoring, p1_strategy=p1_strategy, p2_strategy=p2_strategy)

    for _ in range(num_simulations):
        g.play()

    if focus == 'p2':
        results = np.array(g.results())[1] # Player 2 wins + ties
        return results / (num_simulations - np.array(g.results())[2]) # Return probabilities
    results = np.array(g.results())  # Convert to numpy array for easier manipulation
    return results / num_simulations  # Return probabilities



def all_carlo_simulations(num_simulations=10000, scoring='trick'):
    scoring_methods = [scoring]
    strategies = [
        ['R', 'R', 'R'], ['B', 'B', 'B'],
        ['R', 'B', 'B'], ['B', 'B', 'R'],
        ['R', 'R', 'B'], ['B', 'R', 'R'],
        ['R', 'B', 'R'], ['B', 'R', 'B'],
    ]

    all_results = {}

    for scoring in scoring_methods:
        for p1 in strategies:
            for p2 in strategies:
                if p1 != p2:
                    key = (tuple(p1), tuple(p2))
                    all_results[key] = carlo_simulation(num_simulations, scoring=scoring, p1_strategy=p1, p2_strategy=p2)

    return all_results

def results_to_matrix(results):
    probabilities = pd.Series(results)
    probabilities.index = probabilities.index.set_names(
        ["P1 Strategy", "P2 Strategy"]
    )
    return probabilities.unstack("P1 Strategy")





def main(num_simulations=5000):

    num_simulations = num_simulations
  
    trick_results = all_carlo_simulations(num_simulations, scoring="trick")
    card_results = all_carlo_simulations(num_simulations, scoring="cards")


    trick_matrix = results_to_matrix(trick_results)
    card_matrix = results_to_matrix(card_results)

    difference_matrix = trick_matrix - card_matrix

    figure.make_heatmaps(trick_matrix, card_matrix, difference_matrix)
    
    


if __name__ == '__main__':
    main()