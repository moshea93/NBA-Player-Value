#player stat lines
f = open('brefplayerstats.txt', 'r')
players = list(f)
#team list with season fieldgoals and assist totals
g = open('teamstats.txt', 'r')
teams = []
for line in g:
	teams.append(line[:-1])
#play by play file
h = open('WholeSeason.txt', 'r')
plays = list(h)

def get_league_stats(plays):
	lg_PF = lg_FTA = lg_FT = lg_FG = lg_AST = lg_PTS = lg_FGA = lg_ORB = lg_TOV = lg_TRB = 0
	for x in range(len(plays)):
		if ('foul by' in plays[x] and not ('Technical' in plays[x] or 'tech' in plays[x])) or 'flagrant free throw 1' in plays[x]:
			lg_PF += 1
		if 'free throw' in plays[x]:
			lg_FTA += 1
			if 'makes' in plays[x]:
				lg_FT += 1
				lg_PTS += 1
		elif 'makes' in plays[x]:
			lg_FGA += 1
			lg_FG += 1
			if '3-pt' in plays[x]:
				lg_PTS += 3
			else:
				lg_PTS += 2
			if 'assist' in plays[x]:
				lg_AST += 1
		elif 'misses' in plays[x]:
			lg_FGA += 1
		elif 'rebound' in plays[x] and 'Team' not in plays[x]:
			lg_TRB += 1
			if 'Offensive' in plays[x]:
				lg_ORB += 1
		elif 'Turnover' in plays[x]:
			lg_TOV += 1
	return lg_PF, lg_FTA, lg_FT, lg_FG, lg_AST, lg_PTS, lg_FGA, lg_ORB, lg_TOV, lg_TRB

lg_PF, lg_FTA, lg_FT, lg_FG, lg_AST, lg_PTS, lg_FGA, lg_ORB, lg_TOV, lg_TRB = get_league_stats(plays)

#definitions
factor = 2.0 / 3 - (.5 * (float(lg_AST) / lg_FG)) / (2 * (float(lg_FG) / lg_FT))
VOP = float(lg_PTS) / (lg_FGA - lg_ORB + lg_TOV + .44 * lg_FTA)
DRBrate = (lg_TRB - lg_ORB) / float(lg_TRB)
lg_PACE = 93.9
totPERunits = 0
totnewPERunits = 0
totminutes = 0
guys = []
PER = []
newPER = []

for x in range(1, len(players)):
	entries = players[x].split(',')
#	if entries[0] == players[x - 1].split(',', 1)[0] or entries[0] == 'Rk':
#		continue
	#temporarily avoid players with multiple teams
	if entries[4] == 'TOT' or entries[0] == 'Rk':
		continue
	for y in teams:
		if entries[4] == y[0:3]:
			match = y.split(' ')
			team_FG = float(match[1])
			team_AST = float(match[2])
			team_PACE = float(match[3])
			break
	MP = int(entries[7])
	FG = int(entries[8])
	FGA = int(entries[9])
	THREES = int(entries[11])
	THREESATT = int(entries[12])
	TWOS = int(entries[14])
	TWOSATT = int(entries[15])
	FT = int(entries[18])
	FTA = int(entries[19])
	ORB = int(entries[21])
	DRB = int(entries[22])
	AST = int(entries[24])
	STL = int(entries[25])
	BLK = int(entries[26])
	TOV = int(entries[27])	
	PF = int(entries[28])
	PTS = int(entries[29])
	
	uPER = 1.0 / MP * (
			THREES
			+ 2.0 / 3 * AST
			+ (2 - factor * (team_AST) / team_FG) * FG
			+ FT * .5 * (1 + (1 - (team_AST) / team_FG) + 2.0 / 3 * team_AST / team_FG)
			- VOP * TOV
			- VOP * DRBrate * (FGA - FG)
			- VOP * .44 * (.44 + .56 * DRBrate) * (FTA - FT)
			+ VOP * (1 - DRBrate) * DRB
			+ VOP * DRBrate * ORB
			+ VOP * STL
			+ VOP * DRBrate * BLK
			- PF * (float(lg_FT) / lg_PF - .44 * float(lg_FTA) / lg_PF * VOP)) 
	
	newuPER = 1.0 / MP * (
			+ 2.7767 * THREES - (.7686 * THREESATT)
			1.7297 * TWOS - (.7422 * TWOSATT)
			+ .9212 * FT - (.3604 * FTA)
			+ .32 * AST
			- 1.1085 * TOV
			+ .3029 * DRB
			+ .9014 * ORB
			+ 1.2399 * STL
			+ .6411 * BLK
			- .3248 * PF)

	pace_adj = lg_PACE / team_PACE
	aPER = pace_adj * uPER
	newaPER = pace_adj * newuPER

	totPERunits += aPER * MP
	totnewPERunits += newaPER * MP
	totminutes += MP

	guys.append(entries[1])
	PER.append(aPER)
	newPER.append(newaPER)

lg_aPER = totPERunits / totminutes
new_lg_aPER = totnewPERunits / totminutes
for x in range(len(PER)):
	PER[x] = PER[x] * 15 / lg_aPER
	newPER[x] = newPER[x] * 15 / new_lg_aPER
	print guys[x], PER[x], newPER[x]
