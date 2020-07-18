import os

from __future__ import annotations

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from episcan.scraper.base import Scraper
from episcan.scraper.DOMElem import DOMElem

from episcan.lang import Lang

class Japscan(Scraper):

    base_url = "https://www.japscan.co/lecture-en-ligne/"

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

    #this must also possess an href attribute and be clickable
    chapter_list_elem = DOMElem(By.CLASS_NAME, "text-dark")

    @classmethod
    def from_dict(cls, values):
        return cls(*values[1:])

    def to_dict(self):
        return [self.__class__.__name__, self.chapter_list_url]

    def find_chapter_lang(self, num: float = None): #-> enum[mg.Lang]
        """
        find the language of the chapter (VF, VUS, RAW...)
        """

        lang = None
        self._check_open()
        self.driver.get(self.chapter_list_url)

        try:
            if num % 1 == 0:
                num = int(num)

            elem = self.driver.find_element_by_partial_link_text("{} VF".format(num))

            if elem.text.contain("Raw"):
                lang = lang.get_lang(1)

            else if :
                """ !!! Locate the Vus Badge in the HTML """
                lang = lang.get_lang(2)

            else:
                lang = lang.get_lang(3)

        except:
            lang = lang.get_lang(0)

        self.driver.close()
        return lang

    def find_the_number_of_pages(self, num): #-> int
        """
        find the number of page of this chapter
        """

        self._check_open()
        link = "{}{}/{}/".format(base_url, self.manga.name, num)
        self.driver.get(link)

        elem = self.driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div/p[5]/span")
        nb_pages = int(elem.text[:2])
        """ Might return the 'Number of page:' string instead of the one with the correct number of pages """

        self.driver.close()
        return nb_pages

    def find_chapters_list(self): #-> list[float]
        """
        Find the list of chapter numbers
        """

        self._check_open()
        self.driver.get(self.chapter_list_url)

        chp_list = []
        elems = self.driver.find_elements_by_partial_link_text("VF")

        for elem in elems:

            i  = 0
            nb = ""
            while i < len(elem):

                while (elem[i] >= '1' and elem[i] <= '9') or elem[i] == '.':
                    nb += elem[i]
                    i += 1

                i += 1

            ch_list.append(float(nb))

        self.driver.close()
        return chp_list.sort()

    def download_chapter(self, num: float, overwrite=False):
        """
        Download a Chapter and add it to the manga data
        """

        self._check_open()
        nb_pages = self.find_the_number_of_pages(num)
        chapter  = Chapter(None, None, num, find_chapter_lang(num), [])

        j = 0
        for i in nb_pages:

            try:
                link = "{}{}{}.html".format(base_url, self.manga.name, i)
                self.driver.get(link)

            except:
                break

            images = self.driver.find_elements_by_tag_name('img')

            for image in images:

                image.screenshot("./../../images", "tmp{}.jpg".format(j))
                chapter.add_page("tmp{}.jpg".format(j), j + 1)
                j += 1

        self.manga.add_chapter(chapter, overwrite=True)
        self.driver.close()
