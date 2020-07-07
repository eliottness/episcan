from flask import Flask, render_template, url_for
from flask_caching import Cache

###################################
### INIT
###################################

CONFIG_FILENAME = "app_config.json"
CONFIG_CACHE    = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(CONFIG_CACHE)
app.config.from_json(CONFIG_FILENAME)
cache = Cache(app)

###################################
### Backend bindings
###################################

def reading_data(manga, chapter):
    return {
        "manga_title": "Boruto",
        "chapter_num": "1",
        "manga_home_url": "/manga_home_url",
        "chapters_url_list": [(1.0, "/chapters_url_list1"), (3.0, "/chapters_url_list3")],
        "prev_chap_url": "/prev_chap_url",
        "next_chap_url": "/next_chap_url",
        "page_num": 1,
        "chapter_nb_pages": 2,
        "images_id": ["/static/images/1.jpg", "/static/images/2.jpg"]
    }

def home_feed():
    return dict()

###################################
### Routes
###################################

@app.route('/lecture/<string:manga>/<float:chapter>')
def lecture(manga, chapter):
    data = reading_data(manga, chapter)
    return render_template("lecture.html", **data)

@app.route('/')
@cache.cached(timeout=300)
def home():
    data = home_feed()
    return render_template('homepage.html', **data)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
