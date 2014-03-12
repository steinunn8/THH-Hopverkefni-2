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
				card = Card(suit[i], rank[j])
				self.deck.append(card)

	def shuffle(self):
		random.shuffle(self.deck)
	
	#Shows first card and then removes it from the deck	
	def draw(self):
		self.isEmpty()
		return self.deck.pop(0)

	#Shows first card in deck but does not remove it
	def show(self, key=0):
		return self.deck[key]

	def addFirst(self,card):
		self.deck.insert(0,card)

	def addLast(self,card):
		self.deck.append(card)

	def emptyDeck(self):
		self.deck = []

	def isEmpty(self):
		return self.deck == []


class Card(object):
	def __init__(self, Suit, Rank, Up = False, Left = False, Right = False):
		self.suit = Suit
		self.rank = Rank
		self.up = Up
		self.left = Left
		self.right = Right

	#When str() is used on Card, [X Y] will be the output 
	#where X is the suit of the card and Y is the rank
	def __str__(self):
		return "["+self.suit+" "+str(self.rank)+"]"



#Test deck
hand = Deck()
hand.shuffle()
"""for i in range(0, 52):
		print hand.show(i),
class Tree(object):
	def __init__(self, Height):
		self.height = Height

"""

