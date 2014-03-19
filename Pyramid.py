import Deck
		
'''class CardTree(object):		
	def __init__(self, data, x=None, y=None):
		self.left = None
		self.right = None
		self.data = data
		self.rightParent = None
		self.leftParent = None
		self.x = x
		self.y = y
		self.data.up = False
	
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
			
	def isAvailable(self):
		if(self.left is None and self.right is None):
			return True
		else:
			return False
		
		
	#Shows the card (for example temp.show() shows what card temp is)
	def show(self):
		return self.data'''

class Pyramid:
	def __init__(self, deck, height):
		self.height = height
		self.deck = deck
		
		self.list = []
		
		self.root = self.deck.draw()#CardTree(self.deck.draw(),450,80)
		self.root.x = 450
		self.root.y = 80
		self.list.append(self.root)
		
		for i in range(0, self.height-1):
			self.root.insert_left(self.deck.draw(),self.list)
			self.root.insert_right(self.deck.draw(),self.list)
		
		self.finishPyramid()
		
		for i in range(0, len(self.list)):
			if(self.list[i].isAvailable()):
				self.list[i].up = True
		
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
deck = Deck.Deck()
deck.fullDeck()
deck.shuffle()
pyramid = Pyramid(deck, 4)
