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

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    print(email, password, remember_me)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/")
def index():
    lessons = ["Знакомство со средой", "Условный оператор", "Простые встроенные функции",
               "Знакомство с циклом while", "Знакомство с циклом for"]
    return render_template("main.html", lessons=lessons)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        print()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")

@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = RegisterForm()
    if request.method == 'POST' and 'photo' in request.files:
        print(request.files)
        filename = photos.save(request.files['photo'])
        return 'Файл успешно загружен: {}'.format(filename)
    return render_template('register.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if request.method == 'POST' and 'photo' in request.files:
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            filename = photos.save(request.files['photo'], name=str(int(open("lastsaved.txt").read()) + 1) + ".jpg")
            t = str(int(open("lastsaved.txt").read()) + 1)
            open("lastsaved.txt", "w").write(t)
            user = User(
                name=form.name.data,
                email=form.email.data,
                about=form.about.data,
                avatar_path=filename
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form, message="загрузите аватар")
    return render_template('register.html', title='Регистрация', form=form)

def main():
    db_session.global_init("for_users.db")
    app.run()


if __name__ == '__main__':
    main()