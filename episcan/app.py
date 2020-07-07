from flask import Flask, render_template, url_for, send_from_directory
from flask_caching import Cache

from episcan import lang, manga

###################################
### INIT
###################################

CONFIG_FILENAME = "app_config.json"
CONFIG_CACHE    = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask("episcan")
app.config.from_mapping(CONFIG_CACHE)
app.config.from_json(CONFIG_FILENAME)
cache = Cache(app)

###################################
### Backend bindings
###################################

def get_reading_data(manga, chapter):
    """

    """

    if app.config["DEBUG"]:
        return {
            "manga_title": "Boruto",
            "chapter_num": "1",
            "manga_home_url": "/manga_home_url",
            "chapters_url_list": [(1.0, "/chapters_url_list1"), (3.0, "/chapters_url_list3")],
            "prev_chap_url": "/prev_chap_url",
            "next_chap_url": "/next_chap_url",
            "image_url": "/images/1.jpg",
            "chapter_nb_pages": 2,
            "images_route": "/images/",
            "images_id": ["1.jpg", "2.jpg"]
        }

    manga   = find_manga(manga)
    chapter = manga.find_chapter(chapter)

    return {
        "manga_title": manga.name,
        "chapter_num": chapter.num,
        "manga_home_url": url_for('manga_home', manga.filename),
        "chapters_url_list": sorted(manga.chapters),
        "prev_chap_url": url_for('reading', manga.filename, num),
        "next_chap_url": url_for('reading', manga.filename, num),
        "image_url": url_for('image', chapter.pages[0]),
        "chapter_nb_pages": chapter.nb_pages,
        "images_route": "/images/",
        "images_id": chapter.pages
    }

def get_mangas_list():

    if app.config["DEBUG"]:
        return {"list": [
            {"name": "Boruto", "url": url_for('manga_home', "boruto")}
        ]}


    return {"list":[
        {
            "name": manga.name,
            "url":  url_for('manga_home', manga.filename)
        } for manga in mangas
    ]}

def get_manga_home(manga):

    if app.config["DEBUG"]:
        return {
            "name":"Boruto",
            "chapters_list": []
        }

def get_home_feed():
    return dict()

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
    return render_template("lecture.html", **data)

@app.route('/mangas_list')
def mangas_list():
    data = get_mangas_list()
    return render_template('mangas.html', **data)

@app.route('/manga/<string:manga_name>')
def manga_home(manga):
    data = get_manga_home(manga)
    return render_template("chapters.html", **data)

@app.route('/')
@cache.cached(timeout=300)
def home():
    data = get_home_feed()
    return render_template('homepage.html', **data)

@app.route('/images/<img_file>')
def image(img_file):
    return send_from_directory(app.config["images_path"], img_file, mimetype="image/png")


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
