def getScore(time, deckLength, pyramidLength, height, sortsOn, win):
	timePoints = getTimePoints(time)
	deckPoints = getDeckPoints(deckLength)
	pyramidPoints = getPyrPoints(pyramidLength, height)
	score = int(pyramidPoints + deckPoints + timePoints)
	sortsOnMuliply = 3
	winPoints = 10000
	if(sortsOn):
		if(win):
			return score*height*sortsOnMuliply + winPoints
		else:
			return score*height*sortsOnMuliply
	else:
		if(win):
			return score*height + winPoints
		else:
			return score*height
			
def getTimePoints(time):
	timeBonus = 180  #3 minutes
	if(time > timeBonus):
		return 0
	return (timeBonus-time)*100
	
def getDeckPoints(deckLength):
	return deckLength*100

def getPyrPoints(pyramidLength, height):
	origPyrLength = getOrigPyramidLength(height)
	return (origPyrLength - pyramidLength)*1000
	
def getOrigPyramidLength(height, count=0):
	if(height == 0):
		return count
	return getOrigPyramidLength(height-1, count+height)
		
def getHighScores():
	scores = getScores()
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

def add(score):
	scores = open('allScores.txt', 'a')
	scores.write(score)	
	scores.close()
	
def getScores():
	temp = open('allScores.txt', 'r+')
	str = temp.read()
	temp.close()
	
	listOfScores = str.splitlines()
	scores = []
	for i in range(0, len(listOfScores)):
		scores.append(int(listOfScores[i]))
	return scores

def getHelp():
	temp = open('help.txt', 'r')
	string = temp.read()
	temp.close()

	return string
	

	
	