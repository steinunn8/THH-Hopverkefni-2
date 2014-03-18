import Deck
		
class CardTree(object):		
	def __init__(self, data):
		self.left = None
		self.right = None
		self.data = data
		self.rightParent = None
		self.leftParent = None
	
	def insert_left(self, data):
		if self.left is None:
			self.left = CardTree(data)
			self.left.rightParent = self
		else:
			self.left.insert_left(data)
	
	def insert_right(self, data, special=False):
		if self.right is None:
			self.right = CardTree(data)
			self.right.leftParent = self
			if(special):
				parent = self
				master = parent.rightParent
				magic = master.right
				magic.left = self.right
				self.right.rightParent = magic.left
		else:
			if(special):
				self.right.insert_right(data,True)
			else:
				self.right.insert_right(data)
		
	#Shows the card (for example temp.show() shows what card temp is)
	def show(self):
		return self.data

class Pyramid:
	def __init__(self, deck, height):
		self.height = height
		self.deck = deck
		
		self.deck.fullDeck()
		self.deck.shuffle()
		
		#testing, print cards in deck
		print self.deck.show(0)
		print self.deck.show(1)
		print self.deck.show(2)
		print self.deck.show(3)
		print self.deck.show(4)
		print self.deck.show(5)
		print self.deck.show(6)
		print "same card 1:"
		print self.deck.show(7)
		print "same card 2:"
		print self.deck.show(8)
		print self.deck.show(9)
		
		self.root = CardTree(self.deck.draw())
		
		for i in range(0, self.height-1):
			self.root.insert_left(self.deck.draw())
			self.root.insert_right(self.deck.draw())
		
		#finish pyramid with magic (make a function tomorrow...)
		for i in range(self.height-2, 0, -1):
			if(i == self.height-2):
				for j in range(0, i):
					self.root.left.insert_right(self.deck.draw(),True)
			if(i == self.height-3):
				for j in range(0, i):
					self.root.left.left.insert_right(self.deck.draw(),True)
			if(i == self.height-4):
				for j in range(0, i):
					self.root.left.left.left.insert_right(self.deck.draw(),True)
			if(i == self.height-5):
				for j in range(0, i):
					self.root.left.left.left.left.insert_right(self.deck.draw(),True)
			if(i == self.height-6):
				for j in range(0, i):
					self.root.left.left.left.left.left.insert_right(self.deck.draw(),True)
				
		
		#testing if the cards came out right
		print self.root.show()
		
		print self.root.left.show()
		print self.root.right.show()
		
		print self.root.left.left.show()
		print self.root.right.right.show()
		
		print self.root.left.left.left.show()
		print self.root.right.right.right.show()
		
		print "same card 1:"
		print self.root.left.right.show()
		print self.root.left.right.right.show()
		print self.root.left.left.right.show()
		
		print "same card 2:"
		print self.root.left.right.right.show()
		

#test
deck = Deck.Deck()
pyramid = Pyramid(deck, 4)
