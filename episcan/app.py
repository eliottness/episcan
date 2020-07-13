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

def update_all():
    pass

def update_manga(mg_file):
    """
    argument: a manga filename
    """

    return

    old_thrs = cache.get(SCRAPER_CACHE_KEY)
    thrs     = dict()

    for mg, thr in old_thrs.items():
        if thr.is_alive():
            new_thrs[mg] = thr
        else:
            del old_thrs[mg]

    if not thrs.get(mg_file):
        thr = scraper_main.Scraper_Deamon(mg_file)
        thr.start()
        thrs[mg_file] = thr
        app.logger.info(f"Started to update {mg_file}")
    else:
        app.logger.warning(f"{mg_file} is already updating, wait for update to end")

    cache.set(SCRAPER_CACHE_KEY, thrs)

@cache.memoize()
def find_manga(mg_file):
    """
    Argument: the manga filename
    returns:  The object of a class Manga corresponding
    """

    if mg_file not in db_mangas_list():
        abort(404)

    return manga.Manga.load_manga(mg_file)

def get_reading_data(mg_file, chapter):
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

    mg      = find_manga(mg_file)
    chapter = mg.find_chapter(chapter)

    if chapter.prev:
        prev_url = url_for('reading', mg=mg.filename, chapter=chapter.prev.num)
    else:
        prev_url = None

    if chapter.next:
        next_url = url_for('reading', mg=mg.filename, chapter=chapter.next.num)
    else:
        next_url = None

    return {
        "manga_title": mg.name,
        "chapter_num": chapter.num,
        "manga_home_url": url_for('manga_home', mg=mg.filename),
        "chapters_url_list": sorted(mg.chapters), # return sorted keys
        "prev_chap_url": prev_url,
        "next_chap_url": next_url,
        "image_url": url_for('images', img_file=chapter.pages[0]),
        "chapter_nb_pages": chapter.nb_pages,
        "images_route": config["images_route"],
        "images_id": chapter.pages
    }

@cache.cached(key_prefix="db_mangas_list")
def db_mangas_list():
    return database.get_mangas_list()

def filter_mangas(data, query):
    #TODO
    return data

@cache.memoize()
def get_mangas_list():

    if DEBUG:
        return {"list": [
            {
                "name": "Boruto",
                "image_path": url_for('images', img_file="boruto.jpg"),
                "url": url_for('manga_home', mg="boruto")
            }
        ]}


    return {"list":[
        {
            "name": mg["name"],
            "image_path": url_for('images', img_file=mg["image_path"]),
            "url":  url_for('manga_home', mg=mg["filename"])
        } for mg in database.get_all_mangas()
    ]}

@cache.memoize()
def get_manga_home(mg_file):
    """
    """

    #TODO

    if DEBUG:
        return {
            "name":"Boruto",
            "chapters_list": []
        }

    return {}

    raise NotImplementedError()

def get_home_feed():
    #TODO
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

@app.route('/lecture/<string:mg>/<float:chapter>')
def reading(mg, chapter):
    data = get_reading_data(mg, chapter)
    if DEBUG2: return jsonify(data)
    return render_template("lecture.html", **data)

@app.route('/mangas_list')
def mangas_list():

    data = get_mangas_list()

    if "search" in request.args:
        data = filter_mangas(data, request.args["search"])

    if DEBUG2: return jsonify(data)
    return render_template('mangas.html', **data)

@app.route('/manga/<string:mg>')
def manga_home(mg):
    data = get_manga_home(mg)
    if DEBUG2: return jsonify(data)
    return render_template("chapters.html", **data)

@app.route('/')
@cache.cached()
def home():
    data = get_home_feed()
    if DEBUG2: return jsonify(data)
    return render_template('homepage.html', **data)

@app.route('{}<img_file>'.format(config["images_route"]))
def images(img_file):
    return send_from_directory(config["images_path"], img_file, mimetype="image/jpg")

@app.route('/update', methods=['POST'])
def update(mg):
    if "manga" not in request.args:
        abort(404)

    manga_name = request.args["manga"]

    if manga_name == "__all__":
        update_all()

    if manga_name not in database.get_mangas_list():
        abort(404)

    update_manga(manga_name)

@app.route('/add_manga', methods=['GET', 'POST'])
def add_manga():
    return "Add_Manga page" #TODO

@app.route('search'):
def manga_search():
    if "manga" not in request.args:
        abort(404)
    #TODO

    data = get_mangas_list()
    data = filter_mangas(data, request.args["manga"])

    return jsonify(data)


def main():
    init()
    app.run(debug=True, host="0.0.0.0", port=80)

if __name__ == "__main__":
    main()
