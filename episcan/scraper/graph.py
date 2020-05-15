from __future__ import annotations
import os
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

class KeyElem:

    ###########################
    ### Key elements
    ###########################
    search_menu      = 0        # Used to access the research bar
    first_search_res = 1        # Click on the first result of the research


    #only for jascan and scantrad-union
    search_menu   : DOMElem   # Used to access the research bar
    search_elem   : DOMElem   # Search bar of the homepage
    search_val    : str       # Value to enter in the search bar
    search_result : DOMElem   # Click on the first result of the research
    search_chap   : DOMElem   # Search the first chapter of the manga
    search_start  : DOMElem   # Search for the start reading button (only scan manga)

class DOMElem:

    by        : By  # Search method to find the particular element
    value     : str # Search value
    send_keys : str # Keys to enter if the value is a field


    def __init__(self, by, val):
        self.by     = by
        self.value  = val

class Pipeline:
    """
    Represent a serie of DOM elements to click/send keys on it
    to a certain purpose

    For us, it represents a link between 2 pages, for instance:
    Pipeline() : homepage -> manga chapters list pages
    This reprensent the tag of the pipeline and the interest we gave to it
    """

    entry : enum[KeyPoint]

    @classmethod
    def from_dict(cls, value):
        return cls()

    def to_dict(self):
        return None

class Scraper:
    """
    The data needed by the scraper process to function

    The idea is to make the user enter the location of severals elements
    on the website, these elements will be the keys to automate the construction of
    different pipelines. These pipeline will form the edges a graph which will be the key data
    of our scraping process.

    (The word graph is a little bit wrong because we can only ask the user for a
    sample version of elements like 'next page' button to support muliple edges
    of our graph so it is more a shrinked graph)

    Once we have these key elements we will try all the possibilities of all key
    elements on differents pages to explore the website, firstly this will form
    a graph of all webpages accessed and after we will delete some useless nodes and
    shrink some nodes on the interesting chains, these chains will be our pipelines.

    This class is destined to be derived to add flexibility to key element types
    and the way they are managed
    """

    @classmethod
    def from_dict(cls, value):
        return cls()

    def to_dict(self):
        return None
