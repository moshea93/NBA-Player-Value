#ASSUMES TECHNICAL FOUL IMMEDIATELY AFTER JUMP BALL IS ON DEFENSE, ASSUMES AWAY FROM PLAY FOULS ON DEFENSE, SUBSTITUTIONS DURING AND 1'S NEED FIXING
from bs4 import BeautifulSoup
from urllib2 import urlopen

def get_soup(pbp_url):
	html = urlopen(pbp_url).read()
	soup = BeautifulSoup(html, 'lxml')
	return soup

#team abbreviations
def get_teams(soup):
	boxscore = soup.find('table', 'nav_table stats_table')
	teams = [a.text for a in boxscore.find_all('a')]
	awayteam = teams[0]
	hometeam = teams[1]
	return (awayteam, hometeam)

#time during each play
def get_times(log):
	times = [td.text for td in log.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['align_right'])]
	return times

#score during each play
def get_scores(log):
	scores = [td.string for td in log.find_all('td', attrs={'class': 'align_center', 'colspan': None})]
	return scores

#each play
def get_plays(log):
	plays = [td.text for td in log.find_all(lambda tag: tag.name == 'td' and (tag.get('colspan') == '5' or tag.get('class') == ['background_lime'] or tag.get('class') == ['background_white']))]
	return plays

#which team has possession
def get_possession(log, plays, awayteam, hometeam):

	#tipoff winner
	first_pos = log.contents[9]
	if first_pos.contents[3].has_attr('class'):
		tipwinner = awayteam
		tiploser = hometeam
	else:
		tipwinner = hometeam
		tiploser = awayteam

	#column that has play, good proxy for which team has possession
	pos = ['[N/A]', '[N/A]', '[' + tipwinner + ']']
	for sibling in first_pos.next_siblings:
		if len(sibling) > 1 and sibling.contents[1].has_attr('class'):
			if sibling.contents[3].has_attr('colspan'):
				pos.append('[N/A]')
			elif sibling.contents[3].has_attr('class'):	
					pos.append('[' + awayteam + ']')
			else:
					pos.append('[' + hometeam + ']')

	#plays that change NEXT play's possession
	possessionenders = ['makes 2', 'makes 3', 'makes free throw 1 of 1', 'makes free throw 2 of 2', 'makes free throw 3 of 3', 'Turnover', 'Offensive foul']
	#plays where basketball-reference and possession mismatch
	mismatches = ['Personal foul', 'Shooting block foul', 'Loose ball foul', 'Personal take foul', 'Def 3 sec tech foul', 'Violation', 'Away from play foul', 'Inbound foul', 'Clear path foul', 'Personal block foul',]
	#plays where they MIGHT mismatch
	might_mismatch = ['timeout', 'enters the game', 'Technical foul']
	for x in range(len(pos)):
		for y in mismatches:
			if y in plays[x] and 'Violation by Team' not in plays[x]:
				pos[x] = switch_pos(pos[x], hometeam, awayteam)
		for z in might_mismatch:
			if z in plays[x]:
				#assigning possession when there was no previous play
				if pos[x-1] == '[N/A]':
					if plays[x-1] == 'Start of 2nd quarter' or plays[x-1] == 'Start of 3rd quarter':
						pos[x] = '[' + tiploser + ']'
					elif plays[x-1] == 'Start of 4th quarter':
						pos[x] = '[' + tipwinner + ']'
					elif z == 'Technical foul':
						pos[x] = switch_pos(pos[x], hometeam, awayteam)
				else:
					for pe in possessionenders:
						if pe in plays[x-1]:
							pos[x] = switch_pos(pos[x-1], hometeam, awayteam)
							break
					else:
						pos[x] = pos[x-1]

	return pos

#switch possession for given play
def switch_pos(orig, hometeam, awayteam):
	if orig == '[' + hometeam + ']':
		return '[' + awayteam + ']'
	else:
		return '[' + hometeam + ']'

#data for each game
def create_pbp_file(url):
	soup = get_soup(url)
	awayteam, hometeam = get_teams(soup)
	pbp_log = soup.find('table', 'no_highlight stats_table')

	times = get_times(pbp_log)
	plays = get_plays(pbp_log)
	possession = get_possession(pbp_log, plays, awayteam, hometeam)
	scores = get_scores(pbp_log)

	#dates
	date = url[50:58]
	datelist = [date] * len(times)

	#team names to go with 'scores' (e.g. '77-74' --> 'ORL 77-74 BRK')
	awaylist = [awayteam] * len(times)
	homelist = [hometeam] * len(times)

	gamebreaks = ['Jump ball', 'End of 1st quarter', 'Start of 2nd quarter', 'End of 2nd quarter', 'Start of 3rd quarter', 'End of 3rd quarter', 'Start of 4th quarter', 'End of 4th quarter', 'overtime']
	#filling in scores during gamebreaks
	scores.insert(0, '0-0')
	#keeping track of quarter
	qtr = []
	a = 0
	for x in range(len(times)):
		#filling in scores
		for y in gamebreaks:
			if y in plays[x]:
				scores.insert(x, scores[x-1])
		#quarter stuff
		if 'Start of' in plays[x]:
			a += 1
		qtr.append(a)
		#cosmetics
		if len(scores[x]) < 7:
			scores[x] = scores[x] + (' ' * (7 - len(scores[x])))
		if len(times[x]) < 7:
			times[x] = times[x] + ' '

	data = zip(datelist, awaylist, scores, homelist, qtr, times, possession, plays)

#	for a, b, c, d, e, f, g, h in data:
#		print a, b, c, d, e, f, g, h

	return data

x = open('2014to2015.txt', 'r')
y = open('WholeSeason.txt', 'w')
for i, line in enumerate(x):
	data = create_pbp_file(line)
	for a, b, c, d, e, f, g, h in data:
		y.write(a + '   ' + b + ' ' + c + ' ' + d + '   ' + str(e) + ' ' + f + '   ' + g + ' ' + h + '\n')
