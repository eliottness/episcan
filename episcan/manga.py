from __future__ import annotations
import os
import json
from uuid import uuid4
from episcan.scraper import scraper_classes
from episcan.lang import Lang

LEN_IMG_ID = 16
IMG_EXT    = ".png"
IMAGES_DIR = os.path.join("images", '') #makes either 'images/' or 'images\'
MANGAS_DIR = os.path.join("mangas", '')

def img_file(page_name):
    return IMAGES_DIR + page_name + IMG_EXT

class Chapter:
    """
    """

    #Memory optimization
    __slots__ = ['next', 'prev', 'num', 'lang', 'pages']

    next  : Chapter        #previous chapter, None if empty
    prev  : Chapter        #next chapter, None if empty
    num   : float          #chapter number
    lang  : enum[Lang]     #can be RAW, VUS, VF or unknown for now
    pages : list[str]      #str uuid

    @classmethod
    def from_dict(cls, value):
        c       = cls(value[0], value[1])
        c.pages = value[2]

        return c

    def to_dict(self):
        return [self.num, self.lang, self.pages]

    def __init__(self, num, lang):
        """
        Constructor of the Chapter class:
        :param num  -> float: chapter number
        :param lang -> int | Lang: language of the chapter
        """
        self.num   = num
        self.pages = list()
        self.lang  = Lang.get_lang(lang)

    @property
    def nb_pages(self):
        return len(self.pages)

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

        assert name[-4:] == IMG_EXT, f"The image must be a {IMG_EXT} file"

        id   = uuid4().hex[:LEN_IMG_ID]
        file = img_file(id)
        while not os.path.isfile(file):
            id   = uuid4().hex[:LEN_IMG_ID]
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
    __slots__ = ['image_path', 'filename', 'name', 'chapters', 'lang', 'scraper_data']

    image_path  : str                  # Path to the thumbnail of the manga
    filename    : str                  #Manga name adapted to filenames
    name        : str                  #Manga name
    chapters    : dict[float, Chapter] #chap_number->Chapter object
    lang        : enum[Lang]           #The manga language
    scraper_data: graph.Scraper        #All the data needed to download chapters

    @staticmethod
    def load_manga(filename):
        with open(MANGAS_DIR + filename, 'r') as fh:
            return Manga.from_dict(filename, json.load(fh))

    @classmethod
    def from_dict(cls, filename, value):
        m = cls(filename, value[0], value[1], scraper_classes[value[2][0]].from_dict(value[2]), self.image_path)

        for k, v in value[3].items():
            m.chapters[float(k)] = Chapter.from_dict(v)

        chap_list = m.chap_num_list

        m.chapters[chap_list[0]].prev  = None
        m.chapters[chap_list[-1]].next = None

        for i in range(1, len(chap_list)):
            m.chapters[chap_list[0]].next  = m.chapters[chap_list[-1]]
            m.chapters[chap_list[-1]].prev = m.chapters[chap_list[0]]

        return m

    def save_manga(self, filename=None):
        filename = filename if filename else self.filename
        with open(MANGAS_DIR + filename, 'w') as fh:
            json.dump(self.to_dict(), fh)

    def to_dict(self):
        chapters = dict()

        for k, v in self.chapters.items():
            chapters[k] = v.to_dict()

        return [self.name, self.lang, self.scraper_data.to_dict(), chapters, self.image_path]

    def __init__(self, filename, name, lang, scraper_data, img_path):

        self.image_path = img_path
        self.filename = filename
        self.name     = name
        self.lang     = Lang.get_lang(lang)

        self.scraper_data = scraper_data
        self.chapters     = dict()

    def update(self):
        self.scraper_data.update_manga()

    def find_chapter(self, chap_num):

        if type(chap_num) is not float:
            raise TypeError(f"Chapter index should be a float (Given: {type(chap_num)})")

        if chap_num not in self.chapters:
            raise IndexError(f"The chapter {chap_num} is not in the list of chapters")

        return self.chapters[chap_num]

    @property
    def nb_chap:
        return len(self.chapters)

    @property
    def chap_num_list(self):
        """Sorted list of chapter numbers"""
        return list(sorted(self.chapters.keys()))

    @property
    def chap_to_recheck(self):
        """
        return all the chapter which are in the wrong lang to re_download
        if the lang has changed
        """
        return list(sorted(filter(
                    lambda x: self.chapters[x].lang != self.lang,
                    self.chapters.keys()
                )))

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
            assert type(page) is str and len(page) == LEN_IMG_ID, \
            f"The pages list must be a list of hexadecimal digest in strings of len {LEN_IMG_ID}"
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

        chap_list = self.chap_num_list
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
