f = open('WholeSeason.txt', 'r')
data = list(f)

#given an play, determines how many points were scored
def get_points(pos):
	if 'makes 3' in pos:
		return 3
	elif 'makes 2' in pos:
		return 2
	elif 'makes' in pos and 'free throw' in pos:
		return 1
	else:
		return 0

#given a play, determines how many points the possessor scores during possession
def rest_of_pos_points(posnum):
	possessor = data[posnum][42:45]
	if possessor == 'N/A':
		return 0
	if 'rebound' in data[posnum]:
		posnum += 1
	points = 0
	while possessor == data[posnum][42:45]:
		points += get_points(data[posnum])
		posnum += 1
	return points

#overall value of a possession (VOP) for the season
def points_and_possessions(data):
	pos = 0
	pts = 0
	possessor = ''
	prev = ''
	for x in range(len(data)):
		if x == 0:
			continue
		pts += get_points(data[x])
		possessor = data[x][42:45]
		if possessor != prev and possessor != 'N/A':
			pos += 1
		prev = possessor
	#print 'Possessions: ' + str(pos) + ' Points: ' + str(pts)
	print 'Value of Possession (VOP): ' + str(float(pts)/pos)

def reb_pctg_after_shot(data):
	shots = 0
	reb = 0
	off = 0
	offpts = 0
	reg = 0
	regpts = 0
	for x in range(len(data)):
		if 'misses 2-pt' in data[x] and 'shot' in data[x] and 'block' not in data[x]:
			shots += 1
			if 'rebound' in data[x+1]:
				reb += 1
				if 'Offensive' in data[x+1]:
					off += 1
					offpts += rest_of_pos_points(x + 2)
				if 'Defensive' in data[x+1]:
					reg += 1
					regpts += rest_of_pos_points(x + 2)
	print 'Missed Shots: ' + str(shots) + ' Total Reb: ' + str(reb) + ' Offensive Reb: ' + str(off) + ' Pts off: ' + str(offpts) + ' Defensive Reb: ' + str(reg) + ' Pts off: ' + str(regpts)

def makes(data):
	twos = 0
	threes = 0
	buckets = 0
	ptsofftwo = 0
	ptsoffthree = 0
	for x in range(len(data) - 1):
		if 'makes' in data[x] and 'shot' in data[x]:
			buckets += 1
			possessor = data[x][42:45]
			y = x + 1
			while data[y][42:45] == possessor:
				y += 1
			if '2-pt' in data[x]:
				twos += 1
				ptsofftwo += rest_of_pos_points(y)
			elif '3-pt' in data[x]:
				threes += 1
				ptsoffthree += rest_of_pos_points(y)
	print 'Buckets: ' + str(buckets) + ' Twos: ' + str(twos) + ' Pts off: ' + str(ptsofftwo) + ' Threes: ' + str(threes) + ' Pts off: ' + str(ptsoffthree)

def get_first_frees(data):
	frees = 0
	pos = 0
	rebopp = 0
	converts = 0
	convertpts = 0
	for x in range(len(data)):
		if 'free throw' in data[x]:
			frees += 1
			if ('1 of 2' in data[x] or '1 of 3' in data[x]) and 'flagrant' not in data[x]:
				pos += 1
			if ('1 of 1' in data[x] or '2 of 2' in data[x] or '3 of 3' in data[x]) and 'flagrant' not in data[x]:
				rebopp += 1
				if 'makes' in data[x]:
					converts += 1
					convertpts += rest_of_pos_points(x + 1)
	#print 'Total free throws: ' + str(frees) + ' Free throw possessions: ' + str(nonpos) + ' Rebound Opportunities: ' + str(rebopp) + ' Converted Frees: ' + str(converts) + ' Points after Conversion: ' + str(convertpts)
	print 'Possessions used per free throw: ' + str(float(pos)/frees) + ' Percentage of free throws with reb opportunity: ' + str(float(rebopp)/frees) + ' VOP after made free throw: ' + str(float(convertpts)/converts)

def reb_pctg_after_free(data):
	reb = 0
	off = 0
	offpts = 0
	reg = 0
	regpts = 0
	for x in range(len(data)):
		if 'misses free throw' in data[x] and ('3 of 3' in data[x] or '2 of 2' in data[x] or '1 of 1' in data[x]) and 'flagrant' not in data[x]:
			if 'rebound' in data[x+1]:
				reb += 1
				if 'Offensive' in data[x+1]:
					off += 1
					offpts += rest_of_pos_points(x + 2)
				if 'Defensive' in data[x+1]:
					reg += 1
					regpts += rest_of_pos_points(x + 2)
	#print 'Reb off Frees: ' + str(reb) + ' Off reb: ' + str(off) + ' Pts off: ' + str(offpts) + ' Def reb: ' + str(reg) + ' Pts off: ' + str(regpts)
	print 'Defensive reb % after missed free throw: ' + str(float(reg)/reb) + ' VOP after missed free throw+offensive reb: ' + str(float(offpts)/off) + ' VOP after missed free throw+defensive reb: ' + str(float(regpts)/reg)

