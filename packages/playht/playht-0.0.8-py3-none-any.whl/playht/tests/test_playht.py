import unittest
import os
from playht import PlayHT
from dotenv import load_dotenv

load_dotenv(verbose=True)


class TestPlayHT(unittest.TestCase):
    def setUp(self):
        self.ht = PlayHT(
            user_id=os.getenv('USER_ID'),
            secret_key=os.getenv('SECRET_KEY')
        )

    def test_get_random_voice(self):
        voice = self.ht.get_random_voice()
        self.assertIsNotNone(voice)

    def test_get_random_voices(self):
        voices = self.ht.get_random_voices(2)
        self.assertEqual(len(voices), 2)


# python -m unittest tests/test_playht.py
if __name__ == '__main__':
    unittest.main()
