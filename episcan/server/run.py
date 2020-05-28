from flask import Flask, render_template
app = Flask(__name__)


data_lecture = {
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

data_chapters = {
    "name":"One Piece",
    "image": "/static/Capture.PNG",
    "author": "Eiichirō Oda",
    "synopsis": "Monkey D. Luffy est un garçon espiègle, rêve de devenir le roi des pirates en trouvant le «One Piece», un fabuleux et mystérieux trésor. Mais, par mégarde, Luffy a avalé un jour un «fruit magique du démon» qui l&#039;a transformé en homme caoutchouc. Depuis, il est capable de contorsionner son corps élastique dans tous les sens, mais il a perdu la faculté de nager, le comble pour un pirate ! Au fil d&#039;aventures toujours plus rocambolesques et de rencontres fortuites, Luffy va progressivement composer son équipage et multiplier les amitiés avec les peuples qu&#039;il découvre, tout en affrontant de redoutables ennemis.",
    "chapters":list(enumerate(["https://www.google.com", "/", "/", "/"])),
}

data_homepage = {
    "mangas" : list([("One Piece", "979", "Luffy mange des nouilles")]),
}

data_mangas = {
    "mangas" : list([("One Piece", "/static/Capture.PNG")]),
}

@app.route("/")
def template_test():
    return render_template('mangas.html', **data_mangas)

if __name__ == '__main__':
    app.run(debug=True)
