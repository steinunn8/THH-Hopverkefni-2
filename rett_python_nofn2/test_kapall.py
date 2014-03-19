import unittest
import theGame
import Pyramid
import Deck

class test_Deck_Functions(unittest.TestCase):
	def test_draw(self):
		test_deck = Deck.Deck()
		self.assertEqual(test_deck.draw(), None)
	def test_show(self):
		test_deck = Deck.Deck()
		self.assertEqual(test_deck.show(), None)
	def test_is_empty(self):
		test_deck = Deck.Deck()
		self.assertEqual(test_deck.is_empty(), True)
		test_deck.full_deck()
		self.assertEqual(test_deck.is_empty(), False)
	def test_is_available(self):
		card = Deck.Card("H", 1, True)
		self.assertEqual(card.is_available(), True)
	
class test_theGame_Functions(unittest.TestCase):
	def test_check_color(self):
		test_game = theGame.theGame(2)
		test_game.flip()
		card_x1 = Deck.Card("H", 1, True)
		card_x2 = Deck.Card("S", 4, False)
		self.assertEqual(test_game.check_color(card_x1), False)
		self.assertEqual(test_game.check_color(card_x2), True)
	def test_is_legal(self):
		test_game = theGame.theGame(2)
		test_game.flip()
		card_x1 = Deck.Card("H", 1, True)
		card_x2 = Deck.Card("S", 3, True) #first trash is 4..
		self.assertEqual(test_game.is_legal(card_x1), False)
		self.assertEqual(test_game.is_legal(card_x2), True)

if __name__ == '__main__':
	unittest.main(verbosity=2, exit=False)