import sqlite3
import time
import datetime as dt

from episcan.manga import Manga

__doc__ = r'''

CREATE TABLE "manga_list" (
	"filename"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"nb_chap"	INTEGER NOT NULL,
	"last_update"	TEXT NOT NULL,
	"added_date"	TEXT NOT NULL,
	"image_path"	TEXT,
	PRIMARY KEY("filename")
)

'''


class Database:

    def __init__(self, db_file, logger):
        self.db_file = db_file
        self.logger  = logger

    def __query(self, sql, *args):

        conn = sqlite3.connect(self.db_file)

        for _ in range(5):
            try:
                cr = conn.cursor()
                cr.execute(sql, args)
            except sqlite3.OperationalError:
                cr.close()
                conn.rollback()
                self.logger.warning("Rollback on database {}".format(self.db_file))
                continue
            except sqlite3.DatabaseError as e:
                self.logger.error(f"Database ERROR: {repr(e)}")
                raise e
            else:
                break

        res = cr.fetchall()

        cr.close()
        conn.commit()
        conn.close()

        return res

    def get_all_mangas(self):
        """
        format all the table manga_list into a list of dict
        """
        lines = self.__query("SELECT * FROM manga_list")

        return [{
            "filename": line[0],
            "name": line[1],
            "nb_chap": line[2],
            "last_update": line[3],
            "added_date": line[4],
            "image_path": line[5] #thumbnail
        } for line in lines]

    def get_mangas_list(self):
        """
        get all the manga filenames in the db
        """

        lines = self.__query("SELECT filename FROM manga_list")
        return [line[0] for line in lines]

    def update_manga(self, manga):
        """
        arg: a manga object
        """
        now = dt.datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        sql = "UPDATE manga_list SET last_update = %s, nb_chap = %d WHERE filename = %s"

        self.__query(sql, (now, manga.nb_chap, manga.filename))

    def add_manga(self, manga):
        """
        arg1: a manga object
        """
        now = dt.datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        sql = "INSERT INTO manga_list VALUES (%s, %s, %d, %s, %s, %s)"

        try:
            self.__query(sql, (manga.filename, manga.name, manga.nb_chap, now, now, manga.image_path))
        except sqlite3.IntegrityError as e:
            self.logger.error(f"The Manga {manga.filename} is already in the database")
        else:
            self.logger.warning(f"Added manga named {manga.filename} to the database")

    def health_check(self):

        self.logger.info("Running simple health check between database and saved mangas...")

        db_mangas = self.get_all_mangas()

        for manga in Manga.iter_all_mangas(self.logger):

            db_manga = next(filter(lambda mg: mg["filename"] == manga.filename, db_mangas), None)

            if not db_manga:
                self.logger.warning(f"{manga.filename} is not in the database, adding it")
                self.add_manga(manga)
                continue

            nb_chap    = db_manga["nb_chap"]    == manga.nb_chap
            image_path = db_manga["image_path"] == manga.image_path

            if not nb_chap or not image_path:
                self.logger.error("Reconciliate DB and manga file: {manga.filename}")

                sql = "UPDATE manga_list SET nb_chap = %d, image_path = %s WHERE filename = %s"

                self.__query(sql, (manga.nb_chap, manga.image_path, manga.filename))

        self.logger.info("Health check ended")
