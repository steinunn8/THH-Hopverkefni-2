import Deck
		
class CardTree(object):		
	def __init__(self, data, x=None, y=None):
		self.left = None
		self.right = None
		self.data = data
		self.rightParent = None
		self.leftParent = None
		self.x = x
		self.y = y
	
	def insert_left(self, data, list):
		if self.left is None:
			self.left = CardTree(data)
			self.left.rightParent = self
			self.left.x = self.x-80
			self.left.y = self.y+100
			list.append(self.left)
		else:
			self.left.insert_left(data,list)
	
	def insert_right(self, data, list, special=False):
		if self.right is None:
			self.right = CardTree(data)
			self.right.leftParent = self
			self.right.x = self.x+80
			self.right.y = self.y+100
			list.append(self.right)
			if(special):
				parent = self
				master = parent.rightParent
				magic = master.right
				magic.left = self.right
				self.right.rightParent = magic.left
		else:
			if(special):
				self.right.insert_right(data,list,True)
			else:
				self.right.insert_right(data,list)
	
	def delete(self):
		if self.rightParent is not None:
			right_parent = self.rightParent
			right_parent.left = None
		if self.leftParent is not None:
			left_parent = self.leftParent
			left_parent.right = None
		
	#Shows the card (for example temp.show() shows what card temp is)
	def show(self):
		return self.data

class Pyramid:
	def __init__(self, deck, height):
		self.height = height
		self.deck = deck

		self.list = []
		
		print "spil i stokki:"
		print deck.show(0)
		print deck.show(1)
		print deck.show(2)
		print deck.show(3)
		print deck.show(4)
		print deck.show(5)
		print deck.show(6)
		print deck.show(7)
		print deck.show(8)
		print deck.show(9)
		
		self.root = CardTree(self.deck.draw(),450,80)
		self.list.append(self.root)
		
		for i in range(0, self.height-1):
			self.root.insert_left(self.deck.draw(),self.list)
			self.root.insert_right(self.deck.draw(),self.list)
		
		self.finishPyramid()
		
	def getDeck(self):
		return self.deck
	
	def finishPyramid(self):
		for i in range(self.height-2, 0, -1):
			if(i == self.height-2):
				for j in range(0, i):
					self.root.left.insert_right(self.deck.draw(),self.list,True)
			if(i == self.height-3):
				for j in range(0, i):
					self.root.left.left.insert_right(self.deck.draw(),self.list,True)
			if(i == self.height-4):
				for j in range(0, i):
					self.root.left.left.left.insert_right(self.deck.draw(),self.list,True)
			if(i == self.height-5):
				for j in range(0, i):
					self.root.left.left.left.left.insert_right(self.deck.draw(),self.list,True)
			if(i == self.height-6):
				for j in range(0, i):
					self.root.left.left.left.left.left.insert_right(self.deck.draw(),self.list,True)
	
	def getCards(self):
		return self.list
		

#test
#deck = Deck.Deck()
#pyramid = Pyramid(deck, 4)
#print "pyramidi"
#list = pyramid.getCards()
#for i in range(0, len(list)):
#	print list[i].data

