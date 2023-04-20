from flask import Flask, abort
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.users import User
import datetime
from flask import request
from data.news import News
from flask import render_template

from forms.news import NewsForm
from forms.users import RegisterForm
from flask import redirect
from flask import make_response
from flask import session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__, static_folder="static")
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        print(request.files)
        filename = photos.save(request.files['photo'])
        return 'Файл успешно загружен: {}'.format(filename)
    return render_template('upload.html')

app.run()