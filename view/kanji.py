from flask import Flask, Blueprint,render_template
from controllers.word_controller import Kanji

kanjiquiz = Blueprint('kanjiquiz', __name__)


@kanjiquiz.route('/<int:level>', methods=['GET'])
def show_kanji(level):
    kanji_list = Kanji.get_kanji_list(level, 10)

    return render_template('kanji_quiz.html', kanji_list=kanji_list)