import Trivia.py
import unittest


class testPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("1")

    def testInits(self):
        self.assertEqual(self.player.points, 0)
        self.assertEqual(self.player.name, "1")

    def testAddPoints(self):
        self.player.addPoints(5)
        self.assertEqual(self.player.points, 5)

    def testRemovePoints(self):
        self.player.losePoints(10)
        self.assertEqual(self.player.points, 0)

    def testGetScore(self):
        self.assertEqual(self.player.getScore(), self.player.points)


class testMCQuestion(unittest.TestCase):
    def setUp(self):
        self.question = MCQuestion("question", ["1", "2", "3", "4"], 0, 100)

    def testGetQuestion(self):
        self.assertEqual(self.question.getQuestionText(), ["question", "1: 1", "2: 2", "3: 3", "4: 4"])

    def testGetAnswer(self):
        self.assertEqual(self.question.getAnswer(), "1: 1")

    def testValue(self):
        self.assertEqual(self.question.getValue(), self.question.value)


class testTFQuestion(unittest.TestCase):
    def setUp(self):
        self.question = TFQuestion("question", 0)

    def testGetQuestion(self):
        self.assertEqual(self.question.getQuestionText(), ["question", "1: False", "2: True"])

    def testGetAnswer(self):
        self.assertEqual(self.question.getAnswer(), "False")

    def testValue(self):
        self.assertEqual(self.question.getValue(), self.question.value)

