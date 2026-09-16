from src.carlo import main as carlo_main


def main(num_simulations: int = 1_000_000) -> None:
    carlo_main(num_simulations=num_simulations)


if __name__ == "__main__":
    main()
