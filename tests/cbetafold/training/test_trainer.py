import unittest

from betafold import Trainer

class TestTrainer(unittest.TestCase):

    def test_testing(self):
        self.assertIsNone(Trainer.train())


if __name__ == '__main__':
    unittest.main()