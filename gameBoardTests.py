import gameBoard
import unittest

class testBoardPiece(unittest.TestCase):
    def setUp(self):
        self.board = BoardPiece("red", "1")
        self.assertEqual(self.board.color, "red")
        self.assertEqual(self.board.piece, "1")

    def testWorldScroll(self):
        self.assertEqual(self.board.absX, self.board.xCord)
        self.board.worldScroll(10)
        self.assertEqual(self.board.xCord, self.board.absX - 10)

    def testAddScore(self):
        self.assertEqual(self.board.score, 0)
        self.board.addScore(10)
        self.assertEqual(self.board.score, 10)

    def testMoveCells(self):
        self.board.moveCells(28)
        self.assertEqual(self.board.cell_num, 28)
        self.board.moveCells(1)
        self.assertEqual(self.board.cell_num, 1)

        