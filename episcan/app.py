import logging
import json

from flask import Flask, render_template, url_for, send_from_directory
from flask import request, redirect, abort, jsonify
from flask_caching import Cache

from episcan import lang, manga
from episcan.database import Database
from episcan.scraper  import main as scraper_main

DEBUG       = False
DEBUG2      = True
CONFIG_FILE = "app_config.json"

SCRAPER_CACHE_KEY = "scraper_thread_list"

###################################
### INIT
###################################

with open(CONFIG_FILE, 'r') as fh:
    config = json.load(fh)

app = Flask("episcan")
app.config["DEBUG"] = DEBUG
app.config.from_mapping(config["flask_config"])
cache    = Cache(app)
database = Database(config["sqlite_db"], app.logger)

def init():
    cache.set(SCRAPER_CACHE_KEY, list())

    if not DEBUG2:
        database.health_check()

###################################
### Backend bindings
###################################

def update_manga(manga):
    """
    argument: a manga filename
    """

    old_thrs = cache.get(SCRAPER_CACHE_KEY)
    thrs     = dict()

    for mg, thr in old_thrs.items():
        if thr.is_alive():
            new_thrs[mg] = thr
        else:
            del old_thrs[mg]

    if not thrs.get(manga):
        thr = scraper_main.Scraper_Deamon(manga)
        thr.start()
        thrs[manga] = thr
        app.logger.info(f"Started to update {manga}")
    else:
        app.logger.warning(f"{manga} is already updating, wait for update to end")

    cache.set(SCRAPER_CACHE_KEY, thrs)

@cache.memoize()
def find_manga(manga):
    """
    Argument: the manga filename
    returns:  The object of a class Manga corresponding
    """
    return manga.Manga.load_manga(manga)

def get_reading_data(manga, chapter):
    """
    Argument: manga filename, chapter number (float)
    """

    if DEBUG:
        return {
            "manga_title": "Boruto",
            "chapter_num": "1",
            "manga_home_url": "/manga_home_url",
            "chapters_url_list": [(1.0, "/chapters_url_list1"), (3.0, "/chapters_url_list3")],
            "prev_chap_url": "/prev_chap_url",
            "next_chap_url": "/next_chap_url",
            "image_url": "/images/1.jpg",
            "chapter_nb_pages": 2,
            "images_route": config["images_route"],
            "images_id": ["1.jpg", "2.jpg"]
        }

    manga   = find_manga(manga)
    chapter = manga.find_chapter(chapter)

    if chapter.prev:
        prev_url = url_for('reading', manga.filename, chapter.prev.num)
    else:
        prev_url = None

    if chapter.next:
        next_url = url_for('reading', manga.filename, chapter.next.num)
    else:
        next_url = None

    return {
        "manga_title": manga.name,
        "chapter_num": chapter.num,
        "manga_home_url": url_for('manga_home', manga.filename),
        "chapters_url_list": sorted(manga.chapters), # return sorted keys
        "prev_chap_url": prev_url,
        "next_chap_url": next_urm,
        "image_url": url_for('image', chapter.pages[0]),
        "chapter_nb_pages": chapter.nb_pages,
        "images_route": config["images_route"],
        "images_id": chapter.pages
    }

@cache.memoize()
def get_mangas_list():

    if DEBUG:
        return {"list": [
            {
                "name": "Boruto",
                "image_path": url_for('images', "boruto.jpg"),
                "url": url_for('manga_home', "boruto")
            }
        ]}


    return {"list":[
        {
            "name": manga["name"],
            "image_path": url_for('images', manga["image_path"]),
            "url":  url_for('manga_home', manga["filename"])
        } for manga in database.get_all_mangas()
    ]}

@cache.memoize()
def get_manga_home(manga):
    """
    """

    if DEBUG:
        return {
            "name":"Boruto",
            "chapters_list": []
        }

    return {}

    raise NotImplementedError()

def get_home_feed():

    return dict()

    raise NotImplementedError()

###################################
### Context processors
###################################

@app.context_processor
def lang(lg):
    return lang.Lang.to_str[lg]

###################################
### Routes
###################################

@app.route('/lecture/<string:manga>/<float:chapter>')
def reading(manga, chapter):
    data = get_reading_data(manga, chapter)
    if DEBUG2: return jsonify(data)
    return render_template("lecture.html", **data)

@app.route('/mangas_list')
def mangas_list():
    data = get_mangas_list()
    if DEBUG2: return jsonify(data)
    return render_template('mangas.html', **data)

@app.route('/manga/<string:manga_name>')
def manga_home(manga):
    data = get_manga_home(manga)
    if DEBUG2: return jsonify(data)
    return render_template("chapters.html", **data)

@app.route('/')
@cache.cached()
def home():
    data = get_home_feed()
    if DEBUG2: return jsonify(data)
    return render_template('homepage.html', **data)

@app.route('{}<img_file>'.format(config["images_route"]))
def image(img_file):
    return send_from_directory(config["images_path"], img_file, mimetype="image/jpg")

@app.route('/update', methods=['POST'])
def update(manga):
    if "manga" not in request.args:
        abort(404)

    manga_name = request.args["manga"]

    if manga_name not in database.get_mangas_list():
        abort(404)

    update_manga(manga_name)

def main():
    init()
    app.run(debug=True)

if __name__ == "__main__":
    main()
