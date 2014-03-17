#Hopverkefni 2
import random

class Deck:
	def __init__(self):
		self.deck = []

	def fullDeck(self):
		suit = ["H", "S", "D", "C"]
		rank = range(1, 14)
		for i in range(0, len(suit)):
			for j in range(0, len(rank)):
				if(i == 0 or i == 2):
					card = Card(suit[i], rank[j], True)
					self.deck.append(card)
				else:
					card = Card(suit[i], rank[j], False)
					self.deck.append(card)					

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

	def addFirst(self,card):
		self.deck.insert(0,card)

	def addLast(self,card):
		self.deck.append(card)

	def emptyDeck(self):
		self.deck = []

	def isEmpty(self):
		return self.deck == []
	
	def showAll(self):
		for i in range(0, len(self.deck)):
			print self.deck[i],
	
	def get(self, number=0):
		return self.deck[number].get()

class Card(object):
	def __init__(self, Suit, Rank, Red, Up = False, Left = None, Right = None):
		self.suit = Suit
		self.rank = Rank
		self.red = Red
		self.up = Up
		self.left = Left
		self.right = Right
		#center of card
		self.x = None
		self.y = None

	#When str() is used on Card, [X Y] will be the output 
	#where X is the suit of the card and Y is the rank
	def __str__(self):
		return "["+self.suit+" "+str(self.rank)+"]"
	
	def get(self):
		return [self.suit, self.rank]


#Test deck
hand = Deck()
hand.fullDeck()
hand.shuffle()
"""for i in range(0, 52):
		print hand.show(i),
class Tree(object):
	def __init__(self, Height):
		self.height = Height
"""

