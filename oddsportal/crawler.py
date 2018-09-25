#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 10:42:55 2018

"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

# in each module
import logging
logger = logging.getLogger(__name__)


class Crawler(object):
    """
    A class to crawl links from oddsportal.com website.
    Makes use of Selenium and BeautifulSoup modules
    """
    WAIT_TIME = 3  # max waiting time for a page to load
    
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
    
    def set_time_zone(self, timezone="Budapest"):
        self._go_to_link(self.base_url)
        WebDriverWait(self.driver, self.WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user-header-timezone-expander"))).click()
        WebDriverWait(self.driver, self.WAIT_TIME).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, timezone))).click()
        logger.info('timezone set to: %s', timezone)
        
    def _league_seasons(self, league_link):
        '''
        league_link: eg.: http://www.oddsportal.com/handball/austria/hla/results/
        
        Returns a list of links.
        '''
        p_links = []
        
        if not self._go_to_link(league_link):
            return []
        
        html_source = self._get_html_source()
        soup = BeautifulSoup(html_source, "html.parser")
        
        seasons = soup.find("div", class_="main-menu2 main-menu-gray").find_all("span")
        
        season_links = [season.find("a")['href'] for season in seasons]
        
        logger.info('season links in league: %s', season_links)
        
        for link in season_links:
            self._go_to_link(self.base_url + link)
            p_links.append(self._pagination(link))
        
        # flatten the results
        #https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python#952946
        #flat_list = [item for sublist in a_list for item in sublist]
        return [item for sublist in p_links for item in sublist]
    
    def _pagination(self, season_link):
        '''
        Returns the page's pagination of a single season on the Odds Portal website.
        
        eg.: season_link = '/handball/austria/hla-2017-2018/results/' 
        
        Returns a list of links.
        '''
        pagination_links = []
        
        self._go_to_link(self.base_url + season_link)
        html_source = self._get_html_source()
        soup = BeautifulSoup(html_source, "html.parser")
        pagination_tags = soup.find("div", id="pagination")
        
        # no pagination for this link
        if pagination_tags is None:
            pagination_links.append(self.base_url + season_link)
        else:
            pagination_links.append(self.base_url + season_link)
            paginations = [page['href'] for page in pagination_tags.find_all("a")]
            
            for page in paginations:
                if page.find('page') != -1:
                    if (self.base_url + season_link + page) not in pagination_links:
                        pagination_links.append(self.base_url + season_link + page)
                    
        logger.info('pagination links: %s', pagination_links)
        
        return pagination_links

    def leagues(self, sport):
        '''
        returns all leagues in a given sport
        
        sport: soccer, tennis ...
        
        returns a dict: league name is the key and urls are the values
        '''
        league_dict = {}
        link = self.base_url + '/' + sport + '/results'
        self._go_to_link(link)
        html_source = self._get_html_source()
        
        soup = BeautifulSoup(html_source, "html.parser")
        links = soup.find("table", class_="table-main sport").find_all("a",{"foo":"f"})
        for a in links:
            # setdefault - key might exist already
            league_dict.setdefault(a.get_text(strip=True), []).append(self.base_url + a["href"])
        
        logger.info('leagues in sport %s: %s', sport, league_dict)
        
        return league_dict
    
    def league_links(self, league_dict):
        '''
        leage_dict: league name is the key and urls (as a list) are the values
        
        returns a dict: {league_name: [season_links, season2_links, season3_links]}
        '''
        ret_dict = {}
        
        # python dict: https://stackoverflow.com/questions/10458437/what-is-the-difference-between-dict-items-and-dict-iteritems#10458567
        for k,links in league_dict.items():
            for link in links:
                #print('key: {0}\nvalue: {1}'.format(k,v))
                a_list = self._league_seasons(link)
                for a in a_list:
                    ret_dict.setdefault(k, []).append(a)
        
        return ret_dict

    
    def utest(self):
        print(1)
        return 1
    