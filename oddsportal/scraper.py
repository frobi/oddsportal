#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 15:01:08 2018

@author:
"""

from bs4 import BeautifulSoup

# in each module
import logging
logger = logging.getLogger(__name__)

class Scraper(object):
    """
    A class to scrape/parse match results from oddsportal.com
    """
