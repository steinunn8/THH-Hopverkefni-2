import Deck, Pyramid, time, Scores
import pygame

class theGame(object):
	def __init__(self, height, sortsOn = False):
		#Make full deck
		deck = Deck.Deck()
		deck.fullDeck()
		#deck.shuffle() Not done because of unittesting

		pyramidObject = Pyramid.Pyramid(deck, height)
		self.pyramid = pyramidObject.getCards() 	#Pyramid cards in list
		self.deck = pyramidObject.getDeck()			#Rest of cards
		self.trash = Deck.Deck()    				#Empty Deck	
		self.sortsOn = sortsOn
		
		self.height = height
		self.start = time.clock()
		#Scores.startBonusTime()
		self.time = 0
		#self.score = 0
		self.win = False
		self.scoreThing = Scores.score(self)
	
	def checkColor(self, x): #x is a card
		y = self.trash.show()
		if((x.red and y.red) or (not x.red and not y.red)): #if both red or both black
			return False
		else:
			return True
	
	def isLegal(self, x): #x is a card
		y = self.trash.show()
		if(self.sortsOn):	
			if(x.isAvailable() and checkColor(x)): #If card has no children and the colors are different
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

	def pick(self, x): #x is a card
		y = self.trash.show()
		if(self.isLegal(x)):
			x.delete()
			self.trash.addFirst(x) 		#add card to trash if legal
			self.pyramid.remove(x)		#remove card from pyramid list
			self.gameWon()				#check if game is over
			return True
		return False

	#Draw from pile and add to trash
	def flip(self):
		if(self.deck.isEmpty()):
			print "You have lost!"
			joker_img = pygame.image.load('joker.png')
			return Deck.Card("Joker", 100, True, joker_img)
		card = self.deck.draw()
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

	def gameWon(self):
		if (len(self.pyramid) == 0):
			score = self.scoreThing.getScore()
			self.scoreThing.add(str(score) + '\n')
			self.win = True
			print "You have won!"
			print "You got: " + str(score) + " points!!"
			print "You took " + str(self.getTime()) + "seconds"
			return True
		else:
			return False

	def getTime(self):
		self.time = time.clock() - self.start
		return self.time
		
	