import Deck
import Pyramid
import PyramidTree

"""NEW NEW NEW"""

class theGame(object):
	def __init__(self, height, sortsOn = False):
		#Make full deck
		deck = Deck.Deck()
		deck.fullDeck()
		#deck.shuffle()
		pyramidObject = Pyramid.Pyramid(deck, height)

		self.pyramid = pyramidObject.getCards() 	#Pyramid cards in list
		self.deck = pyramidObject.getDeck()			#Rest of cards
		self.trash = Deck.Deck()    			#Empty Deck	
		self.sortsOn = sortsOn

	def positionDeck(self, deck):
		for i in range(0, len(deck)):
			card = deck.draw()
			card.x = 450
			card.y = 500
			deck.addLast(card)
	
	def checkSort(self, x): #x is a card
		y = self.trash.show()
		if((x.red and y.red) or (not x.red and not y.red)):
			return False
		else:
			return True
	
	def isLegal(self, x): #x is a card, h is a CardTree object
		y = self.trash.show()
		if(sortsOn):	
			if(x.isAvailable() and checkSort(x)): #Still a mess
				if(abs(x.rank - y.rank) == 1):
					return True
				elif(abs(x.rank - y.rank) == 12): #if ace and king or king and ace
					return True
			return False
		else:
			if(x.isAvailable()):
				if(abs(x.rank - y.rank) == 1):
					return True
				elif(abs(x.rank - y.rank) == 12): #if ace and king or king and ace
					return True
			return False

	def pick(self, x): #x is a card, h is CardTree
		y = self.trash.show()
		if(isLegal(x)):
			self.trash.addFirst(x)
			return True
		return False

	#Draw from pile and add to trash
	def flip(self):
		if(self.deck.isEmpty()):
			print "Can't flip"
			return
		self.trash.addFirst(deck.draw())

	def showAll(self):
		print 'Deck: '
		self.deck.showAll()
		print ' '
		
		print 'Trash: '
		self.trash.showAll()
		print ' '
		
		print 'Pyramid: '
		for i in range(0, len(self.pyramid)):
			print self.pyramid[i],

	def gameWon(self):
		if len(self.pyramid == 0):
			return True
		else:
			return False

game = theGame(4)
game.showAll()



