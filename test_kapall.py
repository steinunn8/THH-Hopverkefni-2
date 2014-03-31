import unittest
import theGame, Pyramid, Deck

class test_Deck_Functions(unittest.TestCase):
	def test_draw(self):
		testDeck = Deck.Deck()
		self.assertEqual(testDeck.draw(), None)
	def test_show(self):
		testDeck = Deck.Deck()
		self.assertEqual(testDeck.show(), None)
	def test_isEmpty(self):
		testDeck = Deck.Deck()
		self.assertEqual(testDeck.isEmpty(), True)
		testDeck.fullDeck()
		self.assertEqual(testDeck.isEmpty(), False)
	def test_isAvailable(self):
		card = Deck.Card("H", 1, True)
		self.assertEqual(card.isAvailable(), True)
	
class test_theGame_Functions(unittest.TestCase):
	def test_checkColor(self):
		testGame = theGame.theGame(2, sortsOn=True, shuffle=False)
		testGame.flip()
		cardX1 = Deck.Card("H", 1, True)
		cardX2 = Deck.Card("S", 4, False)
		self.assertEqual(testGame.checkColor(cardX1), False)
		self.assertEqual(testGame.checkColor(cardX2), True)
	def test_isLegal(self):
		testGame = theGame.theGame(2, sortsOn=False, shuffle=False)
		testGame.flip()
		cardX1 = Deck.Card("H", 1, True)
		cardX2 = Deck.Card("S", 3, False)
		self.assertEqual(testGame.isLegal(cardX1), False)
		self.assertEqual(testGame.isLegal(cardX2), True)
		
class test_Scores_Functions(unittest.TestCase):
	def test_getScore(self):
		testGame = theGame.theGame(2, shuffle=False)
		self.assertEqual(testGame.scoreThing.getScore(), 6794)
	def test_getCurrentPoints(self):
		testGame = theGame.theGame(2, shuffle=False)
		self.assertEqual(testGame.scoreThing.getCurrentPoints(), 'Score: 0')
	def test_getTimePoints(self):
		testGame = theGame.theGame(2, shuffle=False)
		self.assertEqual(testGame.scoreThing.getTimePoints(), 1793)
	def test_getDeckPoints(self):
		testGame = theGame.theGame(2, shuffle=False)
		self.assertEqual(testGame.scoreThing.getDeckPoints(), 5000)
	def test_getPyrPoints(self):
		testGame = theGame.theGame(2, shuffle=False)
		self.assertEqual(testGame.scoreThing.getPyrPoints(), 0)
	def test_getWinPoints(self):
		testGame = theGame.theGame(2, shuffle=False)
		self.assertEqual(testGame.scoreThing.getWinPoints(), 0)
	def test_getOrigPyramidLength(self):
		testGame = theGame.theGame(2, shuffle=False)
		self.assertEqual(testGame.scoreThing.getOrigPyramidLength(testGame.height), 3)
		
if __name__ == '__main__':
	unittest.main(verbosity=2, exit=False)
