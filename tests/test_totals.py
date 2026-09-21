import os
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from src import carlo
from src.scoring import scoring


class TotalsTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.original_directory = Path.cwd()
        os.chdir(self.directory.name)
        self.addCleanup(self.directory.cleanup)
        self.addCleanup(os.chdir, self.original_directory)

    def test_successive_runs_match_combined_decks(self):
        with patch('src.carlo.figure.make_heatmaps') as graph:
            carlo.main(7)
            self.assertEqual(graph.call_args.args[-1], 7)
            carlo.main(3)

        with np.load('data/totals.npz') as totals:
            self.assertEqual(int(totals['total_decks']), 10)
            for index, mode in enumerate(('trick', 'cards')):
                batches = []
                for count, seed in ((7, index), (3, index + 2)):
                    with np.load(f'data/decks_{count}_seed_{seed}.npz') as saved:
                        batches.append(saved['decks'])
                expected = scoring().play(np.concatenate(batches, axis=1), mode)
                key = ('trick_counts', 'card_counts')[index]
                np.testing.assert_array_equal(totals[key], expected[:, :, :2])
                results = carlo._scores_to_results(expected, 10)
                pd.testing.assert_frame_equal(
                    graph.call_args.args[index], carlo.results_to_matrix(results),
                )
        self.assertEqual(graph.call_args.args[-1], 10)

    def test_failed_second_mode_preserves_saved_totals(self):
        with patch('src.carlo.figure.make_heatmaps'):
            carlo.main(2)
        before = Path('data/totals.npz').read_bytes()
        with patch('src.carlo._run_simulations', side_effect=[scoring(), RuntimeError('failed')]):
            with self.assertRaises(RuntimeError):
                carlo.main(3)
        self.assertEqual(Path('data/totals.npz').read_bytes(), before)

    def test_main_runs_existing_cli(self):
        with patch('src.main_input.main') as cli:
            runpy.run_path(str(self.original_directory / 'main.py'), run_name='__main__')
        cli.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
