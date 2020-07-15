from __future__ import annotations

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from episcan.scraper.base import Scraper
from episcan.scraper.DOMElem import DOMElem

from episcan.lang import Lang

class Japscan(Scraper):

    base_url = "https://www.japscan.co/"

    ###########################
    ### Key elements
    ###########################

    """ Only tests
    #only for jascan
    search_menu   : DOMElem   # Used to access the research bar
    search_elem   : DOMElem   # Search bar of the homepage
    search_val    : str       # Value to enter in the search bar
    search_result : DOMElem   # Click on the first result of the research
    search_chap   : DOMElem   # Search the first chapter of the manga
    search_start  : DOMElem   # Search for the start reading button (only scan manga)
    """
    chapter_list_url : str

    init_args    = ['chapter_list_url', ]
    chapter_list = DOMElem(By.ID, "chapters_list")
    next_page    = DOMElem(By.ID, "image")
    chapter_lang = DOMElem(By.CLASS_NAME, "badge badge-primary")

    #this must also possess an href attribute and be clickable
    chapter_list_elem = DOMElem(By.CLASS_NAME, "text-dark")

    @classmethod
    def from_dict(cls, values):
        return cls(*values[1:])

    def to_dict(self):
        return [self.__class__.__name__, self.chapter_list_url]

    def find_chapter_lang(self, num: float = None): #-> enum[mg.Lang]
        """ find the language of the chapter (VF, VUS, RAW...) """
        self._check_open()
        self.driver.get(self.chapter_list_url)

        try:
            elem = self.driver.find_element_by_class_name(chapter_lang.value)
            self.manga.lang = lang.get_lang()
        except NoSuchElementException:
            self.manga.lang = lang.get_lang(3)


    def find_the_number_of_pages(self): #-> int
        """ find the number of page of this chapter """
        self._check_open()

    def find_chapters_list(self): #-> list[float]
        """ Find the list of chapter numbers """
        self._check_open()
        self.driver.get(self.chapter_list_url)

    def download_chapter(self, num: float, overwrite=False):
        """ Download a Chapter and add it to the manga data """
        self._check_open()
        nb_pages = self.find_the_number_of_pages()
