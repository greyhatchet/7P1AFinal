import unittest
from question_reader import *

class QuestionReaderTestCase(unittest.TestCase):
    # Tests for question_reader.py

    def test_readQuestion(self):
        self.assertTrue(readQuestion('test'))
        self.assertFalse(readQuestion('not_a_real_category'))
        self.assertFalse(readQuestion(True))
        self.assertFalse(readQuestion(0))


if __name__ == '__main__':
    unittest.main()