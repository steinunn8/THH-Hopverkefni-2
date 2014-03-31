import Deck, Pyramid, time, Scores
import pygame

class theGame(object):
	def __init__(self, height, sortsOn = False, shuffle = True):
		#Make full deck
		deck = Deck.Deck()
		deck.fullDeck()
		if shuffle:
			deck.shuffle() 
		pyramidObject = Pyramid.Pyramid(deck, height)
		self.pyramid = pyramidObject.getCards() 	#Pyramid cards in list
		self.deck = pyramidObject.getDeck()			#Rest of cards
		self.trash = Deck.Deck()    				#Empty Deck	
		self.sortsOn = sortsOn
		
		self.height = height
		self.start = time.clock()
		self.time = self.start
		self.win = False
		self.scoreThing = Scores.Score(self)
		self.fromDeck = False
	
	#If color of the x card is not the same as color of first card in trash we return true
	def checkColor(self, x): #x is a card
		y = self.trash.show()
		if((x.red and y.red) or (not x.red and not y.red)): #if both red or both black
			return False
		else:
			return True
	
	#Compares card x to the first card in trash.
	def isLegal(self, x): #x is a card
		if(self.trash.isEmpty()):
			return False
		y = self.trash.show()
		if(x.rank == 100 or y.rank == 100):
			return True
		elif(self.sortsOn):	
			if(x.isAvailable() and self.checkColor(x)): #If card has no children and the colors are different
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

	#We remove card from pyramid if it meets conditions
	def pick(self, x): #x is a card
		y = self.trash.show()
		if(self.isLegal(x)):
			x.x = 450
			x.y = 570
			x.formDeck = False
			self.trash.addFirst(x) 		#add card to trash if legal
			self.pyramid.remove(x)      #remove card from pyramid list
			x.delete()				
			self.gameWon()				#check if game is over
			return True
		return False

	#Draw from pile and add to trash.
	def flip(self):
		if(self.deck.isEmpty()):
			joker_img = pygame.image.load('joker.png')
			return Deck.Card("Joker", 100, True, joker_img)	
		card = self.deck.draw()
		card.fromDeck = True
		self.trash.addFirst(card)
		return card

	#Prints out cards in all decks
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

	#gives self.win and self.time the correct value and return True if you have won the game, else it returns False
	def gameWon(self):
		if (len(self.pyramid) == 0):
			self.win = True
			self.setTime()
			return True
		else:
			return False

	#returns the time that has elapsed at the moment
	def getTime(self):
		return time.clock() - self.start
	
	#updates self.time the amount of time it took the play the game
	def setTime(self):
		self.time = time.clock() - self.start

	#puts x back into Deck
	def undoDraw(self, x):
		self.deck.addFirst(x)
		self.trash.draw()
