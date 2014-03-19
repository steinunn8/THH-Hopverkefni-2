import unittest
import theGame
import Pyramid
import Deck

class testMaxFunctions(unittest.TestCase):
	
# Deck
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
	
# theGame
	def test_checkSort(self):
		testGame = theGame.theGame(2)
		testGame.flip()
		cardX1 = Deck.Card("H", 1, True)
		cardX2 = Deck.Card("S", 4, False)
		self.assertEqual(testGame.checkSort(cardX1), False)
		self.assertEqual(testGame.checkSort(cardX2), True)
	def test_isLegal(self):
		testGame = theGame.theGame(2)
		testGame.flip()
		cardX1 = Deck.Card("H", 1, True)
		cardX2 = Deck.Card("S", 3, True) #first trash is 4..
		self.assertEqual(testGame.isLegal(cardX1), False)
		self.assertEqual(testGame.isLegal(cardX2), True)

if __name__ == '__main__':
	unittest.main(verbosity=2, exit=False)