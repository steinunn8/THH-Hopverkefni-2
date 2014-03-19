import unittest
import theGame
import Deck

class TestDeckFunctions(unittest.TestCase):
	def test_draw(self):
		testDeck = Deck.Deck()
		self.assertEqual(testDeck.draw(), None)
	def test_show(self):
		testDeck = Deck.Deck()
		self.assertEqual(testDeck.show(), None)
	def test_is_empty(self):
		testDeck = Deck.Deck()
		self.assertEqual(testDeck.is_empty(), True)
		testDeck.full_deck()
		self.assertEqual(testDeck.is_empty(), False)
	def test_is_available(self):
		card = Deck.Card("H", 1, True)
		self.assertEqual(card.is_available(), True)
	
class TestTheGameFunctions(unittest.TestCase):
	def test_check_color(self):
		testGame = theGame.theGame(2)
		testGame.flip()
		cardX1 = Deck.Card("H", 1, True)
		cardX2 = Deck.Card("S", 4, False)
		self.assertEqual(testGame.check_color(cardX1), False)
		self.assertEqual(testGame.check_color(cardX2), True)
	def test_is_legal(self):
		testGame = theGame.theGame(2)
		testGame.flip()
		cardX1 = Deck.Card("H", 1, True)
		cardX2 = Deck.Card("S", 3, True) #first trash is 4..
		self.assertEqual(testGame.is_legal(cardX1), False)
		self.assertEqual(testGame.is_legal(cardX2), True)

if __name__ == '__main__':
	unittest.main(verbosity=2, exit=False)
