scores = []
highScore = []

def getScore(time, deckLength, pyramidLength, height, sortsOn, win):
	timePoints = getTimePoints(time)
	deckPoints = getDeckPoints(deckLength)
	pyramidPoints = getPyrPoints(pyramidLength, height)
	score = round(pyramidPoints + deckPoints + timePoints)
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
	
def getScores():
	global scores
	for i in range(0, len(scores)):
		print scores[i]