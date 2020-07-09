import threading

from episcan import manga, lang, database
from episcan.scraper import headless
from episcan.scraper import scraper_classes

class Scraper_Deamon(threading.Thread):
    """
    Argument: manga filename

    This should be used as a detached thread to run selenium
    to update our data on the manga <manga>
    """
    def __init__(self, manga):
        threading.Thread.__init__(self)
        self.manga_filename = manga

    def run(self):
        manga = manga.Manga.load_manga(self.manga_filename)

        manga.update_manga()
        manga.save_manga()

        database.update_manga(manga)
