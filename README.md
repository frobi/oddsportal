# Oddsportal Scraper

Get results from oddsportal.com in a given sport.


## Crawler Module
Gives back all the league and season links in a given sport.

## Scraper Modue
Scraper/parser to ge the results from oddsportal.com. Currently can scrape results only for 3 way sports (soccer, handball, ...)
Exports data into sqlite3 db.
Create sqlite3 db before use in /data folder.

## Usage

    -h, --help            show this help message and exit
    --tz                  set the Time Zone
    --sport SPORT [OUTPUT_FILE ...]
                        returns all leagues in a given sport. 
                        additional argument save the file to json, if omitted prints to console 
                        e.g.: --sport handball output.json
    --sport-links SPORT_TYPE OUTPUT_FILE
                        returns all the links in a given sport. 
                        additional argument save the file to json 
                        e.g.: --sport-links handball output.json
    --links-from-file INPUT_FILE OUTPUT_FILE
                        returns all the links for specified leagues 
                        e.g.: --links-from-file input.json output.json
    --scrape INPUT_FILE DATABASE_NAME TABLE_NAME
                        get all the results and export it into a sql3 db 
                        args: input.json database table_name 
                        e.g.: --scrape input.json bets.db3 soccer

Get all the leagues/tournaments in a given sport and save the result to json
- *ops --sport floorball floorball_leagues.json*

Get all (season/pagination) links for all leagues/tournaments in a given sport and save the result to json
- *ops --sport-links floorball floorball_links.json*

Get all links for specified leagues
 - *ops --links-from-file edited_floorball_leagues.json floorball_links_e.json*

After we have the necessary links we can download the results and save them into an sqlite3 database. First, we have to create a sqlite3 database in */data* folder. The last parameter is a table name. If that table doesn't exists in database, than it will be created.

- *ops --scrape floorball_links.json bets.db3 floorball*

original source code: https://github.com/DMPierre/oddsPortalScraper/blob/master/OddsParser.py

## BUG
2019-09-29 - there is some memory issue. The Webdrivercontent size can grow fast and can be very huge (5GB+)

