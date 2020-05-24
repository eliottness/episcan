from flask import Flask, render_template
app = Flask(__name__)


data = {
    "name":"One Piece",
    "chap":979,
    "page":1,
    "date":"20 mai 2020",
    "lang":"VF",
    "title":"Luffy mange des nouilles",
    "chapters":list(enumerate(["https://www.google.com", "/", "/", "/"])),
    "pages":list(enumerate(["https://www.google.com", "/", "/", "/"])),
    "next_link":"https://japscan.co",
    "image": "/static/Capture.PNG",
    "next_image":""
}

@app.route("/")
def template_test():
    return render_template('lecture.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
