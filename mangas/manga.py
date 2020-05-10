import os
import uuid

EXTENTION_IMAGE = ".png"

class Lang:
    RAW = 0
    VUS = 1
    VF  = 2

class Scrapper:
    pass

class Chapter:
    self.next  : Chapter
    self.prev  : Chapter
    self.num   : float
    self.lang  : Lang
    self.pages : list[str] #str uuid

    def add_page(name, page_num):

        if not isinstance(page_num, int):
            raise TypeError(f"The number of the page must be an integer (Given: {page_num})")

        if not isinstance(name, str):
            raise TypeError(f"The temporary image file path must be a string (Given: {name})")

        if not os.path.isfile(name):
            raise FileNotFoundError(f"Cannot file the temporary file {name}")

        assert os.path.isdir("images"), "The directory 'images' cannot be found"

        id = uuid.uuid4().hex + EXTENTION_IMAGE
        while not os.path.isfile(os.path.join("images", id)):
            id = uuid.uuid4().hex + EXTENTION_IMAGE

        os.rename(name, os.path.join("images", id))
        self.pages.insert(id, page_num)


class Manga:
    """

    """
    self.name        : str
    self.chapters    : dict[float, Chapter]
    self.lang        : Lang
    self.scraper_data: Scrapper

    def find_chapter(chap_num):

        if chap_num not in self.chapters:
            raise IndexError(f"The chapter {chap_num} is not in the list of chapters")

        return self.chapters[chap_num]
