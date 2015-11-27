#create file with position stats

def get_position_stats(players, pos1, pos2):
	MP = THREES = THREESATT = TWOS = TWOSATT = FT = FTA = ORB = DRB = AST = STL = BLK = TOV = PF = 0
	for x in range(1, len(players)):
		prev = players[x-1].split(',')
		entries = players[x].split(',')
		#skip duplicate entries for players who switched teams
		if prev[0] == entries[0]:
			continue
		if entries[2] == pos1 or entries[2] == pos2:
			MP += int(entries[7]) #minutes
			THREES += int(entries[11]) #threes
			THREESATT += int(entries[12]) #three attempts
			TWOS += int(entries[14]) #twos
			TWOSATT += int(entries[15]) #two attempts
			FT += int(entries[18]) # free throws
			FTA += int(entries[19]) # free throw attempts
			AST += int(entries[24]) # assists
			TOV += int(entries[27]) # turnovers
			DRB += int(entries[22]) # defensive rebounds
			ORB += int(entries[21]) # offensive rebounds
			STL += int(entries[25]) # steals
			BLK += int(entries[26]) # blocks
			PF += int(entries[28]) # personal fouls
	
	value = 1.0 / MP * (
		+ 2.7767 * THREES - (.7686 * THREESATT)
		+ 1.7297 * TWOS - (.7422 * TWOSATT)
		+ .9212 * FT - (.3604 * FTA)
		+ .32 * AST
		- 1.1085 * TOV
		+ .3029 * DRB
		+ .9014 * ORB
		+ 1.2399 * STL
		+ .6411 * BLK
		- .3248 * PF)

	#print round(float(THREES)*48/MP, 4), round(float(THREESATT)*48/MP, 4), round(float(TWOS)*48/MP, 4), round(float(TWOSATT)*48/MP, 4), round(float(FT)*48/MP, 4), round(float(FTA)*48/MP, 4), round(float(AST)*48/MP, 4), round(float(TOV)*48/MP, 4), round(float(DRB)*48/MP, 4), round(float(ORB)*48/MP, 4), round(float(STL)*48/MP, 4), round(float(BLK)*48/MP, 4), round(float(PF)*48/MP, 4)
	return value

#determine value given an array with stat totals
def get_value(player, teams):
	#player statistics needed for value formula
	MP = int(player[7])
	THREES = int(player[11])
	THREESATT = int(player[12])
	TWOS = int(player[14])
	TWOSATT = int(player[15])
	FT = int(player[18])
	FTA = int(player[19])
	ORB = int(player[21])
	DRB = int(player[22])
	AST = int(player[24])
	STL = int(player[25])
	BLK = int(player[26])
	TOV = int(player[27])
	PF = int(player[28])
	unadjvalue = 1.0 / MP * (
		+ 2.7767 * THREES - (.7686 * THREESATT)
		+ 1.7297 * TWOS - (.7422 * TWOSATT)
		+ .9212 * FT - (.3604 * FTA)
		+ .32 * AST
		- 1.1085 * TOV
		+ .3029 * DRB
		+ .9014 * ORB
		+ 1.2399 * STL
		+ .6411 * BLK
		- .3248 * PF)
	
	#pace adjustments
	for x in teams:
		if player[4] == x[0:3]:
			team_PACE = float(x.split(' ')[3])
	lg_PACE = 93.9
	pace_adj = lg_PACE / team_PACE
	adjvalue = unadjvalue * pace_adj
	totalvalue = adjvalue*MP
	player.append(totalvalue)
	return player

f = open('brefplayerstats.txt', 'r')
brefstats = list(f)

g = open('teamstats.txt', 'r')
teams = list(g)

print 'MP, 3P, 3PA, 2P, 2PA, FT, FTA, AST, TOV, DRB, ORB, STL, BLK, PF'
pointval = get_position_stats(brefstats, 'PG', '')
wingval = get_position_stats(brefstats, 'SG', 'SF')
bigval = get_position_stats(brefstats, 'PF', 'C')
print pointval
print wingval
print bigval

players = []
for x in brefstats:
	entry = x.split(',')
	#skip total entries for players on multiple teams, skip category markers
	if entry[4] == 'TOT':
		entry.append(0)
		players.append(entry)
	elif entry[0] == 'Rk':
		entry.append('VAL')
		players.append(entry)
	else:	
		players.append(get_value(entry, teams))
#value versus average
for x in players:
	if x[0] == 'Rk':
		x.append('MARGVAL')
		x.append('VAL/36')
	elif x[4] == 'TOT':
		x.append(0)
		x.append(0)
	else:
		if x[2] == 'PG':
			x.append(x[30] - pointval*float(x[7]))
		if x[2] == 'SG' or x[2] == 'SF':
			x.append(x[30] - wingval*float(x[7]))
		if x[2] == 'C' or x[2] == 'PF':
			x.append(x[30] - bigval*float(x[7]))
		x.append(x[31]*36 / float(x[7]))
#get value for players who switched teams
for x in range(1, len(players)):
	if players[x][0] == 'Rk':
		continue
	if players[x][4] == 'TOT':
		rank = players[x][0]
		y = x + 1
		while players[y][0] == rank:
			players[x][30] += players[y][30]
			players[x][31] += players[y][31]
			players[x][32] += players[y][32]
			players[y][0] = 'Del'
			y += 1
#remove category markers, single team totals for players with multiple teams
players = filter(lambda x: x[0] != 'Del' and x[0] != 'Rk', players)
#ranking = sorted(players, key = lambda player: player[31])

h = open('playervalue.txt', 'w')
for x in players:
	h.write(x[1] + ', ' +  str(x[31]) + ', ' +  str(x[32]) + '\n')

