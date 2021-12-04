from flask import Flask, render_template, jsonify
from flask.helpers import make_response, url_for
from flask_login import LoginManager, current_user, login_manager,login_required, login_user, logout_user, fresh_login_required
from flask_cors import CORS
from view import quiz
from view import kanji
import os
from controllers.crawling_controller import DataCrawling

# allows http
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')

# Blueprints
app.register_blueprint(quiz.wordquiz, url_prefix='/quiz/words')
app.register_blueprint(kanji.kanjiquiz, url_prefix='/quiz/kanji')

CORS(app, supports_credentials=True)
app.secret_key = os.urandom(24)  # varies whenever the server is started
'''
# User session management setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
'''

# 보통 앱을 생성한 다음 바로 지정
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('warning.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


@app.route('/')
def show_main():
    return render_template('top.html')


@app.route('/collect')
def collect_data():
    DataCrawling.collect_data()
    return make_response(jsonify(success=True), 200)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_notfound.html'), 404

'''
# TODO - render_template
@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)
'''

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8081', debug=True)

