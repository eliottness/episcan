import sqlite3
import time
import datetime as dt

__doc__ = r'''

CREATE TABLE "manga_list" (
	"manga_name"	TEXT NOT NULL,
	"nb_chap"	INTEGER NOT NULL,
	"last_update"	TEXT NOT NULL,
	"added_date"	TEXT NOT NULL,
	"image_path"	TEXT,
	PRIMARY KEY("manga_name")
);

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
                time.sleep(1)
                continue
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
            "manga_name": line[0],
            "nb_chap": line[1],
            "last_update": line[2],
            "added_date": line[3],
            "image_path": line[4] #thumbnail
        } for line in lines]

    def get_mangas_list(self):
        """
        get all the manga filenames in the db
        """

        lines = self.__query("SELECT manga_name FROM manga_list")
        return [line[0] for line in lines]

    def update_manga(self, manga):
        """
        arg: a manga object
        """
        now = dt.datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        sql = "UPDATE manga_list SET last_update = %s WHERE manga_name = %s"

        self.__query(sql, (now, manga.filename))

    def add_manga(self, manga):
        """
        arg1: a manga object
        """
        now = dt.datetime.now()
        now = now.strftime("%d/%m/%Y %H:%M:%S")
        sql = "INSERT INTO manga_list VALUES (%s, %d, %s, %s, %s)"

        self.__query(sql, (manga.filename, manga.nb_chap, now, now, manga.image_path))

    def integrity_check(self):

        mangas = self.get_mangas_list()

        

        pass
