from flask import Flask, Blueprint,render_template

kanjiquiz = Blueprint('kanjiquiz', __name__)


@kanjiquiz.route('/<level>', methods=['GET'])
def show_kanji(level):
    
    return render_template('kanji_quiz.html', level=level)