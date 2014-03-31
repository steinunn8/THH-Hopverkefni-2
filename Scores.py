import time, threading

class Score(object):
	def __init__(self, aGame):
		self.game = aGame
		self.bonusTime = ''
		self.startTime = time.time()
		self.bonus_seconds = 0
		self.bonus_minutes = 3
		self.startBonusTime()
		
	#returns the sum of all points for that game
	def getScore(self):
		timePoints = self.getTimePoints()
		deckPoints = self.getDeckPoints()
		pyramidPoints = self.getPyrPoints()
		winPoints = self.getWinPoints()
		return timePoints + deckPoints + pyramidPoints + winPoints
	
	#returns a string that says "Score: " and the current score
	def getCurrentPoints(self):
		pyramidLength = len(self.game.pyramid)
		height = self.game.height
		sortsOn = self.game.sortsOn
		points = "Score: " + str(self.getPyrPoints())
		return points
	
	#returns the number of points you got for finishing the game early
	def getTimePoints(self):
		time = self.game.time
		timeBonus = 180  #3 minutes
		if(time > timeBonus):
			return 0
		return int((timeBonus-time)*10)

	#returns the number of points you got for not using all the cards in the Deck
	def getDeckPoints(self):
		deckLength = len(self.game.deck.deck)
		return deckLength*100

	#returns the number of points you got for removing cards off the pyramid
	def getPyrPoints(self):
		pyramidLength = len(self.game.pyramid)
		height = self.game.height
		origPyrLength = self.getOrigPyramidLength(height)
		sortsOn = self.game.sortsOn
		sortsOnMultiply = 2
		if(sortsOn):
			return (origPyrLength - pyramidLength)*1000*sortsOnMultiply
		return (origPyrLength - pyramidLength)*1000

	#returns the number of points you got for winning the game
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
	
	#returns the number of cards in a pyramid that has the height=height
	def getOrigPyramidLength(self, height, count=0):
		if(height == 0):
			return count
		return self.getOrigPyramidLength(height-1, count+height)

	#adds the string score into a textfile
	def addScore(self, score):
		scores = open('allScores.txt', 'a')
		scores.write(score)	
		scores.close()

	#adds the string name into a textfile
	def addName(self, name):
		scores = open('allScores.txt', 'a')
		scores.write(name)	
		scores.close()

	#returns a matrix that has the all the scores and names, that is [[name1, score1],[name2, score2],...]
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
		
	#returns a matrix with the top five scores and name with the score in a descending order
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

	#returns a string that explains how the game works
	def getHelp(self):
		temp = open('help.txt', 'r')
		string = temp.read()
		temp.close()
		return string
	
	#returns a string with the top 5 scores and names with the score in a descending order
	def getHighScoreString(self):
		list = self.getHighScores()
		for i in range(0, len(list)):
			list[i] = (str(i+1) + '. ' + str(list[i][0]) + ' ' + str(list[i][1]) + '\n')
		tempString = ''
		for i in range(0, len(list)):
			tempString = tempString + list[i]
		return tempString
	
	#updated the string bonusTime so there can be a countdown (?)
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
	
	#returns a string that says 'Timebonus: ' and the time that is left on the time bonus
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
