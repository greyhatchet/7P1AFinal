import unittest
from question_reader import *

class QuestionReaderTestCase(unittest.TestCase):
    # Tests for question_reader.py

    def test_readQuestion(self):
        self.assertTrue(readQuestion('easy')[1])
        self.assertFalse(readQuestion('not_a_real_category')[1])
        self.assertFalse(readQuestion(True)[1])
        self.assertFalse(readQuestion(0)[1])


if __name__ == '__main__':
    unittest.main()