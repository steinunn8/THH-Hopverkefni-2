import Deck

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
		