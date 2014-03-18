import Deck
import Pyramid
import PyramidTree

# height is the number of rows, sortsOn = True is when the sort matters (only red can go and black and vice versa)
class theGame(object):
	def __init__(self, height, sortsOn=False):
		self.deck = Deck.Deck()
		self.deck.fullDeck()
		self.deck.shuffle()
		self.trash = Deck.Deck()
		self.pyramid = Pyramid.Pyramid(height, self.deck)
		self.sortsOn = sortsOn
	
	#the top(first) card in the deck is removed and put on top(first) of the trash deck
	def draw(self):
		self.trash.addFirst(self.deck.draw())
		self.showAll() #remove this!
	
	#AUKA: all cards have been printed
	def showAll(self):
		print 'Deck: '
		self.deck.showAll()
		print ' '
		
		print 'Trash: '
		self.trash.showAll()
		print ' '
		
		print 'Pyramid: '
		self.pyramid.showAll()
	
	#if pyramid[number] is available, then if it is legal it is removed from there and put on top(first) off trash, else returns False
	def pick(self, number):
		if(self.pyramid.isAvailable(number)) and (self.isLegal(number)):
			self.trash.addFirst(self.pyramid.remove(number))
			return True
		else:
			return False
	
	def checkSort(self, cardX, cardY):
		X = cardX[0]
		Y = cardY[0]
		if(((X=="H")or(X=="D"))and((Y=="S")or(Y=="C"))) or (((Y=="H")or(Y=="D"))and((X=="S")or(X=="C"))):
			return True
		else:
			return 

	"""def isLegal(self, number):
		if not(self.pyramid.isAvailable(number)):
			return False
		
		topTrash = self.trash.get(0)
		pyramidCard = self.pyramid.get(number)
		
		if(abs(topTrash[1]-pyramidCard[1]) == 1):
			if(self.sortsOn == False):
				return True
			else:
				if(self.checkSort(topTrash, pyramidCard)):
					return True
		return False"""

	def quit(self):
		exit()
	
	#def newGame(self):


"""NEW NEW NEW"""

class theGame2(object):
	def __init__(self, height, sortsOn = False):
		self.deck = None 			#Get from Edda
		self.trash = Deck.Deck()
		self.pyramid = None			#Get from Edda
		self.sortsOn = sortsOn

	def possitionDeck(self, deck):
		for i in range(0, len(deck)):
			card = deck.draw()
			card.x = 250
			card.y = 300
			deck.addLast(card)
	
	def checkSort(self, cardX, cardY):
		x = cardX
		y = cardY
		if(x.red and y.red or not x.red and not y.red):
			return False
		else:
			return True

	def getPyramid(self):
		self.pyramid = PyramidTree.Pyramid()
		return self.pyramid

	def quit(self):
		exit()






#test:
# test = theGame(3, True)
# test.showAll()
# test.draw() ...
# test.pick(4) ...
	