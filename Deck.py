import random, sys, pygame

class Deck:
	def __init__(self):
		self.deck = []

	def fullDeck(self):
		suit = ["D", "C", "H", "S"]
		rank = range(1, 14)
		sheet = pygame.image.load('cards.jpg')
		x = 0	# x nd y for cutting down cards pic
		y = 0
		width = 80
		height = 124
		for i in range(0, len(suit)):
			for j in range(0, len(rank)):
				# load sprite image
				rect = pygame.Rect(x,y,width,height)
				image = pygame.Surface(rect.size)
				image.blit(sheet, (0, 0), rect)
				x += 79
				# make card
				if(i == 0 or i == 2):
					card = Card(suit[i], rank[j], True, image)
					self.deck.append(card)
				else:
					card = Card(suit[i], rank[j], False, image)
					self.deck.append(card)
			x = 0		
			y += 123	
		#Add a wild card
		wild_img = pygame.image.load('wild.png')
		wild = Card("Wild", 100, False, wild_img)
		self.deck.append(wild)

	#Shuffle the deck
	def shuffle(self):
		random.shuffle(self.deck)
	
	#Shows first card and then removes it from the deck	
	def draw(self):
		if(not self.isEmpty()):
			return self.deck.pop(0)
		else:
			return

	#Shows first card in deck but does not remove it
	def show(self, key=0):
		if(not self.isEmpty()):
			return self.deck[key]
		else:
			return 

	#Adds card to front of deck (positon 0)
	def addFirst(self,card):
		self.deck.insert(0,card)

	#Adds card to last seat of deck
	def addLast(self,card):
		self.deck.append(card)

	#Makes deck empty
	def emptyDeck(self):
		self.deck = []

	#Checks if deck is empty
	def isEmpty(self):
		return self.deck == []
	
	#Print out the deck, for testing
	def showAll(self):
		if(self.isEmpty()):
			print "is empty"
		for i in range(0, len(self.deck)):
			print self.deck[i],


class Card(object):
	def __init__(self, Suit, Rank, Red, image=None):
		self.suit = Suit
		self.rank = Rank
		self.red = Red 	# True if card is red, else False
		self.up = False
		self.left = None	#left child
		self.right = None	#right child
		self.rightParent = None	
		self.leftParent = None
		#center of card, default position
		self.x = 450
		self.y = 570
		self.image = image
		self.fromDeck = False # True if the card came from the deck

	#When str() is used on Card, [X Y] will be the output 
	#where X is the suit of the card and Y is the rank
	def __str__(self):
		return "["+self.suit+" "+str(self.rank)+"]"
		
	#insert a left child to self
	def insert_left(self, data, list):
		if self.left is None:
			self.left = data
			self.left.rightParent = self
			self.left.x = self.x-60
			self.left.y = self.y+60
			list.append(self.left)
		else:
			self.left.insert_left(data,list)
	
	#insert a rhigt child to self
	def insert_right(self, data, list, special=False):
		#special is True if card has 2 parents, and those parents then need update
		if self.right is None:
			self.right = data
			self.right.leftParent = self
			self.right.x = self.x+60
			self.right.y = self.y+60
			list.append(self.right)
			if(special):
				parent = self #the data's left parent
				master = parent.rightParent #the right parent of parent
				magic = master.right #this card will be data's right parent
				magic.left = self.right #update the right parent of data
				self.right.rightParent = magic #now magic is the data's right parent
		else:
			if(special):
				self.right.insert_right(data,list,True)
			else:
				self.right.insert_right(data,list)
	
	#Removes the card and also the children of the parents 
	def delete(self):
		if self.rightParent is not None:
			right_parent = self.rightParent
			right_parent.left = None
		if self.leftParent is not None:
			left_parent = self.leftParent
			left_parent.right = None
	
	#Return true if the card has no children 
	def isAvailable(self):
		if(self.left is None and self.right is None):
			self.up = True
			return True
		else:
			return False
		
	#Shows the card (for example temp.show() shows what card temp is)
	def show(self):
		return self.data
