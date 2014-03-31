import time, threading

class Score(object):
	def __init__(self, aGame):
		self.game = aGame
		self.bonusTime = ''
		self.startTime = time.time()
		self.bonus_seconds = 0
		self.bonus_minutes = 3
		self.startBonusTime()
		
		
	def getScore(self):
		timePoints = self.getTimePoints()
		deckPoints = self.getDeckPoints()
		pyramidPoints = self.getPyrPoints()
		winPoints = self.getWinPoints()
		return timePoints + deckPoints + pyramidPoints + winPoints
				
	def getCurrentPoints(self):
		pyramidLength = len(self.game.pyramid)
		height = self.game.height
		sortsOn = self.game.sortsOn
		points = "Score: " + str(self.getPyrPoints())
		return points

	def getTimePoints(self):
		time = self.game.time
		timeBonus = 180  #3 minutes
		if(time > timeBonus):
			return 0
		return int((timeBonus-time)*10)

	def getDeckPoints(self):
		deckLength = len(self.game.deck.deck)
		return deckLength*100

	def getPyrPoints(self):
		pyramidLength = len(self.game.pyramid)
		height = self.game.height
		origPyrLength = self.getOrigPyramidLength(height)
		sortsOn = self.game.sortsOn
		sortsOnMultiply = 2
		if(sortsOn):
			return (origPyrLength - pyramidLength)*1000*sortsOnMultiply
		return (origPyrLength - pyramidLength)*1000

	def getWinPoints(self):
		sortsOnMultiply = 2
		sortsOn = self.game.sortsOn
		win = self.game.win
		winPoints = 1000
		if(win):
			if(sortsOn):
				return winPoints*sortsOnMultiply
			else:
				return winPoints
		else:
			return 0
	
	def getOrigPyramidLength(self, height, count=0):
		if(height == 0):
			return count
		return self.getOrigPyramidLength(height-1, count+height)

	def addScore(self, score):
		scores = open('allScores.txt', 'a')
		scores.write(score)	
		scores.close()

	def addName(self, name):
		scores = open('allScores.txt', 'a')
		scores.write(name)	
		scores.close()

	def getAllScores(self):
		temp = open('allScores.txt', 'r+')
		scores = []
		string = temp.read()
		lines = string.split('\n')
		scores = []
		for i in range(0,len(lines)-1):
			scores.append(lines[i].split('\t'))
		for i in range(0,len(scores)):
			scores[i][1] = int(scores[i][1])
		temp.close()
		return scores
		
	def getHighScores(self):
		scores = self.getAllScores()
		highScores = []
		if(len(scores) < 5):
			length = len(scores)
		else:
			length = 5
		sortedScores = sorted(scores, key=lambda score:score[1], reverse=True)
		#sortedScores = sorted(scores, reverse=True)
		
		for i in range(0,length):
			highScores.append(sortedScores[i])
		return highScores

	def getHelp(self):
		temp = open('help.txt', 'r')
		string = temp.read()
		temp.close()
		return string
		
	def getHighScoreString(self):
		list = self.getHighScores()
		for i in range(0, len(list)):
			list[i] = (str(i+1) + '. ' + str(list[i][0]) + ' ' + str(list[i][1]) + '\n')
		tempString = ''
		for i in range(0, len(list)):
			tempString = tempString + list[i]
		return tempString
	
	def startBonusTime(self):
		timer = threading.Timer(1.0, self.startBonusTime)
		timer.start()
		
		elapsedTime = int(time.time() - self.startTime)
		secondsLeft = self.bonus_seconds - elapsedTime
		
		if (self.bonus_minutes < 0):
			timer.cancel()
			threading.Event().set()
			secondsLeft = 0
			return
			
		if(secondsLeft < 10):
                        self.bonusTime = 'Timebonus: ' + '0' + str(self.bonus_minutes) + ':0' + str(secondsLeft)
		else:
                        self.bonusTime = 'Timebonus: ' + '0' + str(self.bonus_minutes) + ':' + str(secondsLeft)

		if (secondsLeft <= 0):
			self.startTime = time.time()
			self.bonus_seconds = 60
			self.bonus_minutes -= 1
	
	def getBonusTime(self):
		return self.bonusTime

	# Returns a string with info about how the points where divided
	def getDivided(self):
		time = self.getTimePoints()
		deck = self.getDeckPoints()
		pyr = self.getPyrPoints()
		win = self.getWinPoints()

		sTime = '          ' + str(time) + " points for being quick. \n"
		sDeck = '          ' + str(deck) + " points for having many cards left in the deck. \n"
		sPyr = '          ' + str(pyr) + " points for removing pyramid cards. \n"
		sWin = '          ' + str(win) + " points for winning the game. \n"

		return sTime + sDeck + sPyr + sWin
