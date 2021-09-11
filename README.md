# NFL Top 100

Since 2010, the NFL network has released a show ranking the "Top 100 Players in the NFL" voted by the players. 

Using the Rankings of the last 10 years, what kind of things can we uncover?

* Can the top 10/15/20 players of the 2020 season be predicted based on historical data?
* What team has had the best players of the past 10 years?
* What players have been the most consistent?

Ranking data and player statistics was scraped through the Beautiful Soup library


Some changes that I made:
- Left off Full Backs from offensive playmakers as it makes up only 0.3% of the rankings and it's a slowly fading position
- Changed St. Louis, San Diego, Oakland to their new respective team-location abbreviations (as well as the Washington Football Team)


My prediciton of top 10 (in no particular order):
* Aaron Rodgers
* Josh Allen
* Aaron Donald
* Patrick Mahomes
* Tom Brady
* TJ Watt
* Travis Kelce
* Derrick Henry
* Davante Adams
* Myles Garret

Model prediction of top 10 players (in no particular order):
* Derrick Henry *
* Aaron Rodgers *
* Tom Brady *
* Patrick Mahomes *
* Josh Allen *
* Russel Wilson *
* Davante Adams
* Dalvin Cook
* TJ Watt
* Travis Kelce

"*" indicates predicted top 10, players with no asterisk were predicted top 15

The Model was able to predict the top 10 players of this past year with 80% accuracy. It missed on (Aaron Donald and Deandre Hopkins)

#### Exploratory Analysis.ipynb is where the historical data was analyized to see past trends and determine which playes have historically been ranked the best
#### Predictive Analysis.ipynb is where PyCaret and SciKit Learn were used to predict where the top players of this season would land on the players list
#### The files under scapers are the web-scraping files used to gather past rankings and statistics of players
#### The data collected is under the Data folder


