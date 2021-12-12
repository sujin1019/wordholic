from flask import Flask, Blueprint, session, render_template, request, make_response, jsonify, redirect, url_for
from flask_login import login_user, current_user, login_required
from controllers.word_controller import Quiz

wordquiz = Blueprint('wordquiz', __name__)
wordanswer = Blueprint('wordanswer', __name__)


@wordquiz.route('/n<int:level>', methods=['GET'])
def show_quiz(level):
    word_list = Quiz.get_word_list(level, 10)
    return render_template('word_quiz.html', level=level, word_list=word_list)


@wordanswer.route('/', methods=['POST'])
def check_answer():
    user_answer = request.json
    result = Quiz.check_answer(user_answer)
    
    return make_response(jsonify(success=True, result=result), 200)

