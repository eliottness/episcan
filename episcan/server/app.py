from flask import Flask, render_template, url_for
app = Flask(__name__)

data = {
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

@app.route('/')
def lecture():
    return render_template("lecture.html", **data)
