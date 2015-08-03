from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import timedelta, date

BASE_URL = "http://www.basketball-reference.com"

def get_daily_boxscore_links(day_url):
	html = urlopen(day_url).read()
	soup = BeautifulSoup(html, "lxml")
	if soup.find("a", text="Play-By-Play") == None:
		return []
	medium_text = soup.find("table", "medium_text")
	boxscore_links = [BASE_URL + a["href"] for a in medium_text.find_all("a", text="Play-By-Play")]
	return boxscore_links

start_date = date(2014, 10, 28)
end_date = date(2015, 4, 15)
delta = timedelta(days=1)
d = start_date
yearly_pbp_links = []
while d <= end_date:
	daily_links = get_daily_boxscore_links("http://www.basketball-reference.com/boxscores/index.cgi?month=" + str(d.month) + "&day=" + str(d.day) + "&year=" + str(d.year))
	for x in daily_links:
		yearly_pbp_links.append(x)
	d += delta

f = open('2014to2015.txt', 'w')
for x in yearly_pbp_links:
	f.write(str(x) + "\n")
