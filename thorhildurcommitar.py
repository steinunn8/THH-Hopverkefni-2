from PyramidTree import Pyramid
from PyramidTree import CardTree
import Deck

class Game(object):
	def __init__(self, height, sortsOn=False):
		self.sortsOn = sortsOn
		self.height = height
		self.deck = Deck.Deck()
		self.trash = []
		print "Made it here"
		self.deck.fullDeck()
		self.deck.shuffle()
		pyramid = Pyramid(self.deck, self.height)
		# new deck is the rest of the cards after the pyramid has been made
		#self.deck = Pyramid.getDeck()
		self.draw()
		print self.deck.show(0)

	# draw top card from deck and add to trash
	def draw(self):
		self.trash.append(deck.draw())
		print "drew a card"

game = Game(4, True)
