import uuid
from memory_profiler import profile
from episcan.manga import * #bad
from episcan.scraper.japscan import Japscan

def chapter_init(num):
    self = Chapter(num, Lang.VF)
    self.pages = [uuid.uuid4().hex[:LEN_IMG_ID] for i in range(20)]

    return self

def manga_init():
    self = Manga("one-piece.mg", "One Piece", Lang.VF, Japscan("test"), "/images/boruto.jpg")

    self.chapters = dict()
    self.chapters[0.0] = chapter_init(0.0)
    self.chapters[0.0].prev = None

    for i in map(float, range(1, 1000)):
        self.chapters[i] = chapter_init(i)
        self.chapters[i - 1.0].next = self.chapters[i]
        self.chapters[i].prev = self.chapters[i - 1.0]

    return self

@profile
def main():
    m = manga_init()
    m.save_manga()

    import timeit

    def func():
        x = Manga.load_manga("one-piece.mg")
        del x
    #print(timeit.timeit(func, number=2000) / 2000)
    #Do not run the time profiler and the memory profiler

if __name__ == "__main__":
    main()
