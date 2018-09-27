# Oddsportal Scraper

Get results from oddsportal.com in a given sport.

## Crawler Module
Gives back all the league and season links in a given sport.

## Scraper Modue
Scraper/parser to ge the results from oddsportal.com. Currently can scrape only 3 way sports data (soccer, handball, ...)
Exports data into sqlite3 db.
Create sqlite3 db before use in /data folder.

**Usage**
Get all the leagues/tournaments in a given sport and save the result to json
- *ops --sport floorball floorball_leagues.json*

Get all (season/pagination) links for all leagues/tournaments in a given sport and save the result to json
- *ops --sport-links floorball floorball_links.json*

Get all links for specified leagues
 - *ops --links-from-file edited_floorball_leagues.json futsal_links.json*

After we have the necessary links we can download the results and save them into an sqlite3 database. First, we have to create a sqlite3 database in /data folder.





BUGS:
Page Not Found-nál elszáll:  
http://www.oddsportal.com/futsal/greece/super-league/results/  
File "/home/rob/projects/python/ops/oddsportal/crawler.py", line 89, in _league_seasons
seasons = soup.find("div", class_="main-menu2 main-menu-gray").find_all("span")
AttributeError: 'NoneType' object has no attribute 'find_all'

TEST on a new branch:  
https://stackoverflow.com/questions/18371741/git-branching-strategy-integated-with-testing-qa-process#18899910

https://stackoverflow.com/questions/24806469/add-the-file-on-the-specific-branch-in-git

https://nvie.com/posts/a-successful-git-branching-model/

show git branch
https://stackoverflow.com/questions/1838873/visualizing-branch-topology-in-git/34467298#34467298
