from flask import Blueprint, render_template, make_response, jsonify, request
from controllers.word_controller import Kanji

kanjiquiz = Blueprint('kanjiquiz', __name__)
kanjihint = Blueprint('kanjihint', __name__)
kanjianswer = Blueprint('kanjianswer', __name__)


@kanjiquiz.route('/<int:level>', methods=['GET'])
def show_kanji(level):
    kanji_list = Kanji.get_kanji_list(level, 10)

    return render_template('kanji_quiz.html', level=level, kanji_list=kanji_list)


@kanjihint.route('/', methods=['GET'])
def give_hint():
    row_id = request.args.get('row_id')
    hint = Kanji.get_hint(row_id)
    
    return make_response(jsonify(succss=True, hint=hint), 200)


@kanjianswer.route('/', methods=['POST'])
def check_answer():
    user_answer = request.json
    result = Kanji.check_answer(user_answer)
    
    return make_response(jsonify(success=True, result=result), 200)

