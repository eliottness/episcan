from __future__ import annotations
import os
from uuid import uuid4

IMG_EXT = ".png"
IMAGES_DIR = os.path.join("images", '')

def img_file(page_name):
    return IMAGES_DIR + page_name + IMG_EXT

class Lang:
    UnK = -1
    RAW = 0
    VUS = 1
    VF  = 2

class Scrapper:
    pass

class Chapter:
    """
    """

    #Memory optimization
    #__slots__ = ['next', 'prev', 'num', 'lang', 'pages']

    next  : Chapter        #previous chapter, None if empty
    prev  : Chapter        #next chapter, None if empty
    num   : float          #chapter number
    lang  : Lang           #can be RAW, VUS, VF or unknown for now
    pages : list[str]      #str uuid

    def add_page(self, name, page_num):

        if not isinstance(page_num, int):
            raise TypeError(f"The number of the page must be an integer (Given: {page_num})")

        if not isinstance(name, str):
            raise TypeError(f"The temporary image file path must be a string (Given: {name})")

        if not os.path.isfile(name):
            raise FileNotFoundError(f"Cannot file the temporary file {name}")

        if page_num >= len(self.pages):
            raise IndexError("The page number should be either to change a specific \
                                page (e.g. number in [0; len(pages) - 1]), \
                                or -1 to add the page at the end of chapter")

        assert os.path.isdir(IMAGES_DIR), "The directory 'images' cannot be found"
        assert name[:-4] == IMG_EXT, "The image must be a png file"

        id   = uuid.uuid4().hex
        file = img_file(id)
        while not os.path.isfile(file):
            id   = uuid.uuid4().hex
            file = img_file(id)

        os.rename(name, file)

        if page_num == -1:
            self.pages.append(id)
        else:
            if os.path.isfile(img_file(self.pages[page_num])):
                os.remove(img_file(self.pages[page_num]))

            self.pages[page_num] = id

class Manga:
    """
    This class manga is done to contain all the data needed in any form of way
    to power the web server and the scraper
    """

    #Memory optimization
    #__slots__ = ['name', 'chapters', 'lang', 'scraper_data']

    name        : str                  #Manga name
    chapters    : dict[float, Chapter] #chap_number->Chapter object
    lang        : Lang                 #The manga language
    scraper_data: Scrapper             #All the data needed to download chapters

    def find_chapter(self, chap_num):

        if type(chap_num) is not float:
            raise TypeError(f"Chapter index should be a float (Given: {type(chap_num)})")

        if chap_num not in self.chapters:
            raise IndexError(f"The chapter {chap_num} is not in the list of chapters")

        return self.chapters[chap_num]

    def chapters_list(self):
        return list(sorted(self.chapters.keys()))

    def add_chapter(self, chapter, overwrite=False):
        """
        add a chapter to this manga, the chapter instance should already have:
         *  a chapter number
         *  a language
         *  a list of images id, added to it with the method: add_page

        if the overwrite parameter is True, the old chapter images will be deleted
        """

        assert hasattr(chapter, 'num'), "chapter do not have a number"
        assert hasattr(chapter, 'pages'), "Chapter do not have any pages"
        assert hasattr(chapter, 'lang'), "Chapter do not have a lang"
        assert chapter.num >= 0.0, "Chapter number must be in R+"
        assert isinstance(chapter.lang, Lang), "Chapter lang must from the Lang class"

        for page in chapter.pages:
            assert type(page) is str and len(page) == 32, \
            "The pages list must be a list of hexadecimal 4-bytes digest in strings"
            assert os.path.isfile(img_file(page)), \
            f"Did not find any page named {page} in images dir"

        if not overwrite:
            assert chapter.num not in self.chapters, f"There is already a chapter with the number {chapter.num}"
        elif chapter.num in self.chapters:
            new_pages = set(chapter.pages)
            old_pages = set(self.chapters[chapter.num])

            #Only delete old images which are not in the new images
            old_pages = map(img_file, old_pages - new_pages.intersection(old_pages))
            for page in old_pages:
                if os.path.isfile(page):
                    os.remove(page)

            del self.chapters[chapter.num]

        chap_list = self.chapters_list()
        index     = 0

        while index < len(chap_list) and chapter.num > chap_list[index]:
            index += 1

        try:
            chapter.prev = self.chapters[chap_list[index - 1]]
            self.chapters[chap_list[index - 1]].next = chapter
        except IndexError:
            chapter.prev = None

        try:
            chapter.next = self.chapters[chap_list[index]]
            self.chapters[chap_list[index]].prev = chapter
        except IndexError:
            chapter.next = None

        self.chapters[chapter.num] = chapter
