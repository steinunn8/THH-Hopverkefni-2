import time

class score(object):
	def __init__(self, aGame):
		self.game = aGame
		self.allScores = self.getScores
		self.highScores = self.getHighScores
		
	def getScore(self):
		sortsOn = self.game.sortsOn
		win = self.game.win
		
		timePoints = self.getTimePoints()
		deckPoints = self.getDeckPoints()
		pyramidPoints = self.getPyrPoints()
		
		sortsOnMultiply = 2
		
		if(sortsOn):
			if(win):
				return int(sortsOnMuliply*(pyramidPoints + winPoints) + deckPoints + timePoints)
			else:
				return int(sortsOnMuliply*pyramidPoints + deckPoints + timePoints)
		else:
			if(win):
				return int(pyramidPoints + winPoints + deckPoints + timePoints)
			else:
				return int(pyramidPoints + deckPoints + timePoints)

	#kristin needs to change kapall because its a self-thingie not agame				
	def getCurrentPoints(self):
		pyramidLength = len(self.game.pyramid)
		height = self.game.height
		sortsOn = self.game.sortsOn
		return self.getPyrPoints() #pyramidLength, height, sortsOn

	def getTimePoints(self):
		time = self.game.time
		timeBonus = 180  #3 minutes
		if(time > timeBonus):
			return 0
		return (timeBonus-time)*10

	def getDeckPoints(self):
		deckLength = len(self.game.deck.deck)
		return deckLength*100

	def getPyrPoints(self):
		pyramidLength = len(self.game.pyramid)
		height = self.game.height
		sortsOn = self.game.sortsOn
		origPyrLength = self.getOrigPyramidLength(height)
		if(sortsOn):
			return (origPyrLength - pyramidLength)*1000*2
		return (origPyrLength - pyramidLength)*1000

	def getOrigPyramidLength(self, height, count=0):
		if(height == 0):
			return count
		return self.getOrigPyramidLength(height-1, count+height)

	def add(self, score):
		scores = open('allScores.txt', 'a')
		scores.write(score)	
		scores.close()

	def getScores(self):
		temp = open('allScores.txt', 'r+')
		str = temp.read()
		temp.close()
		
		listOfScores = str.splitlines()
		scores = []
		for i in range(0, len(listOfScores)):
			scores.append(int(listOfScores[i]))
		return scores
		
	def getHighScores(self):
		scores = self.getScores()
		highScores = []
		if(len(scores) < 5):
			length = len(scores)
		else:
			length = 5
		top = 0
		for i in range(0,length):
			top = max(scores)
			highScores.append(top)
			scores.remove(top)
		return highScores

	def getHelp(self):
		temp = open('help.txt', 'r')
		string = temp.read()
		temp.close()
		return string
		
	def getHighScoreString(self):
		list = self.getHighScores()
		one =  '1. ' + str(list[0]) + '\n'
		two =  '2. ' + str(list[1]) + '\n'
		three = '3. ' + str(list[2]) + '\n'
		four =  '4. ' + str(list[3]) + '\n'
		five =  '5. ' + str(list[4]) + '\n'
		return one + two + three + four + five
