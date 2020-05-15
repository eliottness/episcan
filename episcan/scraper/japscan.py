from __future__ import annotations

from .. import manga as mg
from selenium.webdriver.common.by import By
from .base import Scraper, DOMElem

class Japscan:

    base_url = "https://www.japscan.co/"

    ###########################
    ### Key elements
    ###########################

    #only for jascan and scantrad-union
    search_menu   : DOMElem   # Used to access the research bar
    search_elem   : DOMElem   # Search bar of the homepage
    search_val    : str       # Value to enter in the search bar
    search_result : DOMElem   # Click on the first result of the research
    search_chap   : DOMElem   # Search the first chapter of the manga
    search_start  : DOMElem   # Search for the start reading button (only scan manga)


    @classmethod
    def from_dict(cls, value):
        return cls()

    def to_dict(self):
        return None
