from flask import Flask, Blueprint, session, render_template, request, make_response, jsonify, redirect, url_for
from flask_login import login_user, current_user, login_required

wordquiz = Blueprint('wordquiz', __name__)


@wordquiz.route('/<level>', methods=['GET'])
def show_quiz(level):
    print(level)
    return render_template('word_quiz.html', level=level)
