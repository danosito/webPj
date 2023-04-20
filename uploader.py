from flask import request, render_template
import datetime
import flask
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

app = flask.Flask(__name__, static_folder="static")
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return 'Файл успешно загружен: {}'.format(filename)
    return render_template('upload.html')

app.run()