import subprocess
from src.carlo import main as carlo_main


def main() -> None:
    while True:
        num_decks = input('How many decks do you want to simulate? ').replace(",", "")
        if not num_decks.isdecimal():
            print('Please enter a positive whole number.')
            continue

        if int(num_decks) <= 0:
            print('Please enter a positive whole number.')
            continue

        carlo_main(num_simulations=int(num_decks))
        break
    print('Simulation Complete!')
    while True:
        response = input('Would you like to see the Heat Map? (y/n)')
        if response == 'yes' or response == 'y':
            subprocess.run('start "" "figures/simulation_results.png"', shell=True)
            break
        
        elif response == 'no' or response == 'n':
            print('That\'s a shame. The heatmap is pretty cool. Goodbye :(')
            break
        else:
            print('Please enter "y" or "n".')
            continue

        


    



if __name__ == '__main__':
    main()
