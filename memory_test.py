import uuid
import json
from memory_profiler import profile
from mangas.manga import * #bad

"""def chapter_init(self, num):
    self.num   = num
    self.lang  = Lang.VF
    self.pages = [uuid.uuid4().hex for i in range(20)]

Chapter.__init__ = chapter_init

def manga_init(self):
    self.name = uuid.uuid4().hex
    self.lang = Lang.VF
    self.scraper_data = Scrapper()

    self.chapters = dict()
    self.chapters[0.0] = Chapter(0.0)
    self.chapters[0.0].prev = None

    for i in map(float, range(1, 1000)):
        self.chapters[i] = Chapter(i)
        self.chapters[i - 1.0].next = self.chapters[i]
        self.chapters[i].prev = self.chapters[i - 1.0]

Manga.__init__ = manga_init"""

@profile
def main():
    m = Manga()
    json.dump(m.to_dict(), open('test.pkl', "w"))

if __name__ == "__main__":
    main()
