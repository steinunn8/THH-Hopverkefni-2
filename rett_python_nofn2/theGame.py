import Deck
import Pyramid

class theGame(object):
	def __init__(self, height, sortsOn = False):
		#Make full deck
		deck = Deck.Deck()
		deck.full_deck()
		#deck.shuffle() Not done because of unittesting

		pyramidObject = Pyramid.Pyramid(deck, height)
		self.pyramid = pyramidObject.get_cards() 	#Pyramid cards in list
		self.deck = pyramidObject.get_deck()			#Rest of cards
		self.trash = Deck.Deck()    				#Empty Deck	
		self.sortsOn = sortsOn
	
	def check_color(self, x): #x is a card
		y = self.trash.show()
		if((x.red and y.red) or (not x.red and not y.red)): #if both red or both black
			return False
		else:
			return True
	
	def is_legal(self, x): #x is a card
		y = self.trash.show()
		if(self.sortsOn):	
			if(x.is_available() and check_color(x)): #If card has no children and the colors are different
				if(abs(x.rank - y.rank) == 1):
					return True
				elif(abs(x.rank - y.rank) == 12): #if ace and king or king and ace
					return True
			return False
		else:
			if(x.is_available()):
				if(abs(x.rank - y.rank) == 1):
					return True
				elif(abs(x.rank - y.rank) == 12): #if ace and king or king and ace
					return True
			return False

	def pick(self, x): #x is a card
		y = self.trash.show()
		if(self.is_legal(x)):
			x.delete()
			self.trash.add_first(x) 		#add card to trash if legal
			self.pyramid.remove(x)		#remove card from pyramid list
			self.game_won()				#check if game is over
			return True
		return False

	#Draw from pile and add to trash
	def flip(self):
		if(self.deck.is_empty()):
			print "You have lost!"
			return Deck.Card("Joker", 100, True)
		card = self.deck.draw()
		self.trash.add_first(card)
		return card

	#Prints out cards in all decks
	def show_all(self):
		print 'Deck: '
		self.deck.show_all()
		print ' '
		
		print 'Trash: '
		self.trash.show_all()
		print ' '
		
		print 'Pyramid: '
		for i in range(0, len(self.pyramid)):
			print self.pyramid[i],

	def game_won(self):
		if (len(self.pyramid) == 0):
			print "You have won!"		#For now, only prints in console
			return True
		else:
			return False