def turnovers(data):
	turnovers = 0
	points = 0
	for x in range(len(data)):
		if 'Turnover' in data[x]:
			turnovers += 1
			points += rest_of_pos_points(x + 1)
	#print 'Turnovers: ' + str(turnovers) + ' Points off: ' + str(points)
	print '(TURNOVERS) VOP after turnover: ' + str(float(points)/turnovers)

def rebounds(data):
	rebounds = 0
	off = 0
	offpts = 0
	reg = 0
	regpts = 0
	for x in range(len(data)):
		if 'rebound' in data[x] and 'Team' not in data[x]:
			rebounds += 1
			if 'Offensive' in data[x]:
				off += 1
				offpts += rest_of_pos_points(x + 1)
			if 'Defensive' in data[x]:
				reg += 1
				regpts += rest_of_pos_points(x + 1)
	#print 'Total Reb: ' + str(rebounds) + ' Offensive Reb: ' + str(off) + ' Pts off: ' + str(offpts) + ' Defensive Reb: ' + str(reg) + ' Pts off: ' + str(regpts)
	print '(REBOUNDS) Defensive reb %: ' + str(float(reg)/rebounds) + ' VOP after defensive reb: ' + str(float(regpts)/reg) + ' VOP after offensive reb: ' + str(float(offpts)/off)

def steals(data):
	steals = 0
	points = 0
	for x in range(len(data)):
		if 'steal' in data[x]:
			steals += 1
			points += rest_of_pos_points(x + 1)
	#print 'Steals: ' + str(steals) + ' Points off: ' + str(points)
	print '(STEALS) VOP after steal: ' + str(float(points)/steals)

def blocks(data):
	blocks = 0
	reb = 0
	off = 0
	offpts = 0
	reg = 0
	regpts = 0
	for x in range(len(data)):
		if 'block by' in data[x]:
			blocks += 1
			if 'rebound' in data[x+1]:
				reb += 1
				if 'Offensive' in data[x+1]:
					off += 1
					offpts += rest_of_pos_points(x + 2) 
				if 'Defensive' in data[x+1]:
					reg += 1
					regpts += rest_of_pos_points(x + 2)
	#print 'Blocks: ' + str(blocks) + ' Total Reb: ' + str(reb) + ' Offensive Reb: ' + str(off) + ' Pts off: ' + str(offpts) + ' Defensive Reb: ' + str(reg) + ' Pts off: ' + str(regpts)
	print '(BLOCKS) Defensive reb % after block: ' + str(float(reg)/reb) + ' VOP after block and offensive reb: ' + str(float(offpts)/off) + ' VOP after block+defensive reb: ' + str(float(regpts)/reg)

def fouls(data):
	fouls = 0
	techs = 0
	offensive = 0
	offpts = 0
	andones = 0
	andonepts = 0
	nonofforandone = 0
	defpts = 0
	flagrants = 0
	flagfts = 0
	possessionsused = 0
	for x in range(len(data)):
		if 'foul by' in data[x] and 'Team' not in data[x]:
			#Technical Fouls aren't personal fouls, don't count toward total
			if 'Technical' in data[x] or 'tech' in data[x]:
				techs += 1
				continue
			fouls += 1
			y = x + 1
			#Offensive fouls
			if 'Offensive' in data[x]:
				offensive += 1
				while data[y][42:45] == data[x][42:45]:
					y += 1
				offpts += rest_of_pos_points(y)
				continue
			#Getting past deadball actions
			while 'enters the game' in data[y] or 'timeout' in data[y]:
				y += 1
			#And 1's
			if '1 of 1' in data[y]:
				andones += 1
				andonepts += rest_of_pos_points(y)
				continue
			#Regular defensive fouls
			nonofforandone += 1
			defpts += rest_of_pos_points(y)
		elif 'flagrant free throw 1' in data[x]:
			fouls += 1
			flagrants += 1
			flagfts += rest_of_pos_points(x)
	#print 'Personal fouls: ' + str(fouls) + ' Offensive: ' + str(offensive) + ' Pts off: ' + str(offpts) + ' And 1\'s: ' + str(andones) + ' Pts off: ' + str(andonepts) + ' Regular fouls: ' + str(nonofforandone) + ' Pts off: ' + str(defpts) 
	#print 'Flagrants: ' + str(flagrants) + ' Pts off: ' + str(flagfts)
	#print 'Possessions used: ' + str(possessionsused)
	#print 'Techs: ' + str(techs)
	print '(FOULS) And1 value: ' + str(float(andonepts)/andones) + ' And1%: ' + str(float(andones)/(fouls - flagrants)) + ' VOP after Def non-And1 foul: ' + str(float(defpts)/nonofforandone) + ' Def Non-And1%: ' + str(float(nonofforandone)/(fouls - flagrants))

points_and_possessions(data)
reb_pctg_after_shot(data)
makes(data)
get_first_frees(data)
reb_pctg_after_free(data)
turnovers(data)
rebounds(data)
steals(data)
blocks(data)
fouls(data)
