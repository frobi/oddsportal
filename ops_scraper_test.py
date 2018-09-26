#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:34:49 2018

@author:
"""

from oddsportal import scraper

from bs4 import BeautifulSoup
import os
import logging.config
#logging.config.fileConfig('/path/to/logging.conf')
logging.basicConfig(filename=os.path.join(os.getcwd(),'log/ops_test.log'),
                    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S")   
    
c = scraper.Scraper(headless=False)


# TEST go to link http://www.oddsportal.com/handball/ukraine/superleague/results/
c._go_to_link('http://www.oddsportal.com/handball/ukraine/superleague/results/')

html_source = c._get_html_source()
soup = BeautifulSoup(html_source, "html.parser")
table = soup.find("table", id="tournamentTable")
l = c._cells_data_3way(table)
print(l)

c.close_browser()