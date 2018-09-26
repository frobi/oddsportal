#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 15:01:08 2018

@author:
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re
import datetime

# in each module
import logging
logger = logging.getLogger(__name__)

# https://code.activestate.com/recipes/52308/
class CellData(object):
    """
    strucutre for cell data
    """
    def __init__(self, **kwds):
        #dict.__init__(self,kwds)
        self.__dict__.update(kwds)


class Scraper(object):
    """
    A class to scrape/parse match results from oddsportal.com
    """
    
    def __init__(self, headless=True, browser='firefox'):
        """
        Constructor providing the executable path value to None
        for now only firefox
        for Firefox headless gecko driver required
        """
        self.base_url = 'http://www.oddsportal.com'
        
        if browser == 'firefox':
            if headless:
                self.option = webdriver.firefox.options.Options()
                self.option.add_argument('-headless')
                self.driver = webdriver.Firefox(firefox_options=self.option)
                logger.info('browser opened in headless mode')
            else:
                self.driver = webdriver.Firefox()
                logger.info('browser opened')
        
        # exception when no driver created
        
    def _go_to_link(self,link):
        '''
        returns True if no error
        False whe page not found
        '''
        # load the page fully
        self.driver.get(link)
        try:
            # if no Login button -> page not found
            self.driver.find_element_by_css_selector('.button-dark')
        except NoSuchElementException:
            logger.warning('problem with link: %s', link)
            return False
        
        return True
        
    def _get_html_source(self):
        return self.driver.page_source
    
    def close_browser(self):
        self.driver.quit()
        logger.info('browser closed')
    
    def _convert_date(self, date):
        '''
        returns the date in a from yyyy-mm-dd
        
        input:
            Today, 26 Sep
            Yesterday, 25 Sep
            19 Sep 2018
        '''
        now = datetime.datetime.now()
        m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        n = ['0'+str(i) if i<10 else str(i) for i in range(1,13)]
        months = dict(zip(m,n))
        l = date.split()
        retval = None
        
        if 'Today,' in l:
            retval = None
        elif 'Yesterday,' in l:
            retval = '{}-{}-{}'.format(now.year, months[l[-1]], l[1])
        else:
            retval = '{}-{}-{}'.format(l[-1], months[l[1]], l[0])
            
        return retval
    
    def _cells_data_3way(self, table):
        '''
        returns the match's details in a list of struct [CellData1, CellData2, ...]
        for 3 way sports like soccer, handball ...
        '''
        cells = []
        
        isEmpty = table.find("td", id="emptyMsg")
        if not isEmpty:
            for tr in table.find_all("tr"):
                cell = CellData(url=None, date=None, hour=None, teams=None, score=None, 
                                odds_home=None, odds_draw=None, odds_away=None, result=None)
                
                for span in tr.find_all("span",class_=re.compile('datet')):
                    # convert it to yyyy-mm-dd form
                    md = self._convert_date(span.get_text())
                    
                valid_match = False
                for num, td in enumerate(tr.find_all("td")):
                    if num == 0 and td.get_text() != u'':
                        cell.hour = td.get_text()   # Match hours
                        cell.date = md # Match date
                    elif num == 1 and td.get_text() != u'': 
                        cell.teams = td.get_text()  # Teams or Players
                        # TODO maybe split home away here
                        if 'inplay' in td.a['href']:
                            cell.url = None
                        else:
                            cell.url = td.a['href'] # Links to the match details
                    elif num == 2 and td.get_text() != u'':
                        cell.score = td.get_text()  # Score
                    elif num == 3 and td.get_text() != u'':
                        cell.odds_home = td.get_text()  # Average odd for team 1
                        if 'result-ok' in td.get('class') and not valid_match:
                            cell.result = 1 # Team 1 is the winner
                            valid_match = True
                    elif num == 4 and td.get_text() != u'':
                        cell.odds_draw = td.get_text()  # Average odd for draw
                        if 'result-ok' in td.get('class') and not valid_match:
                            cell.result = 0 # Tie
                            valid_match = True
                    elif num == 5 and td.get_text() != u'': 
                        cell.odds_away = td.get_text()  # Average odd for team 2
                        if 'result-ok' in td.get('class') and not valid_match:
                            cell.result = 2
                            valid_match = True
                    elif num == 6 and td.get_text() != u'':
                        #odd_tot.append(td.get_text())  # Number of bookies
                        # if there is no result (match may be cancelled)
                        if not valid_match:
                            cell.result = -1
                
                if cell.hour is not None:
                    print('{} {} {} {} {} {}'.format(cell.hour, cell.url, cell.score, cell.date, cell.teams, cell.result))
                    cells.append(cell)

            return cells

    def get_data(self, links):
        '''
        input is a list of links
        returns a list of links
        '''
        
        html_source = self._get_html_source()
        soup = BeautifulSoup(html_source, "html.parser")
        # get the table which contains the results 
        table = soup.find("table", id="tournamentTable")
        
        # call cells_data(table)
        