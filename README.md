# NBA Player Value

  This project aimed to improve the formula of a widely used basketball statistic, John Hollinger's widely
used "PER". It involved scraping the play-by-play data for the 2014-15 NBA season from
basketball-reference.com, and using a number of insights that the data provided to adjust PER's formula.
PER's formula is given here: http://www.basketball-reference.com/about/per.html 

  PER attempts to calculate a player's value by assigning weights to each of a player's box score stats,
such as three point attempts, turnovers, and defensive rebounds. The main idea is that there is an
expected number of points a team will score in a possession (a little more than 1 point, on average)
and that each box score statistic can be valued by relating it to that "Value Of Possession" (VOP) 
figure. For example, a steal ends the opposing team's possession with 0 points instead of whatever the 
VOP figure is, so the player who got the steal is credited with the VOP figure (again, a little more than
1 point). PER uses those weights for each statistic, averages them for each player on a per-minute basis,
and then scales the results together such that a league-average player has a PER of 15, while the best
players in the league usually have PERs above 25.

  There are three main improvements my work makes to PER. The first involves the assumptions that
Hollinger had to make to construct his formula because he had to rely solely on box scores for each game.
For example, he had to estimate how many possessions a team had in a game based on its field goal
attempts, free throw attempts, offensive rebounds, and turnovers. For another, he had to estimate what
portion of blocks the defending team rebounds. With play-by-play data available, I was able to replace
each of his assumptions with more accurate values.

  The second involves Hollinger's weights for shooting statistics: free throws, two pointers, and three
pointers made and attempted. PER has been criticized for its handling of these statistics: it implies a
break even shooting percentage of around 30% for two pointers and 21% for threes. These figures are
immediately and intuitively recognizable as far too low by basketball fans and analysts, and they 
overvalue players that take many shots at a low efficiency. I refigure how these weights are
calculated, with break even shooting percentages more in line with common sense.

  The third improvement involves incorporating what happens on the following possession into the weight
I assign each statistic. To see what that means, let's consider the value of a steal. While a steal is
worth the VOP figure for ending the opponent's possession, it also frequently leads to a valuable fast
break opportunity, which has a higher than normal points expectation. In fact teams typically score
around .2 points more on possession immediately following steals. Thus a steal is worth VOP + .2, for
ending the opposing team's possession and for increasing the value of the team's next possession. I
applied similar adjustments to the weight of each statistic.

Work in progress
