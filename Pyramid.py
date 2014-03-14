import Deck
		
class Pyramid(object):		
	def __init__(self, height, deck):
		self.pyramid = []
		self.available = []
		count = self.findCount(height)
		while(count != 0):
			self.pyramid.append(deck.draw())
			count -= 1
		
	# Find the number of cards needed in a Pyramid if the depth is height
	def findCount(self, height, count=0):
		if(height == 0):
			return count
		return self.findCount(height-1, count+height)
	
	# AUKA: prints all the cards that are in the pyramid
	def showAll(self):
		for i in range(0, len(self.pyramid)):
			print self.pyramid[i],
	
	# returns the number of where the kid that is under pyramid[number] and on the right side
	def findKids(self, number, i=0, j=0):
		if(number <= i):
			return number + j+2
		else:
			return self.findKids(number, i+j+2, j+1)

	# returns true if pyramid[number] is available (and exists)
	def isAvailable(self, number):
		kids = self.findKids(number)
		if(len(self.pyramid) <= number):
			return False
		elif(kids > len(self.pyramid)):
			return True
		elif(self.pyramid[kids] == None) and (self.pyramid[kids-1] == None) and (self.pyramid[number] != None):
			return True
		else:
			return False
	
	# AUKA: updates self.available
	def availableCards(self):
		self.available = []
		for i in range(0, len(self.pyramid)):
			if(self.isAvailable(i)) and (self.pyramid[i] != None):
				self.available.append(self.pyramid[i])
	
	# removes self.pyramid[number] and puts None instead
	def remove(self, number):
		temp = self.pyramid[number]
		if(self.isAvailable(number)):
			self.pyramid[number] = None
			#return True #needs fixing
			return temp
		else:
			return False
	
	# AUKA: updates self.available and prints out all available cards
	def showAvailableCards(self):
		self.availableCards()
		for i in range(0, len(self.available)):
			print self.available[i],
	
	def get(self, number):
		return self.pyramid[number].get()
	
		
		
### Test deck
test = Deck.Deck()
test.fullDeck()
test.shuffle()
#pyr = Pyramid(3,test)
#pyr.remove(4)
