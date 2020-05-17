from __future__ import annotations
import os
import json

from selenium.webdriver.common.by import By

class DOMElem:

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

    manga:  Manga
    driver: HeadlessChrome


    @classmethod
    def from_dict(cls, value):
        return cls()

    def to_dict(self):
        return None

    @property
    def opened(self):
        return hasattr(self, 'driver')

    def open(self, driver):
        driver._check_open()
        self.driver = driver

    def _check_open(self):
        if not hasattr(self, 'driver'):
            raise ValueError("Chrome Driver is not open, please use HeadlessChrome in a 'with' clause")

    def close(self):
        del self.driver

    def find_chapter_lang(self, num: float = None): #-> enum[Lang]
        """ find the language of the chapter (VF, VUS, RAW...) """
        raise NotImplementedError()

    def find_the_number_of_pages(self): #-> int
        """ find the number of page of this chapter """
        raise NotImplementedError()

    def find_chapters_list(self): #-> list[float]
        """ Find the list of chapter numbers """
        raise NotImplementedError()

    def download_chapter(self, num: float, overwrite=False):
        """ Download a Chapter and add it to the manga data """
        raise NotImplementedError()

    def update_manga(self):
        """ Update the manga with all the chapters"""
        new_list = self.find_chapter_list()
        old_list = self.manga.chap_num_list
        recheck  = self.manga.chap_to_recheck
        diff     = set(new_list) - set(old_list)

        for num in diff:
            self.download_chapter(num)

        for num in recheck:
            old_lang = self.manga.chapters[num].lang
            new_lang = self.find_chapter_lang(num)
            if old_lang != new_lang:
                self.download_chapter(num, overwrite=True)
