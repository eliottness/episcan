from __future__ import annotations
import os
import json

from .. import manga as mg
from selenium.webdriver.common.by import By

class DOMElem:

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


    by        : By  # Search method to find the particular element
    value     : str # Search value
    send_keys : str # Keys to enter if the value is a field

    def __init__(self, by, val):
        self.by         = by
        self.value      = val
        self.send_keys  = None

class Scraper:
    """
    The data needed by the scraper process to function
    """

    manga: mg.Manga

    @classmethod
    def from_dict(cls, value):
        return cls()

    def to_dict(self):
        return None

    def find_chapter_lang(self, num: float = None): -> enum[mg.Lang]
        """ find the language of the chapter (VF, VUS, RAW...) """
        raise NotImplementedError()

    def find_the_number_of_pages(self): -> int
        """ find the number of page of this chapter """
        raise NotImplementedError()

    def find_chapters_list(self): -> list[float]
        """ Find the list of chapter numbers """
        raise NotImplementedError()

    def download_chapter(self, num: float, overwrite=False):
        """ Download a Chapter and add it to the manga data """
        raise NotImplementedError()

    def update_manga(self):
        """ Update the manga with all the chapters"""
        new_list = self.find_chapter_list()
        old_list = self.manga.chap_num_list
        diff     = set(new_list) - set(old_list)

        for num in diff:
            self.download_chapter(num)

        old_recheck  = self.manga.chap_to_recheck
        new_recheck  = [self.find_chapter_lang(x) for x in old_recheck]

        for num, new_lang in zip(old_recheck, new_recheck):
            old_lang = self.manga.chapters[num].lang
            if old_lang != new_lang:
                self.download_chapter(num, ov overwrite=True)
