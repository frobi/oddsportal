# Oddsportal Scraper

Get results from oddsportal.com in a given sport.

## Crawler Module
Gives back all the league and season links in a given sport.

**Usage**  
ops --sport floorball floorball_leagues.json
ops --sport-links floorball floorball_links.json
ops --links-from-file futsal_leagues.json futsal_links.json

BUGS:

Page Not Found-nál elszáll: nem túl szépen de próbáltam kezelni  
http://www.oddsportal.com/futsal/greece/super-league/results/  
File "/home/rob/projects/python/ops/oddsportal/crawler.py", line 89, in _league_seasons
seasons = soup.find("div", class_="main-menu2 main-menu-gray").find_all("span")
AttributeError: 'NoneType' object has no attribute 'find_all'

